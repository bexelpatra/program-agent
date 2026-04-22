---
agent: coder
task_id: TASK-006
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약
DataSource 추상 인터페이스와 공통 예외 계층을 `ingestion/base.py`에 정의했다. `abc.ABC` 기반으로 `fetch_ohlcv`, `fetch_fx`, `list_symbols`, `source_name` property를 @abstractmethod로 선언하고 각 메서드 docstring에 반환 DataFrame의 컬럼 명세를 명시했다. `DataSourceError`, `SymbolNotFoundError`, `RateLimitError`도 같은 모듈에 포함했다. `from stock_backtest.ingestion.base import DataSource` import 정상 동작 확인.

## 변경된 파일
- projects/stock-backtest/src/stock_backtest/ingestion/base.py (신규)

## 이슈/블로커
없음. `__init__.py`는 이미 존재하여 추가 작업 없음.

## 다음 제안
- TASK-007 (또는 이후 태스크): `yfinance_source.py`, `pykrx_source.py` 구현으로 진행. 두 구현체는 본 인터페이스를 준수하고, rate-limit 발생 시 `RateLimitError`, 심볼 조회 실패 시 `SymbolNotFoundError`를 raise 하도록 구현할 것.
- `fetch_fx`의 rate 의미("1 base = rate quote")가 `fx_rates` 테이블 컬럼 정의와 일치하는지 데이터 레이어 담당자와 한 번 더 확인 권장.
