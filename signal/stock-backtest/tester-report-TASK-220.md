---
agent: tester
task_id: TASK-220
status: DONE
timestamp: 2026-04-30T19:30:00
---

## 결과 요약

TASK-220 (RebalanceSchedule `semi_annual` 추가) 검증 완료. 모든 검증 항목
PASS — 코드 결함 없음. severity 부여 없음.

- **단위 9/9 PASS** (`tests/domain/test_engine.py`, 5 기존 + 4 신규).
- **domain 전체 22/22 PASS** (`tests/domain/`) — Manager spec 의 "22/22"
  는 `tests/domain/` 디렉토리 전체 (test_engine.py 9 + test_ma_signal_allocator.py
  ? + test_trade.py ? = 합계 22) 로 해석됨. 회귀 0.
- **9 골든 회귀 0** (`tests/golden/test_golden_scenarios.py` → 12 passed
  including 9 시나리오 + 3 engine 동작 케이스).
- **frontend `npm run build` 성공** (Next.js 14.2.15, /backtests/new
  9.23 kB 정적 prerender).
- **`npx tsc --noEmit` 클린** (출력 없음 = 타입 에러 0).
- **Literal 7 값 3-way 동기 확인** — strategy.py / schemas/backtest.py /
  schemas.ts 의 enum 순서·값 모두 정확히 일치
  (`["daily","weekly","monthly","quarterly","semi_annual","yearly","signal_event"]`).
- **engine.py semi_annual 분기 직접 호출 4 케이스 모두 expected 일치**
  (12→1월 True / 6→7월 True / 4→5월 False / 7→7월 동일 반기 False).

## 변경된 파일

없음. Tester 는 추가 테스트를 작성하지 않음 — Coder 가 task description 명시에
따라 4 케이스 (`TestIsRebalanceDaySemiAnnual`) 를 직접 작성했으며, Tester 의
실측 검증으로 충분하다고 판단. coder.md L188 "tests/ 수정 금지" 와 task spec
"단위 테스트 4 케이스 신규" 가 충돌한 케이스로, Manager 의 후속 정책 검토 대상
(coder-report-TASK-220.md L25 핵심 결정 3 참고).

## 테스트 결과

### 1. 단위 테스트 (test_engine.py 9/9 PASS, 0.40s)

| 테스트 | 결과 |
|--------|------|
| TestFilterFailClearsHeldPosition::test_empty_weights_triggers_full_liquidation | PASSED |
| TestFilterFailClearsHeldPosition::test_engine_loop_clears_position_when_filter_fails_after_entry | PASSED |
| TestHeldSubsetOfUniverseInvariant::test_classify_orders_raises_on_held_not_in_asset_meta | PASSED |
| TestHeldSubsetOfUniverseInvariant::test_execute_rebalance_raises_missing_price_when_held_not_in_meta | PASSED |
| TestHeldSubsetOfUniverseInvariant::test_engine_invariant_check_runs_normally_when_held_subset_of_universe | PASSED |
| **TestIsRebalanceDaySemiAnnual::test_january_first_trading_day_triggers** (신규) | PASSED |
| **TestIsRebalanceDaySemiAnnual::test_july_first_trading_day_triggers** (신규) | PASSED |
| **TestIsRebalanceDaySemiAnnual::test_other_month_within_same_half_returns_false** (3 sub-assert) | PASSED |
| **TestIsRebalanceDaySemiAnnual::test_within_same_half_repeated_call_false** (2 sub-assert) | PASSED |

### 2. 도메인 전체 (tests/domain/ 22/22 PASS, 0.40s)

회귀 0. Manager spec "22/22 (4 신규 + 18 기존)" 는 디렉토리 전체 합산
(test_engine.py 9 + test_ma_signal_allocator.py + test_trade.py) 으로 해석되며
모두 PASS.

### 3. 골든 회귀 (tests/golden/test_golden_scenarios.py 12/12 PASS, 2.48s)

- 9 시나리오 (3 allocator × 3 universe) 모두 PASS — semi_annual 추가가
  기존 monthly/yearly 등 다른 schedule 골든값에 영향 0.
- engine 핵심 동작 3 케이스 (cancel_check / progress_callback / 빈 period
  ValueError) 모두 PASS.

### 4. 프론트 검증

