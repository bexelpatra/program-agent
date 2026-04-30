---
agent: coder
task_id: TASK-233
status: DONE
timestamp: 2026-04-30T18:00:00
---

## 결과 요약

`pipeline.py` 가 `calendar_guard` 의 사적 심볼 `_MARKET_CALENDARS` 를 직접 import 하던 것을 정리했다.

- `app/domain/asset/calendar_guard.py` 에 신규 public 함수 `get_calendar_name(market: str) -> str | None` 추가.
  - **unknown market 일 때 raise 하지 않고 `None` 반환** — `_trading_days` 의 `dict.get()` graceful fallback 의도를 그대로 보존.
  - 기존 `_resolve_calendar_name` (ValueError raise) 은 변경 없이 유지. 단순 public 승격이 아니라 별도 정의.
  - `_MARKET_CALENDARS` 자체는 모듈 내부 상수로 유지 (외부 노출 없음).
- `app/data/pipeline.py:29` import 변경: `from app.domain.asset.calendar_guard import get_calendar_name`.
- `app/data/pipeline.py:67` 호출 변경: `cal_name = get_calendar_name(market)`.
- 단위 테스트 신규 작성: `backend/tests/domain/test_calendar_guard.py` — 6 케이스 (KR/US/CRYPTO + UNKNOWN/빈문자열/소문자 변형).

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/asset/calendar_guard.py` (수정 — `get_calendar_name` 추가)
- `projects/stock-backtest/backend/app/data/pipeline.py` (수정 — import + 호출처 2 곳)
- `projects/stock-backtest/backend/tests/domain/test_calendar_guard.py` (신규 — 6 단위 테스트)

### Public API 변경

- 신규: `app.domain.asset.calendar_guard.get_calendar_name(market: str) -> str | None`
  - unknown market 시 `None` 반환 (raise 없음)
  - 기존 `_resolve_calendar_name` (raise 정책) 과 의도적으로 정책이 다름 — 호출자가 graceful 인지 strict 인지에 따라 선택

## DoD 충족 검증

| 항목 | 결과 |
|------|------|
| `grep "_MARKET_CALENDARS" backend/app/data/pipeline.py` 0 hit | OK (0 hit 실측) |
| `grep "_MARKET_CALENDARS" backend/app/domain/asset/calendar_guard.py` 1+ hit | OK (5 hit 실측 — L24/L32/L33/L34/L49) |
| unknown market 시 `get_calendar_name("UNKNOWN") is None` 단위 테스트 | OK (`tests/domain/test_calendar_guard.py::TestGetCalendarNameUnknownMarket::test_unknown_market_returns_none` PASSED) |
| 기존 회귀 PASS | OK (data + domain + regression 96/96 PASSED, calendar 관련 29/29 PASSED) |

### 테스트 실행 결과

```
tests/domain/test_calendar_guard.py — 6/6 PASSED
tests/regression/test_calendar_defense.py — 23/23 PASSED
tests/data/ + tests/domain/ + tests/regression/ — 96/96 PASSED
```

회귀 실패는 발견되지 않았다. (참고: `tests/api/test_api_contract.py::test_api_contract_fuzz[GET /api/assets/{asset_id}]` 는 `asset_id=0 not found` 404 fuzz 실패가 있으나 calendar_guard 와 무관한 API 레이어 이슈로, 다른 병렬 Coder 변경의 영향 가능성. 본 태스크 범위 외.)

## 이슈/블로커

없음.

## 다음 제안

1. **(범위 외) `_resolve_calendar_name` 재사용 검토**: 현재 calendar_guard 내부에 `_resolve_calendar_name` (raise) 과 신규 `get_calendar_name` (None) 두 개의 유사 함수가 공존한다. 정책 차이가 명확하므로 둘 다 유지하는 것이 클린하지만, 추후 사용처가 늘면 명명 규칙 (`*_strict` / `*_graceful`) 통일을 검토할 수 있다. 현재는 변경 불필요.
2. **(관찰) test_api_contract_fuzz 별도 태스크화 검토**: `GET /api/assets/{asset_id}` fuzz 가 `asset_id=0` 에서 404 를 반환하는 것이 contract 위반인지(스키마에 0 허용?) 다른 Coder 변경 부작용인지 Manager 가 판정 필요. 본 태스크 범위 외라 손대지 않음.
