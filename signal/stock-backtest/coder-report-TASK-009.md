# Coder Report — TASK-009

## 상태
**DONE**

## 개요
- Task: 거래일 캘린더 모듈 (KRX, NYSE, Crypto 365일, 공통 기간 교집합)
- 파일: `projects/stock-backtest/src/stock_backtest/backtest/calendar.py`

## 구현 요약

### 공개 API
- `MarketNotSupportedError(Exception)` — 알 수 없는 market 코드
- `get_trading_days(market, start, end) -> pd.DatetimeIndex`
- `is_trading_day(market, d) -> bool`
- `previous_trading_day(market, d) -> date` (d가 거래일이면 d 그대로)
- `next_trading_day(market, d) -> date` (d가 거래일이면 d 그대로)
- `common_trading_days(markets, start, end) -> pd.DatetimeIndex` (교집합, MIXED 모드용)
- `union_trading_days(markets, start, end) -> pd.DatetimeIndex` (합집합, 참고용)

### Market 코드 매핑
- `KR`/`KRX`/`KOSPI`/`KOSDAQ`/`XKRX` → `XKRX`
- `US`/`NYSE`/`NASDAQ`/`XNYS` → `XNYS`
- `CRYPTO` → 365일 연속 (`pd.date_range(..., freq='D')`)
- 그 외는 `MarketNotSupportedError`

### 설계 포인트
- `_get_calendar(code)`는 `functools.lru_cache(maxsize=8)`으로 래핑하여 ExchangeCalendar 객체 재사용.
- `CRYPTO`는 exchange_calendars 밖에서 직접 처리(모든 일자가 거래일, `is_trading_day`는 항상 True, `previous/next_trading_day`는 `d` 그대로).
- 반환 인덱스는 모두 **tz-naive**로 정규화(`_normalize_index`)하여 docstring에 명시.
- `previous_trading_day` / `next_trading_day`는 `ExchangeCalendar.date_to_session(ts, direction=...)` 사용 (입력이 세션이 아니어도 동작). 구 API 호환 fallback 포함.
- 입력은 `datetime.date | datetime | pd.Timestamp | str` 모두 수용(`_to_date` 헬퍼).
- 타입 힌트 + docstring 완비, `__all__` 선언.

### 의존성
- `exchange_calendars` (requirements.txt에 이미 포함).
- 설치 중 numpy 2.4.4로 자동 업그레이드되어 pandas ABI 불일치 발생 → `numpy<2`로 재설치하여 해결. 현재 numpy 1.26.4, exchange_calendars 4.13.2.

## 검증 결과 (2024-01 기준)

| 항목 | 값 | 비고 |
|------|----|------|
| US(XNYS) Jan 2024 거래일 | **21** | 1/1 New Year's Day, 1/15 MLK Day 2회 휴장 → 31 - 8(주말) - 2 = 21 ✅ |
| KR(XKRX) Jan 2024 거래일 | 22 | 1/1 신정 휴장, 설연휴는 2월이므로 22일 |
| CRYPTO Jan 2024 | 31 | 매일 거래일 |
| KR∪US 합집합 | 22 | |
| KR∩US 교집합 | **21** | 단순 합계(43)보다 현저히 적음 → 교집합 로직 정상 ✅ |
| KOSPI alias Jan | 22 | XKRX로 정상 매핑 |
| NASDAQ alias Jan | 21 | XNYS로 정상 매핑 |
| `is_trading_day('US', 2024-01-01)` | False | 신년 휴장 |
| `is_trading_day('US', 2024-01-02)` | True | |
| `is_trading_day('CRYPTO', 2024-01-06 Sat)` | True | |
| `previous_trading_day('US', 2024-01-01)` | 2023-12-29 | 직전 금요일 |
| `next_trading_day('US', 2024-01-01)` | 2024-01-02 | |
| `previous_trading_day('US', 2024-01-03)` | 2024-01-03 | 본인 거래일 |
| 인덱스 tz / dtype | None / datetime64[ns] | tz-naive 확인 |
| Unknown market 'JP' | `MarketNotSupportedError` raise ✅ | |

## 완료 조건 체크
- [x] `python -c "from stock_backtest.backtest.calendar import get_trading_days, common_trading_days; import datetime as dt; print(len(get_trading_days('US', dt.date(2024,1,1), dt.date(2024,1,31))))"` → **21** 출력.
- [x] US 2024-01 거래일 수 21 (라이브러리 기준 합리적 값) 보고.
- [x] KR∩US = 21, KR∪US = 22, 단순 합계 43보다 적음 확인.
- [x] `exchange_calendars` 캐시(lru_cache)로 재사용.
- [x] tz-naive Timestamp 반환 확인.
- [x] 타입 힌트, docstring, `MarketNotSupportedError` 정의 완료.

## 수정/생성 파일
- `projects/stock-backtest/src/stock_backtest/backtest/calendar.py` (신규)

## 금지 사항 준수
- `task-board.md`, `architecture.md`, `tests/`, `ingestion/` 미수정.
