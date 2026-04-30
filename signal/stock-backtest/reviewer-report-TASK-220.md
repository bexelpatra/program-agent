---
task_id: TASK-220
verdict: PASS
review_round: 2
---

# Reviewer Report: TASK-220 (ver 2)

## 검증 대상

- **Manager 산출물 (재작성)**: `signal/stock-backtest/task-board.md` L124 (TASK-220 행)
- **실행 순서 권고 갱신**: task-board.md L126-131 (Reviewer 1차 NEEDS_REVISION 반영 섹션)
- **사용자 결정 (2026-04-30)**: semi_annual = **1월·7월 첫 거래일** trigger (quarterly 와 의미론 일관)
- **재검증 코드**:
  - `backend/app/domain/strategy.py:34-41` (RebalanceSchedule Literal)
  - `backend/app/schemas/backtest.py:29-36` (HTTP DTO Literal)
  - `backend/app/domain/engine.py:109-141` (`_is_rebalance_day`)
  - `frontend/lib/api/schemas.ts:149-156` (Zod RebalanceScheduleEnum)
  - `frontend/app/backtests/new/page.tsx:74-80` (REBALANCE_OPTIONS) + `L507-521` (드롭다운)
  - `frontend/lib/i18n/ko.ts` (rebalance 키 부재 재확인)
  - `backend/tests/domain/test_engine.py` (`_is_rebalance_day` 테스트 부재 재확인)

## 1차 NEEDS_REVISION 5건 + 사용자 결정 1건 반영 검증

| # | 1차 지적 | Manager 반영 결과 (재작성된 L124 / L126-131) | 반영 |
|---|----------|---------------------------------------------|------|
| 0 | 사용자 결정: semi_annual 의미론 (1/1·7/1 vs 6/30·12/31) | "사용자 결정 (2026-04-30): semi_annual = **1월·7월 첫 거래일** trigger (quarterly 와 의미론 일관)" 명시 | OK |
| 1 | engine.py 분기 로직 명시 (quarterly 와 일관) | "engine.py:133-136 quarterly 분기 = `(d.month-1)//3` 변경 검사 → **분기 시작 첫 거래일** (1/1, 4/1, 7/1, 10/1) trigger (3/31·6/30 분기말 아님). … quarterly 분기와 같은 패턴으로 semi_annual 분기 추가 — `if schedule == "semi_annual": return prev_d is None or (d.month - 1) // 6 != (prev_d.month - 1) // 6 or d.year != prev_d.year`" | OK |
| 2 | 휴일 보정 로직 제거 | "휴일 보정 로직 추가하지 않음 — `_is_rebalance_day` 는 이미 거래일만 받음 (`trading_days_in_period` 결과)" | OK |
| 3 | 한글 라벨 위치 정정 (StrategyParamsForm/ko.ts → page.tsx inline) | "한글 라벨 위치: `app/backtests/new/page.tsx:74-80` `REBALANCE_OPTIONS` inline 상수 + `L507-521` 드롭다운. `lib/i18n/ko.ts` 에 `rebalance.*` namespace **0 hit** (전수 grep) — 다른 옵션도 inline 한글, 일관성 위해 inline 한 줄 추가." + 수정 단계 ⑤ "`app/backtests/new/page.tsx:74-80` `REBALANCE_OPTIONS` 에 `{ value: "semi_annual", label: "반기" }` 한 줄 추가 (i18n/ko.ts 갱신 X)" | OK |
| 4 | 단위 테스트 케이스 변경 (휴일 보정 제거, 분기 시작 케이스로 교체) | "`tests/domain/test_engine.py` (현재 `_is_rebalance_day` 테스트 부재 확인됨) 신규: (a) 1월 첫 거래일 trigger, (b) 7월 첫 거래일 trigger, (c) 다른 월 false, (d) 동일 분기 두 번째 호출 false. **휴일 보정 케이스 제거** (calendar 가 처리)." | OK |
| 5 | TASK-218 과 page.tsx 동시 수정 → 병렬 금지 / Depends On 추가 | Depends On = **TASK-218** 명시. L126-131 "실행 순서 권고": "**TASK-218 (page.tsx 대규모 재구성)** 과 **TASK-220 (page.tsx REBALANCE_OPTIONS 한 줄 추가)** 가 같은 파일 수정 → **순차 진행**: 218 DONE 후 220 시작 (TASK-220 Depends On = TASK-218). … 진행 순서: (218 ∥ 219) → 220." | OK |

→ 1차 5건 + 사용자 결정 1건 모두 반영 완료.

## 추가 검증 (Manager 재요청 3 항목)

### A. Manager 인용 라인 실제 일치 검증