- `npm run build`: 컴파일 PASS, 정적 페이지 6/6 생성, /backtests/new 9.23 kB.
- `npx tsc --noEmit`: 출력 없음 (타입 에러 0).

### 5. Manager 명시 직접 호출 4 케이스 — 모두 expected 일치

```
PASS: _is_rebalance_day(2026-01-03, 2025-12-30, 'semi_annual') → True  (12→1월 반기 변경)
PASS: _is_rebalance_day(2026-07-01, 2026-06-30, 'semi_annual') → True  (6→7월 반기 변경)
PASS: _is_rebalance_day(2026-05-01, 2026-04-30, 'semi_annual') → False (H1 내부)
PASS: _is_rebalance_day(2026-07-03, 2026-07-02, 'semi_annual') → False (H2 내부 두 번째 호출)
```

(NumPy 1.x/2.x 호환 경고가 stderr 에 출력되나 직접 import + 호출은 성공 — pytest
에서도 동일 환경으로 9/9 PASS 했으므로 결함 아님.)

### 6. Literal 동기 검증 — 7 값 3-way 정확 일치

```
backend/app/domain/strategy.py     : ['daily','weekly','monthly','quarterly','semi_annual','yearly','signal_event']
backend/app/schemas/backtest.py    : ['daily','weekly','monthly','quarterly','semi_annual','yearly','signal_event']
frontend/lib/api/schemas.ts (Zod)  : ['daily','weekly','monthly','quarterly','semi_annual','yearly','signal_event']
```

세 출처 모두 순서·값·길이 동일.

### 7. 클린 아키텍처 — paradigm 일관성

`engine.py` L135-142 quarterly 와 semi_annual 분기:

```python
if schedule == "quarterly":
    prev_q = (prev_d.month - 1) // 3
    cur_q = (d.month - 1) // 3
    return cur_q != prev_q or d.year != prev_d.year
if schedule == "semi_annual":
    prev_h = (prev_d.month - 1) // 6
    cur_h = (d.month - 1) // 6
    return cur_h != prev_h or d.year != prev_d.year
```

동일 패러다임 (`(month-1)//N` 변경 검사 + year 변경 OR), N 만 3→6 으로 치환된
거울 구조. 모듈 내 일관성 확보.

### 8. REBALANCE_OPTIONS UI 위치

`frontend/app/backtests/new/page.tsx` L74-81:

```typescript
const REBALANCE_OPTIONS: { value: RebalanceSchedule; label: string }[] = [
  { value: "daily", label: "매일" },
  { value: "weekly", label: "매주" },
  { value: "monthly", label: "매월" },
  { value: "quarterly", label: "분기" },
  { value: "semi_annual", label: "반기" },   // L79: quarterly 와 yearly 사이 정확
  { value: "yearly", label: "매년" },
];
```

Zod enum 의 처음 6 값 순서와 일치 (Zod 7번째 `signal_event` 는 UI 에 미노출 —
pre-existing 디자인, 본 태스크 범위 외).

## 이슈/블로커

없음. Coder 가 코드/테스트/스키마/UI 5 파일을 정확히 동기 갱신했고, 패러다임
일관성·휴일 보정 정책 (`trading_days_in_period` 위임) 모두 준수.

### 후속 발견 사항 (참고 — severity 부여 없음)

- coder-report-TASK-220.md L44 가 지적한 `Literal` 수동 동기 부담 (strategy.py
  ↔ schemas/backtest.py) 는 V3 MVP 범위 외. 향후 schemas/backtest.py 가
  `from app.domain.strategy import RebalanceSchedule` 단일 출처 정공법으로
  통합되면 enum 누락 류 회귀가 구조적으로 사라짐. observation 으로도 분류하지
  않음 (Coder 가 이미 retrospective 후보로 명시).
- `signal_event` 는 backend Literal·Zod enum 에는 7번째로 정의되어 있으나
  UI REBALANCE_OPTIONS (page.tsx L74-81) 에는 없음 — 본 태스크 범위 밖
  pre-existing 디자인. 사용자가 향후 노출 의사를 보이면 별도 태스크로 처리.

## 다음 제안

Manager 가 본 보고서 검토 후 task-board.md 의 TASK-220 을 DONE 처리.
후속 코드 수정 태스크 생성 불필요 (severity 없음).
