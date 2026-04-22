# stock-backtest

한국 거주자 관점에서 글로벌 자산(지수/ETF/채권/원자재/암호화폐)을 대상으로
시계열 데이터 수집, 계절성 분석, 정적/동적 자산배분 전략 백테스트를
수행하는 플랫폼이다.

> **V2 재구축 중** — 웹(Dash) 계층은 제거되었으며, 외부 인터페이스는
> FastAPI 기반 API로 재구성될 예정이다. API 엔드포인트 문서는 TASK-117
> 완료 후 갱신된다.

---

## 1. 프로젝트 소개

- **대상 사용자**: 한국 거주 개인 투자자 / 퀀트 실험자.
- **목적**: 세제·환율을 실제 환경에 맞춰 반영한 백테스트로 정적/동적
  자산배분과 계절성 아이디어를 검증한다.
- **주요 특징**
  - **한국 거주자 세금 모듈**: 해외주식 양도세 22% + 250만원 공제,
    해외 배당 15.4% 원천징수, 국내 ETF 세제 분류(`kr_tax_class`),
    암호화폐 양도세(on/off 가능)를 리밸런싱 시점에 자동 반영
    (architecture.md §14).
  - **다중 통화 / FX 환전 비용**: 자산은 native currency로 체결·보유하고
    평가는 `base_currency`로 환산. 크로스-커런시 리밸런싱 시
    `fx_spread_bps`(기본 20bp)를 차감.
  - **TimescaleDB**: `ohlcv`, `backtest_equity`를 hypertable로 운영.
  - **전략 registry**: `src/stock_backtest/strategies/` 하위에 파일을 하나
    만들고 `@register` 데코레이터만 달면 자동 등록된다.
  - **market_mode**: `STOCK` / `CRYPTO` / `MIXED` — 주식 거래일 캘린더와
    암호화폐(UTC 00:00 365일)의 시간축 불일치를 안전하게 처리.

## 2. 아키텍처 개요

전체 설계는 `signal/stock-backtest/architecture.md`를 참조한다. 요점만
추리면:

- **언어/런타임**: Python 3.11+.
- **DB**: PostgreSQL 16 + TimescaleDB (Docker Compose로 기동).
- **데이터 소스**: `yfinance`(US/원자재/암호화폐/FX), `pykrx`(KR).
- **거래일 캘린더**: `exchange_calendars`.
- **수치/분석**: `pandas`, `numpy`, `scipy`.
- **설정**: `.env` + `config/defaults.yaml`.
- **백테스트 엔진**: 벡터화 직접 구현(이벤트 루프 없음). 리밸런싱 시점에만
  목표 비중 vs 현재 비중 차이로 거래 생성.
- **핵심 디렉토리**

  ```
  src/stock_backtest/
  ├── data/          # ORM, 세션, 리포지토리
  ├── ingestion/     # DataSource, pipeline, CLI
  ├── analysis/      # seasonality, political_cycle, stats
  ├── strategies/    # base + registry + static/dynamic
  ├── backtest/      # engine, portfolio, fx, tax, calendar, cache, run_store
  └── metrics/       # performance
  ```

## 3. 설치

```bash
# 1) Python 3.11+ 확인
python --version

# 2) 가상환경
python -m venv .venv
source .venv/bin/activate

# 3) 의존성
pip install -r requirements.txt
pip install -r requirements-dev.txt   # 개발/테스트 시

# 4) 환경변수
cp .env.example .env
# .env 편집 (DB 접속, 기타 옵션)

# 5) Docker Compose (Postgres + TimescaleDB)
docker compose up -d
docker compose ps              # healthy 확인

# 6) Alembic 마이그레이션 적용
alembic upgrade head

# 7) 초기 데이터 seed
python scripts/seed_universe.py        # 자산 universe 등록
python scripts/seed_market_events.py   # 대선/중간선거/FOMC/실적시즌 등
```

기본 DB 접속 정보: host=`localhost`, port=`5432`, user=`stock`,
password=`stock`, db=`stock_backtest` (테스트는 `stock_backtest_test`).

## 4. 데이터 수집

`ingestion.cli`는 `assets` 테이블의 active 자산 기준으로 DB 증분 수집을
수행한다(architecture.md §9).

```bash
# KR 시장 전체 수집
python -m stock_backtest.ingestion.cli --market KR

# US 시장, 특정 심볼만
python -m stock_backtest.ingestion.cli --market US --symbols SPY,QQQ

# 전체 시장 순차 실행 (KR -> US -> CRYPTO)
python -m stock_backtest.ingestion.cli --market ALL

# dry-run: 대상 자산만 열거하고 DB 쓰기 없음
python -m stock_backtest.ingestion.cli --market KR --dry-run

# 상세 로그
python -m stock_backtest.ingestion.cli --market US --log-level DEBUG
```

CLI 플래그 요약:

| 플래그 | 설명 |
|--------|------|
| `--market {KR,US,CRYPTO,ALL}` | 대상 시장 (필수). `ALL`은 KR→US→CRYPTO 순차. |
| `--symbols SYM1,SYM2,...` | 해당 시장의 자산 중 이 심볼만 수집. |
| `--dry-run` | 대상 자산 열거만, 실제 수집 없음. |
| `--log-level {DEBUG,INFO,WARNING,ERROR}` | 로그 레벨(기본 INFO). |

종료 코드: `0` 성공 / `1` 일부 실패 / `2` 전체 실패 또는 내부 예외.