| 인용 라인 | 실측 (Read 결과) | 일치 |
|-----------|----------------|------|
| `engine.py:133-136` quarterly 분기 = `(d.month-1)//3` | L133-136 정확:<br>```python\nif schedule == "quarterly":\n    prev_q = (prev_d.month - 1) // 3\n    cur_q = (d.month - 1) // 3\n    return cur_q != prev_q or d.year != prev_d.year\n``` | OK |
| `engine.py:109-141` `_is_rebalance_day` 시그니처 | L109-141 정확. L123 `if prev_d is None: return True` (Manager 가 인용한 `prev_d is None or …` 패턴과 부합 — 함수 입구에서 별도 처리). | OK (의미 동등) |
| `app/backtests/new/page.tsx:74-80` `REBALANCE_OPTIONS` inline | L74-80 정확히 5 옵션 inline 상수 (`signal_event` 미노출). | OK |
| `app/backtests/new/page.tsx:L507-521` 드롭다운 | L506-521 `<Label>리밸런싱 주기</Label>` + `<Select id="rebalance" value={rebalanceSchedule} … REBALANCE_OPTIONS.map(…)` 정확. | OK |
| `frontend/lib/api/schemas.ts:149-156` Zod RebalanceScheduleEnum | L149-156 정확히 6 값 (`signal_event` 포함). 한 줄 추가 가능. | OK |
| `strategy.py:34-41` Literal 6 값 | L34-41 정확. | OK |
| `schemas/backtest.py:29-36` Literal 동기 | L29-36 정확. | OK |
| `lib/i18n/ko.ts` rebalance 0 hit | grep 결과 0 hit 재확인. inline 패턴이 정합. | OK |
| `tests/domain/test_engine.py` `_is_rebalance_day` 테스트 부재 | grep `_is_rebalance_day\|is_rebalance` 0 hit 재확인. | OK |

### B. semi_annual 분기 로직 일관성 검증

quarterly (engine.py L133-136):
```python
prev_q = (prev_d.month - 1) // 3
cur_q  = (d.month - 1) // 3
return cur_q != prev_q or d.year != prev_d.year
```

Manager 가 task-board.md 에 명시한 semi_annual:
```python
if schedule == "semi_annual":
    return prev_d is None or (d.month - 1) // 6 != (prev_d.month - 1) // 6 or d.year != prev_d.year
```

검증:
- `(d.month-1)//6` 매핑: 1~6월 → 0, 7~12월 → 1. 정확.
- transition 검증:
  - 6/30 → 7/1: prev_h=0, cur_h=1 → True. 7월 첫 거래일 trigger.
  - 12/30 → 1/2 (다음 해): prev_h=1, cur_h=0, year 변경 → True. 1월 첫 거래일 trigger.
  - 4/30 → 5/1: prev_h=0, cur_h=0, year 동일 → False. (의도 — 5월은 trigger 아님)
  - 7/2 → 7/3: prev_h=1, cur_h=1, year 동일 → False. (의도 — 같은 후반기 내)
- quarterly 와 동일 패러다임 (`(month-1)//N` index 변경 검사). **일관성 OK**.
- 첫날 처리: `prev_d is None` 분기를 함수 입구 (engine.py:123) 가 이미 처리하므로, semi_annual 의 `prev_d is None or …` 형태도 동일 동작. **두 표현 모두 정상**. (Manager 가 설명력 위해 `prev_d is None or …` 를 명시한 것은 OK — Coder 는 입구 가드를 활용해도 무방.)

### C. 단위 테스트 import 범위 검증

질문: "`_is_rebalance_day(d, prev_d, "semi_annual")` 호출만으로 충분한지 (engine 전체 import 필요한지)."

검증 (engine.py 헤드 부분 + L109-141 Read 결과):
- `_is_rebalance_day` 는 engine.py 모듈 레벨 함수 (class method 아님).
- 의존성: `date` (stdlib), `RebalanceSchedule` (Literal — runtime 검사 없음, 단순 string).
- 다른 engine 함수/클래스 (Portfolio, prices_aligned, fills 등) 와 독립.
- import 라인: `from app.domain.engine import _is_rebalance_day` + `from datetime import date` 만으로 충분.
- pytest fixture 불필요 (DB / source 의존성 없음).

→ 단위 테스트는 **engine 전체 import 불필요**. `_is_rebalance_day` 단일 import 로 4 케이스 (1월 첫 거래일 / 7월 첫 거래일 / 다른 월 false / 동일 분기 두 번째 호출 false) 모두 검증 가능. Manager 의 description ⑥ 4 케이스 그대로 OK.

### D. 부수 검증 (실행 순서)

- TASK-220 Depends On = TASK-218 명시 → page.tsx 충돌 회피 OK.
- TASK-219 는 page.tsx 만지지 않음 (allocators/ + services/ + api/ 만 — task-board L123 ③ 참조). TASK-218 ∥ 219 병렬 안전.
- (218 ∥ 219) → 220 순서 정합.

### E. 1차 review 후 신규 식별 위험 — **없음**

- description 의 모든 인용 라인이 실측과 일치.
- 휴일 보정이 사라져 잘못된 테스트 케이스 위험 제거.
- semi_annual 분기 로직이 quarterly 와 동일 패러다임 → 모듈 내 일관성 유지.
- 한글 라벨이 inline (다른 옵션과 동일 패턴) → i18n 리팩토링 부채 미발생.

## 판정

**PASS**

1차 NEEDS_REVISION 5건 + 사용자 결정 1건 모두 반영 완료. 인용 라인 실측 일치, 분기 로직 quarterly 와 일관, 단위 테스트 4 케이스 독립 import 로 실행 가능. Manager 는 Coder 호출 가능.

## Manager 에게 전달

- TASK-220 은 TASK-218 DONE 후 시작 (Depends On 명시됨).
- 진행 순서: (TASK-218 ∥ TASK-219) → TASK-220.
- Coder 호출 시 description (task-board.md L124) 그대로 전달하면 충분 — 분기 로직·단위 테스트 케이스·라인 번호 모두 명시되어 있음.
- 권장: TASK-220 commit 후 e2e 검증 (10년 백테스트, 약 20회 trade, month ∈ {1,7}) 을 Manager 가 직접 또는 Tester 위임으로 1회 수행. (현 description DoD c 항목과 일치.)
- 별도 ESCALATE 필요 사항 없음.
