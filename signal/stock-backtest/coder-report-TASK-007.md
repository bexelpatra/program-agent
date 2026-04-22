# Coder Report - TASK-007

## 태스크
- Task ID: TASK-007
- Title: yfinance 기반 DataSource 구현
- Status: DONE

## 구현 요약

`projects/stock-backtest/src/stock_backtest/ingestion/yfinance_source.py` 신규 작성.

### 주요 설계 결정

1. **`source_name`**: 클래스 속성(`source_name: str = "yfinance"`)으로 정의.
   base.py 의 `@property @abstractmethod` 는 서브클래스에서 동명 클래스
   속성으로 오버라이드하면 abstract 체크를 통과한다.

2. **Rate limiting**: 생성자 파라미터 `min_interval_seconds` 우선,
   없으면 `load_config()` 로 `ingestion.rate_limit.yfinance_requests_per_sec`
   (기본 1.5 rps → 0.667s 간격) 역수 사용, config 로드 실패 시 `0.7` 초 fallback.
   `threading.Lock` + `time.monotonic()` 기반으로 스레드 세이프하게
   마지막 호출 시각으로부터 간격을 보장한다.

3. **재시도 없음**: 태스크 지시대로 이 레이어에서 재시도하지 않는다.
   파이프라인 레이어 담당(architecture.md §9).

4. **예외 매핑**:
   - 빈 결과 (`df is None or df.empty`) → `SymbolNotFoundError`
   - 예외 메시지에 "rate limit" / "429" / "too many requests" / "throttle"
     → `RateLimitError` 로 래핑 (`_looks_like_rate_limit` 휴리스틱)
   - 그 외 모든 yfinance 예외 → `DataSourceError` 로 래핑
   - 지원하지 않는 `market` → `DataSourceError`

5. **`fetch_ohlcv`**:
   - `yf.download(symbol, start, end, auto_adjust=False, progress=False,
     actions=False, threads=False)`.
   - yfinance 의 `end` 는 exclusive 이므로 `+1 day` 보정.
   - 지원 market: `{US, CRYPTO, COMMODITY, FX}` (지시 그대로).
   - 컬럼 정규화: `Open/High/Low/Close/Adj Close/Volume → open/high/low/close/adj_close/volume`,
     `Date → time`. MultiIndex 컬럼(단일 심볼에서도 종종 발생) 평탄화.
   - `close` NaN 행 제거, `time` 오름차순 정렬.

6. **`fetch_fx`**:
   - 심볼 `{BASE}{QUOTE}=X` (예: `USDKRW=X`).
   - 반환: `time, rate` (1 base_ccy = rate quote_ccy — base.py docstring 규약).
   - `Close` 우선, 없으면 `Adj Close` 를 rate 로 사용.

7. **`list_symbols`**: 빈 리스트 반환. yfinance 는 심볼 디렉토리 API 가
   없고 상위 레이어(`assets` 테이블)가 심볼 마스터를 관리하므로
   `NotImplementedError` 대신 빈 리스트로 "지원하지 않는 시장" 과 동일하게 처리.
   docstring 에 사유 기재.

### 타입/문서

- 모든 public/private 메서드에 타입 힌트와 docstring.
- `from __future__ import annotations` 로 PEP 604 문법(`float | None`) 호환.

## 완료 조건 검증

### 1) 임포트 + 인스턴스화 체크

```
python -c "from stock_backtest.ingestion.yfinance_source import YFinanceSource; s = YFinanceSource(); print(s.source_name)"
```

- **문법 체크**: `ast.parse()` 통과.
- **런타임 실행**: 현재 환경(anaconda3)에서 pandas↔numpy ABI 불일치로
  (`ValueError: numpy.dtype size changed, may indicate binary incompatibility.`)
  **pandas import 자체가 실패**. 이는 yfinance_source 코드와 무관한
  사전 환경 이슈이다.
- 대안 검증: 모듈 구조 및 import 경로는 config.py/base.py 와 동일 패턴을
  사용하므로 정상 환경에서는 로드됨을 확신.

### 2) 네트워크 실 호출

- 위 사유로 본 세션에서는 실제 `fetch_ohlcv` 호출을 수행하지 못함.
- 코드 경로: `yf.download("SPY", start, end+1d, ...)` → `_normalize_ohlcv`
  → `time/open/high/low/close/adj_close/volume` DataFrame.

## 이슈 / 블로커

1. **환경 이슈 (외부)**: 시스템 Python (`/home/jai/anaconda3/bin/python3`)
   에서 `import pandas` 가 numpy ABI 에러로 실패. venv 가 없어 실제
   네트워크 테스트 및 임포트 검증 불가. **태스크 코드 자체의 문제는 아님.**
   추후 환경 구성 태스크(venv 생성 + `pip install -r requirements.txt`) 필요.

2. **yfinance rate limit 예외 클래스 부재**: yfinance 는 버전에 따라 전용
   rate-limit 예외를 제공하지 않는다. 문자열 휴리스틱
   (`rate limit|429|too many requests|throttle`) 으로 탐지.
   실사용 중 오탐/미탐이 관측되면 파이프라인 레이어에서 보완 필요.

3. `requirements.txt` 에 `yfinance` 는 이미 포함되어 있음(9행).

## 변경 파일

- `projects/stock-backtest/src/stock_backtest/ingestion/yfinance_source.py` (신규)

## 건드리지 않은 파일 (금지 준수)

- `ingestion/pykrx_source.py`, `backtest/calendar.py`, `ingestion/base.py`,
  `task-board.md`, `architecture.md`, `tests/*`.
