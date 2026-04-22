# Coder Report - TASK-035

## 태스크
- Task ID: TASK-035
- Title: 비거래일 방어 모듈
- Status: DONE

## 결과
- 신규 파일 `projects/stock-backtest/src/stock_backtest/backtest/calendar_guard.py` 작성.
- 신규 테스트 `projects/stock-backtest/tests/test_calendar_guard.py` 작성 (15 tests, all pass).
- `repository.py`, `ingestion/*`, `analysis/political_cycle.py` 등 타 코더 작업 영역은 건드리지 않음. 본 태스크는 순수 유틸 모듈로만 구현했으며, repository/엔진 통합은 향후 태스크로 분리.

## 공개 API (요구 스펙 대비 매핑)
- `NonTradingDayError(ValueError)` — `market`, `date` 속성 보유.
- `MissingPriceError(ValueError)` — `asset_id`, `date` 속성 보유 (`asset_id`는 단일 자산 맥락이 아닌 경우 `None`).
- `validate_trading_day(market, d, *, align='error'|'previous'|'next') -> date`
  - `'error'`: 비거래일이면 `NonTradingDayError` raise.
  - `'previous'`/`'next'`: `calendar.previous_trading_day`/`next_trading_day` 재사용.
- `validate_date_range(market, start, end, prices_index, *, strict=True) -> None`
  - `expected = get_trading_days(market, start, end)` vs `prices_index` 차집합.
  - `strict=True`: 첫 결측일로 `MissingPriceError`.
  - `strict=False`: `logging.warning` 만, 첫 5건 샘플 + 추가 개수 표기.
- `align_to_trading_day(market, dates, *, direction='previous'|'next') -> DatetimeIndex`
  - 벡터화 구현: 세션 인덱스를 14일 패딩 후 `np.searchsorted`로 O(n log m) 매핑. 크기 보존, 원 순서 유지.
- `assert_universe_coverage(market_by_asset, prices, start, end) -> None`
  - 자산별로 해당 market의 거래일 vs 실제 non-NaN index를 비교.
  - 결측이 있는 **모든** 자산을 한 번에 수집해 메시지에 나열 후 `MissingPriceError` raise.
  - `prices.columns` 중 매핑에 없는 자산이 있으면 `KeyError` (silent 무시 방지).

## 구현 세부
- 모든 반환/비교 index는 tz-naive + midnight normalize (`_normalize_index`). `calendar.py`와 동일 규약.
- CRYPTO는 `is_trading_day`가 항상 True → `validate_trading_day` 조기 반환, `align_to_trading_day`도 365일 세션이라 사실상 passthrough.
- `align_to_trading_day`: 세션 배열을 `datetime64[ns]`로 변환 후 `searchsorted(side='right')-1` (previous) / `side='left'` (next). 경계에서 `np.clip`.
- docstring/logging/타입힌트 완비. `logging` 로거 이름 = 모듈 full path.

## 테스트
- 실행 결과: `pytest tests/test_calendar_guard.py -v` → **15 passed** (0.41s, Python 3.11.3, pytest-9.0.2).
- 커버한 시나리오:
  - 토요일 2024-01-06 (US): error / previous(2024-01-05 Fri) / next(2024-01-08 Mon) ✅
  - 거래일 passthrough ✅
  - 잘못된 align 모드 → ValueError ✅
  - US 2024-01 21 세션 중 하나 누락 → strict=True MissingPriceError (date 속성 일치) ✅
  - strict=False → warning 기록, 예외 없음 ✅
  - `align_to_trading_day` Fri/Sat/Sun/Mon → previous=[Fri,Fri,Fri,Mon], next=[Fri,Mon,Mon,Mon] ✅
  - 잘못된 direction → ValueError, 빈 입력 passthrough ✅
  - `assert_universe_coverage`: 완전 커버리지 통과, 복수 자산 결측 시 asset_id 다중 메시지 (asset 1,3 기재, 2 미기재) ✅
  - `market_by_asset` 누락 → KeyError ✅

## 파일
- `projects/stock-backtest/src/stock_backtest/backtest/calendar_guard.py` (신규)
- `projects/stock-backtest/tests/test_calendar_guard.py` (신규)

## 후속 제안 (별도 태스크 권장)
1. `repository.py`에서 OHLCV fetch 후 `validate_date_range` 호출 훅 추가 (조회 레이어 방어).
2. `backtest/engine.py` 데이터 로드 직후 `assert_universe_coverage` 호출.
3. `ingestion/pipeline.py`에서 소스 레코드 close=0/NaN 거부 로직 (수집 레이어 방어, architecture #13의 레이어 1).
