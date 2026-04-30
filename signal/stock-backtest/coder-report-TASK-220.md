---
agent: coder
task_id: TASK-220
status: DONE
timestamp: 2026-04-30T12:00:00
---

## 결과 요약

`RebalanceSchedule` 에 `semi_annual` (반기) 추가 완료. 사용자 결정대로 **1월·7월 첫 거래일** trigger (quarterly 와 의미론 일관, `(month-1)//6` 패턴). 휴일 보정 로직은 추가하지 않음 — `_is_rebalance_day` 는 이미 거래일만 받기 때문 (`trading_days_in_period` 결과).

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/strategy.py` (수정) — Literal 6→7 값. `semi_annual` 주석으로 의미 명시.
- `projects/stock-backtest/backend/app/schemas/backtest.py` (수정) — Literal 6→7 값 동기.
- `projects/stock-backtest/backend/app/domain/engine.py` (수정) — `_is_rebalance_day` 에 semi_annual 분기 추가 (`(d.month-1)//6` 패턴, quarterly 분기 바로 아래). 함수 docstring 의 schedule 설명 갱신.
- `projects/stock-backtest/frontend/lib/api/schemas.ts` (수정) — Zod enum 6→7 값.
- `projects/stock-backtest/frontend/app/backtests/new/page.tsx` (수정) — `REBALANCE_OPTIONS` (현재 L74-81, 라인 변동 없음) 에 `{ value: "semi_annual", label: "반기" }` quarterly 와 yearly 사이 1줄 추가.
- `projects/stock-backtest/backend/tests/domain/test_engine.py` (수정) — `TestIsRebalanceDaySemiAnnual` 클래스 4 케이스 신규 추가 (파일 끝). Manager 의 task description 이 명시적으로 "단위 테스트 4 케이스 신규" 를 Coder 에게 지시했으므로 coder.md L188 ("tests/ 수정 금지") 보다 명시적 task spec 우선.

## 핵심 결정

1. **함수 호출 후 분기 (early return) 패턴 — 기존 quarterly 와 동일 구조**: `prev_h = (prev_d.month - 1) // 6; cur_h = (d.month - 1) // 6; return cur_h != prev_h or d.year != prev_d.year`. half=0 (1~6월), half=1 (7~12월).
2. **휴일 보정 X**: task description 명시 — calendar 가 이미 거래일만 통과시킴. `_is_rebalance_day` 시그니처는 변경하지 않음.
3. **테스트 파일 수정의 정당성**: agents/coder.md L188 "tests/ 디렉토리 수정 금지 (Tester 전용)" 와 task description 의 "단위 테스트 4 케이스 신규: ... `tests/domain/test_engine.py`" 가 충돌. Manager 의 task spec 이 더 명시적 + DoD (a) 가 단위 테스트 통과를 요구 → spec 우선 적용. Reviewer 가 분리를 요구하면 후속 태스크로 Tester 에게 이관 가능.
4. **frontend i18n 처리 일관성**: `lib/i18n/ko.ts` 의 `rebalance.*` namespace 가 0 hit (전수 grep 확인) — 다른 옵션도 inline 한글이라서 inline 한 줄 추가로 일관성 유지.

## DoD 검증 결과

- (a) **단위 테스트 4 케이스 통과**: `pytest tests/domain/test_engine.py -v` 실행 결과 9/9 PASSED (기존 5 + 신규 4). 회귀 0.
  - `test_january_first_trading_day_triggers` PASSED
  - `test_july_first_trading_day_triggers` PASSED
  - `test_other_month_within_same_half_returns_false` PASSED (3 sub-assert: H1 내부 / H2 내부 / 1→2월)
  - `test_within_same_half_repeated_call_false` PASSED (2 sub-assert: 1/2→1/3, 1/2→6/30)
- (b) **`npm run build` 성공**: Zod enum 7 값 포함 + 컴파일 통과. `/backtests/new` route 9.23 kB (정적 prerender). 타입 체크 통과.
- (c) **10년 백테스트 실측은 Manager 가 수동 검증** (task description 위임 명시). 단위 테스트로 1월·7월 trigger 동작 + 같은 반기 내 false 검증 완료 → 이론적으로 10년 시 trades 가 1·7월 부근만 발생.

## 이슈/블로커

없음.

### 후속 발견 사항 (참고)

- `backend/app/schemas/backtest.py:29-37` Literal 정의가 `app/domain/strategy.py` 와 **수동 동기**다. 추후 한 곳에서 다른 곳으로 import 하거나 (예: `from app.domain.strategy import RebalanceSchedule`) ENUM 단일 출처 정공법을 검토할 만함. 현재 V3 MVP 범위 외라 변경하지 않음.
- TASK-221 (test_api_contract len==4 갱신) 은 RebalanceSchedule 스키마 길이를 검증하는 테스트일 가능성 — 7 값으로 갱신 필요. Manager 가 Tester 에게 분리 할당 예정이므로 본 태스크에서는 손대지 않음.
- 이미 production DB 에 저장된 backtest_runs 의 strategy JSON 에 `rebalance_schedule` 값이 있다면, semi_annual 추가는 backward-compatible (Literal 확장만, 기존 6 값 그대로 유효). 마이그레이션 불필요.

## 다음 제안

Manager 가 Reviewer 에게 본 보고서 검증 요청 → PASS 시 task-board 에서 TASK-220 DONE 처리. TASK-221 (Tester) 호출 시 본 변경 사항 (Literal 7 값) 을 참조 자료로 전달 권장.
