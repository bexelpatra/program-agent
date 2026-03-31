# Architecture

## 개요

**프로젝트명**: Asset Price Tracker & Analyzer

yfinance API를 이용하여 자산 가격 변동을 추적·저장하고, 축적된 데이터에서 계절성과 패턴을 분석하며, 전략을 백테스팅하는 시스템.

### 기술 스택
- **언어**: Python 3.11+
- **데이터 수집**: yfinance (Yahoo Finance API 래퍼)
- **데이터베이스**: ClickHouse (시계열 최적화 컬럼형 DB)
- **DB 드라이버**: clickhouse-connect (공식 Python 드라이버, HTTP 기반, 빠른 insert/select)
- **분석**: pandas, statsmodels (STL 분해), scipy (통계 검정)
- **로깅**: Python logging → 파일 + 콘솔 (cron 디버깅용)
- **스케줄링**: cron (시스템)

### 추적 자산 (Phase 1)
| 자산 | yfinance 티커 | 설명 | 데이터 시작 |
|------|---------------|------|-------------|
| S&P 500 | `^GSPC` | 미국 대형주 지수 | ~1927년 |
| Gold Futures | `GC=F` | 금 선물 | ~2000년 |
| US 20Y+ Treasury Bond ETF | `TLT` | 미국 중장기 국채 ETF | 2002년 |

### 확장 로드맵
- **Phase 2**: 자산 확대 (코인, 원자재, 해외 지수), GPU 가속 분석 (cuDF, PyTorch)
- **Phase 3**: 증권사 API 연동 자동매매, 실시간 스트리밍

## 구조

```
src/
├── __init__.py
├── config.py              # 설정 (티커 목록, DB 연결, 로깅)
├── database.py            # ClickHouse 연결 및 CRUD
├── collector.py           # yfinance 데이터 수집 (백필 + 증분)
├── analyzer/              # 분석 프레임워크 (플러그인 구조)
│   ├── __init__.py        # StrategyRegistry (전략 자동 등록)
│   ├── base.py            # BaseStrategy 추상 클래스
│   ├── seasonality.py     # STL 계절성 분해 전략
│   ├── moving_average.py  # 이동평균 크로스오버 전략
│   └── correlation.py     # 자산 간 상관관계 분석
├── backtester.py          # 백테스팅 엔진
├── run_collector.py       # Collector 엔트리포인트 (cron용)
└── run_analyzer.py        # Analyzer 엔트리포인트 (CLI)

tests/
├── __init__.py
├── test_database.py
├── test_collector.py
├── test_strategies.py
└── test_backtester.py

logs/                      # 로그 파일 디렉토리 (gitignore)
requirements.txt
run_collector.sh           # cron 실행용 셸 스크립트
```

## 설계 결정

### 1. ClickHouse 테이블 설계
- **결정**: ReplacingMergeTree 엔진, `(symbol, date)` 기본 키, 월 단위 파티셔닝
- **이유**: 시계열 데이터는 시간 범위 쿼리가 대부분이므로 파티셔닝으로 불필요한 파티션 스캔을 제거. symbol을 기본 키에 포함하여 자산별 조회 최적화.

#### 메인 테이블: `asset_prices`
```sql
CREATE TABLE IF NOT EXISTS asset_prices (
    symbol String,
    date Date,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    adj_close Float64,
    volume UInt64,
    collected_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(collected_at)
PARTITION BY toYYYYMM(date)
ORDER BY (symbol, date)
```

- **ReplacingMergeTree**: 같은 `(symbol, date)` 행이 중복 insert되면 `collected_at`이 최신인 행만 유지.

#### Materialized View: 월별 통계 (고속 집계용)
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_stats
ENGINE = AggregatingMergeTree()
PARTITION BY toYear(month)
ORDER BY (symbol, month)
AS SELECT
    symbol,
    toStartOfMonth(date) AS month,
    avgState(close) AS avg_close,
    maxState(high) AS max_high,
    minState(low) AS min_low,
    sumState(volume) AS total_volume,
    count() AS trading_days
FROM asset_prices
GROUP BY symbol, toStartOfMonth(date)
```

#### 일간 수익률 — 쿼리 시점 계산 (MV 아님)
```sql
-- database.py에서 제공하는 쿼리 함수
SELECT
    symbol, date, close,
    lagInFrame(close, 1) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
    if(prev_close > 0, (close - prev_close) / prev_close, 0) AS daily_return
