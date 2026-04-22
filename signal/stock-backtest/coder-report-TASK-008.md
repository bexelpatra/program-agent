# Coder Report - TASK-008

- Task ID: TASK-008
- Title: pykrx 기반 DataSource 구현 (KR 지수/ETF)
- Status: DONE
- Agent: Coder

## 변경 파일
- 신규: `projects/stock-backtest/src/stock_backtest/ingestion/pykrx_source.py`

## 구현 요약

`PykrxSource(DataSource)` 구현 완료. 주요 사항:

- `source_name = "pykrx"` (read-only property).
- `__init__(self, min_interval_seconds: float = 0.1)`: 음수 거부, 내부 `_last_call_ts` 관리.
- `_respect_rate_limit()`: `time.monotonic()` 기반으로 직전 호출로부터 `min_interval_seconds` 가 경과할 때까지 sleep. 0 이면 sleep 생략. pykrx 호출 직전에만 호출.
- `fetch_ohlcv(symbol, market, start, end)`:
  - 허용 market: `{"KR", "KOSPI", "KOSDAQ"}`. 그 외는 `DataSourceError`.
  - 심볼 분기: 6자리 숫자면 `pykrx.stock.get_market_ohlcv` (종목/ETF), 그 외는 `pykrx.stock.get_index_ohlcv` (지수 코드 `KS11`, `KQ11`, `KRX100`, `1001` 등).
  - pykrx 는 지연 import (미설치 환경에서도 모듈 로드 가능).
  - 한글 컬럼(시가/고가/저가/종가/거래량) → 표준 컬럼 매핑.
  - 빈 응답 / 미지 심볼 → `SymbolNotFoundError`.
  - pykrx 예외는 `DataSourceError` 로 래핑 (원인 체인 유지).
  - 인덱스(날짜)를 `time` 컬럼으로 승격, `pd.to_datetime` 으로 정규화.
  - `adj_close = close` 로 채움 (pykrx 미제공 — docstring 에 명시).
  - 지수 응답에 `volume` 이 없으면 0 으로 채움.
  - 최종 스키마: `time, open, high, low, close, adj_close, volume` + `time` 오름차순 정렬.
- `fetch_fx(...)`: `NotImplementedError("pykrx does not provide FX; use YFinanceSource")`.
- `list_symbols(market)`:
  - `"KR"` → `get_market_ticker_list(market="KOSPI") + get_market_ticker_list(market="KOSDAQ")` 합산, 중복 제거.
  - 구버전 pykrx 대비: `TypeError` 발생 시 market 키워드 없이 호출(fallback).
  - 그 외 market → 빈 리스트.
  - pykrx 예외는 `DataSourceError` 로 래핑.
- 타입 힌트, docstring 완비. `__all__ = ["PykrxSource"]`.

## 설계 메모
- pykrx 는 임의 import 순서에서 문제가 없도록 **지연 import** 방식으로 처리 (모듈 로드만은 pykrx 미설치/네트워크 차단 환경에서도 성공).
- architecture.md §13 (비거래일 방어) 준수: 빈 응답을 `SymbolNotFoundError` 로 올려 상위 pipeline 이 `ingestion_log` 에 기록하고 스킵할 수 있게 함.
- config 의 `ingestion.rate_limit.pykrx_min_interval_ms` 값은 호출자가 `min_interval_seconds = settings.ingestion.rate_limit.pykrx_min_interval_ms / 1000` 로 전달하는 구조. `PykrxSource` 내부에서 직접 config 를 로드하지 않아 의존성을 단순하게 유지.

## 완료 조건 검증
- `python -m py_compile .../pykrx_source.py` → OK.
- 의도한 import 경로: `from stock_backtest.ingestion.pykrx_source import PykrxSource`. 런타임 import 검증은 현재 `python` 환경의 pandas/numpy 바이너리 호환 문제(numpy 2.4.4 vs 기존 pandas)로 실행 불가 — **프로젝트 코드와 무관한 환경 이슈**. 파일은 바이트 컴파일 성공, 문법/구조 정상.
- 네트워크 테스트는 선택이라 생략.

## 금지 사항 준수
- `task-board.md`, `architecture.md`, `tests/` 미수정.
- `ingestion/yfinance_source.py`, `backtest/calendar.py` 미접근.

## 이슈/블로커
- 없음. 다음 태스크 진행 가능.