### Cron 스케줄

시장별 권장 스케줄(KST):

| 시장 | 스케줄 | 근거 |
|------|--------|------|
| KR | 매일 18:00 | KRX 장 마감(15:30) 이후 종가 확정 여유 |
| US | 매일 07:00 | 전일 미국 장 마감 후 익일 새벽 수집 |
| Crypto | 매일 09:00 | UTC 00:00 일봉 확정 = KST 09:00 |

상세 설치 방법과 샘플 crontab은 [`docs/cron.md`](docs/cron.md) 및
[`docker/cron/crontab.example`](docker/cron/crontab.example)을 참조한다.
(`CRON_TZ=Asia/Seoul` 고정 필수.)

## 5. 백테스트 실행 (Python API)

현재 V2 재구축 중이므로 프로그램에서 직접 호출하는 방식만 지원한다.
외부 API 인터페이스는 TASK-117 이후 추가된다.

```python
import datetime as dt
from decimal import Decimal

from stock_backtest.config import load_config
from stock_backtest.data import db
from stock_backtest.backtest.engine import BacktestConfig, BacktestEngine, AssetSpec
from stock_backtest.strategies.registry import get_strategy

settings = load_config()

spec_spy = AssetSpec(asset_id=1, symbol="SPY", market="US", currency="USD")
spec_agg = AssetSpec(asset_id=2, symbol="AGG", market="US", currency="USD")

cfg = BacktestConfig(
    strategy_name="fixed_weight",
    params={"weights": {"SPY": 0.6, "AGG": 0.4}},
    universe=[spec_spy, spec_agg],
    period_start=dt.date(2015, 1, 1),
    period_end=dt.date(2024, 12, 31),
    base_currency="USD",
    market_mode="STOCK",
    initial_capital=Decimal("100000"),
    rebalance_freq="ME",
)

StrategyCls = get_strategy(cfg.strategy_name)
strategy = StrategyCls(StrategyCls.params_schema(**cfg.params))

engine = BacktestEngine(settings=settings, session_factory=db.get_session)
result = engine.run(cfg, strategy)

print(result.equity_curve.tail())
print("tax paid by year:", result.tax_paid_by_year)
```

`BacktestResult`는 `equity_curve`(pd.Series), `trades`, `realized_trades`,
`tax_paid_by_year`, `run_hash`를 포함한다. 같은 조건 재실행 시
`run_hash` 기반 캐시를 확인한다(architecture.md §10, §11).

## 6. 새 전략 추가법

1. `src/stock_backtest/strategies/static/` 또는 `.../dynamic/` 아래에 파일을 하나 만든다.
2. `StrategyParams`를 상속한 pydantic 모델로 파라미터 스키마를 선언한다.
3. `Strategy`를 상속한 클래스를 만들고 `@register` 데코레이터를 붙인다.
4. 그걸로 끝이다 — registry가 자동 스캔한다.

```python
# src/stock_backtest/strategies/static/my_tilt.py
from __future__ import annotations
import pandas as pd
from pydantic import Field

from stock_backtest.strategies.base import Strategy, StrategyParams
from stock_backtest.strategies.registry import register


class MyTiltParams(StrategyParams):
    equity_weight: float = Field(0.7, ge=0.0, le=1.0, description="주식 비중")
    bond_weight: float = Field(0.3, ge=0.0, le=1.0, description="채권 비중")


@register
class MyTiltStrategy(Strategy):
    name = "my_tilt"
    params_schema = MyTiltParams
    description = "사용자 정의 주식/채권 기울임 포트폴리오"

    def generate_weights(
        self,
        prices: pd.DataFrame,
        rebalance_dates: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        w = pd.DataFrame(0.0, index=rebalance_dates, columns=prices.columns)
        if "SPY" in w.columns:
            w["SPY"] = self.params.equity_weight
        if "AGG" in w.columns:
            w["AGG"] = self.params.bond_weight
        return w.div(w.sum(axis=1), axis=0)  # 행 합=1 정규화

    def required_universe(self) -> list[str] | None:
        return None  # 사용자 universe 허용
```

## 7. 테스트

```bash
pytest

# 개별 파일
pytest tests/test_strategy_integration.py -v
```

## 8. 디렉토리 레이아웃

핵심 트리(요약):

```
projects/stock-backtest/
├── README.md
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── config/
│   └── defaults.yaml           # 수수료/슬리피지/FX/리밸런싱/세금 디폴트
├── docker/
│   └── cron/crontab.example
├── docs/
│   └── cron.md
├── migrations/                 # Alembic
│   └── versions/
├── scripts/
│   ├── seed_universe.py
│   └── seed_market_events.py
├── src/stock_backtest/
│   ├── config.py
│   ├── data/ (models, db, repository)
│   ├── ingestion/ (base, yfinance_source, pykrx_source, pipeline, cli)
│   ├── analysis/ (seasonality, political_cycle, stats)
│   ├── strategies/ (base, registry, static/, dynamic/)
│   ├── backtest/ (engine, portfolio, fx, tax, calendar, calendar_guard,
│   │              cache, run_store)
│   └── metrics/ (performance)
└── tests/
```

## 9. 라이선스 / 면책

본 프로젝트는 연구·실험용 오픈 코드다. **투자 조언이 아니며**, 여기서
산출된 백테스트 결과로 인한 실제 투자 손익에 대해 어떤 책임도 지지
않는다.