FROM asset_prices
FINAL
WHERE symbol = {symbol:String}
ORDER BY date
```
- **MV를 사용하지 않는 이유**: ClickHouse MV는 INSERT 배치 내에서만 윈도우 함수가 동작한다. 증분 수집 시 1건만 INSERT되면 전날 데이터를 참조할 수 없어 항상 0이 된다. ClickHouse는 컬럼형 DB이므로 쿼리 시점 계산도 충분히 빠르다.

### 2. 데이터 수집 전략
- **결정**: 2단계 전략 — 초기 백필(max history) + 이후 증분 수집(마지막 날짜 이후)
- **이유**: yfinance는 전체 히스토리 한 번에 조회 가능 (`period="max"`). 이후에는 DB의 마지막 날짜부터만 수집하여 API 부하와 시간을 최소화.
- **티커 추가 시**: 새 티커는 DB에 데이터가 없으므로 자동으로 백필, 기존 티커는 증분 수집

### 3. Analyzer 플러그인 아키텍처
- **결정**: Strategy 패턴 기반 플러그인 구조 + 전략 레지스트리
- **이유**: 분석 전략을 독립적으로 추가/제거/교체할 수 있어야 함. 향후 GPU 전략, ML 모델, 자동매매 시그널 등을 같은 인터페이스로 통합 가능.

#### BaseStrategy 인터페이스
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import pandas as pd

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class Signal:
    date: str
    signal_type: SignalType
    weight: float = 1.0  # 0.0~1.0, 자본 대비 포지션 비율

class BaseStrategy(ABC):
    """모든 분석/매매 전략의 기본 클래스"""

    @property
    @abstractmethod
    def name(self) -> str:
        """전략 이름"""

    @property
    def description(self) -> str:
        """전략 설명 (선택)"""
        return ""

    @abstractmethod
    def analyze(self, df: pd.DataFrame, **params) -> dict:
        """
        분석 실행.
        - df: OHLCV DataFrame (symbol, date, open, high, low, close, adj_close, volume)
        - params: 전략별 파라미터 (이동평균 기간, 윈도우 크기 등)
        - return: {"summary": str, "metrics": dict, "details": DataFrame}
        """

    def generate_signals(self, df: pd.DataFrame, **params) -> list[Signal]:
        """
        매매 시그널 생성 (백테스팅용).
        기본 구현은 빈 시그널. 매매 전략만 오버라이드.
        weight로 포지션 크기 조절 가능 (향후 포트폴리오 전략 대비).
        """
        return []
```

#### StrategyRegistry (analyzer/__init__.py)
```python
class StrategyRegistry:
    """전략을 이름으로 등록/조회. 새 전략 파일 추가 시 여기에 등록."""
    _strategies: dict[str, BaseStrategy] = {}

    @classmethod
    def register(cls, strategy: BaseStrategy):
        cls._strategies[strategy.name] = strategy

    @classmethod
    def get(cls, name: str) -> BaseStrategy: ...

    @classmethod
    def list_all(cls) -> list[str]: ...
```

#### 확장 예시
```python
# 향후 GPU 전략 추가 시 — 같은 인터페이스, 내부만 GPU 사용
class GPUCorrelationStrategy(BaseStrategy):
    name = "gpu_correlation"
    def analyze(self, df, **params):
        import cudf
        gdf = cudf.from_pandas(df)
        ...

# 향후 자동매매 시그널 전략 — weight로 포지션 크기 지정
class MACDTradingStrategy(BaseStrategy):
    name = "macd_trading"
    def analyze(self, df, **params): ...
    def generate_signals(self, df, **params):
        # MACD 기반 BUY/SELL 시그널 + weight(포지션 비율) 생성
        return [Signal(date="2026-01-15", signal_type=SignalType.BUY, weight=0.5), ...]
```

### 4. 백테스팅 엔진
- **결정**: 전략의 `generate_signals()`를 받아 과거 데이터에서 시뮬레이션
- **이유**: 실제 매매 전에 전략의 수익률/리스크를 검증해야 함
- **설정**: 초기 자본, 수수료율, 슬리피지
- **포지션 추적**: Signal의 weight를 반영한 일별 포지션·잔고 계산
- **성과 지표**:
  - 총 수익률, 연환산 수익률(CAGR)
  - 최대 낙폭(MDD)
  - 샤프 비율 (무위험 수익률 설정 가능)
  - 승률, 평균 수익/손실 비율
- **벤치마크**: Buy & Hold 전략과 자동 비교
- **출력**: 터미널 리포트 + CSV 내보내기

### 5. 로깅 전략
- **결정**: Python logging 모듈, 파일 + 콘솔 동시 출력
- **이유**: cron 실행 시 터미널 출력을 볼 수 없으므로 파일 로깅 필수. 디버깅 시 콘솔에서도 확인 가능해야 함.
- **구성**: `logs/collector.log`, `logs/analyzer.log` (일별 로테이션)

### 6. CLI 인터페이스 (run_analyzer.py)
- **결정**: argparse 기반 서브커맨드
- **이유**: 분석과 백테스팅을 하나의 진입점에서 관리
- **커맨드**:
  - `python -m src.run_analyzer analyze --strategy seasonality --symbol ^GSPC`
  - `python -m src.run_analyzer backtest --strategy moving_average --symbol ^GSPC --capital 10000`
  - `python -m src.run_analyzer list` (등록된 전략 목록)

### 7. clickhouse-connect 선택
- **결정**: clickhouse-connect (공식 ClickHouse Python 드라이버)
- **이유**: HTTP 프로토콜 기반으로 별도 설정 없이 연결 가능, pandas DataFrame 직접 insert/select 지원, 공식 지원으로 안정적

## 현재 상태
설계 완료 — 태스크 분해 및 실행 대기
