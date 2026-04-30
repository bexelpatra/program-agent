---
task_id: TASK-218
verdict: PASS
review_round: 2
---

# Reviewer Report: TASK-218 (ver 2 — 재검증)

## 검증 대상
- 파일: `signal/stock-backtest/task-board.md` L122 (TASK-218 행, 재작성됨), L124 (TASK-220 Depends On 변경), L128-130 (실행 순서 권고)
- Manager 주장: 직전 1차 review (`reviewer-report-TASK-218.md` ver 1) 의 NEEDS_REVISION 9건 모두 반영
- 추가 검증: 인용 라인 번호 (`client.ts:188/194/201`, `useBacktestPolling`, `ProgressPanel.tsx:89,139`) 실측 일치 + TASK-220 의 Depends On = TASK-218 추가

## 검증 결과

### 파일 존재 (1차에서 확인된 것 + 신규)
| 경로 | 존재 | 비고 |
|------|------|------|
| `frontend/app/backtests/new/page.tsx` | O | **539 lines** (`wc -l` 실측, 1차와 동일) — Manager 정정 일치 ✓ |
| `frontend/app/backtests/[run_id]/page.tsx` | O | 290 lines, 유지 명시됨 ✓ |
| `frontend/components/backtest/ProgressPanel.tsx` | O | 237 lines, L89/L139 router.push 위치 정확 ✓ |
| `frontend/lib/api/client.ts` | O | 248 lines |
| `frontend/hooks/useBacktestPolling.ts` | O | 113 lines, polling hook 존재 ✓ |
| `frontend/hooks/__tests__/` | X | **신규 디렉토리 — 태스크 #(d) 가 이를 생성하도록 지시함**. 태스크 의도와 일치 (작성 대상). |
| `frontend/hooks/useFormPersistence.ts` | X | **신규 — 태스크가 생성하도록 명시**. ✓ |
| `backend/tests/e2e/test_persona_first_use.py` | O | 존재 (수정 대상) ✓ |

### 9 항목 반영 검증 (Manager 주장 vs 실제 task-board)

| # | 1차 지적 | Manager 주장 | task-board L122 실측 | 반영 |
|---|----------|--------------|---------------------|------|
| 1 | 1071 → 539 정정 (실측) | 정정 완료 | "= **539 lines** (1071 은 commit 36d4684 의 +/-stat 합산)" — 출처까지 명시 | ✓ |
| 2 | ProgressPanel.tsx:89, 139 router.push 두 곳 제거 명시 | 추가 완료 | "③ **ProgressPanel.tsx:89, L139 `router.push('/backtests/{run_id}')` 두 곳 제거**" | ✓ |
| 3 | 기존 `/backtests/[run_id]/page.tsx` 유지 (이력 화면) | 사용자 결정 반영 | "**기존 `/backtests/[run_id]/page.tsx` (290 lines) 는 유지** — 이력에서 결과 다시 보기 진입 경로" + DoD (d) 회귀 0 | ✓ |
| 4 | localStorage 세부 (키/필드/직렬화/시점) | 모두 명시 | 키 `backtest:last_form_state:v1`, 9 필드 (universe_asset_ids 배열만 직렬화), 마운트 useEffect 복원, debounce 500ms 저장 | ✓ |
| 5 | sticky lg breakpoint 이상, 미만 stacked | 명시 | "① page.tsx 를 좌(폼, sticky lg breakpoint 이상) + 우(결과 패널) 2-column 으로. lg 미만은 stacked." | ✓ |
| 6 | useFormPersistence hook 분리 | 명시 | "④ 폼 값 localStorage 보존 — `useFormPersistence` hook 분리 (`frontend/hooks/useFormPersistence.ts`)" | ✓ |
| 7 | persona harness 갱신 + hook 단위 테스트 | 둘 다 명시 | "⑥ persona harness 테스트 갱신 ... useFormPersistence hook 단위 테스트 (`frontend/hooks/__tests__/useFormPersistence.test.ts`) — save/restore/version migration" | ✓ |
| 8 | 회귀 commit msg 가이드 | 추가 | "**commit msg 가이드**: 'TASK-218: 백테스트 인플레이스 결과 — ProgressPanel router.push 제거 + useFormPersistence 추가 + 좌+우 레이아웃'" | ✓ |
| 9 | 1071 → 정정 (= #1 중복) | 동일 처리 | (#1 과 동일) | ✓ |

### 추가 검증 — 인용 라인 번호 실측
- **`client.ts:188` (`getBacktest`)**: 실측 L188-189 `getBacktest: (runId: number) => fetchAndValidate(...)` ✓
- **`client.ts:194` (`getBacktestResult`)**: 실측 L194-195 `getBacktestResult: (runId: number) => fetchAndValidate(...)` ✓
- **`client.ts:201` (`cancelBacktest`)**: 실측 L201 `cancelBacktest: async (runId: number): Promise<void>` ✓
- **`useBacktestPolling`**: `frontend/hooks/useBacktestPolling.ts` 존재 (113 lines) ✓
- **`ProgressPanel.tsx:89`**: 실측 L89 `router.push(\`/backtests/${runId}\`);` (useEffect 안 setTimeout 콜백) ✓
- **`ProgressPanel.tsx:139`**: 실측 L139 `onClick={() => router.push(\`/backtests/${run.run_id}\`)}` (seeResult 버튼) ✓
- `grep router.push` 결과 ProgressPanel 내 정확히 2곳 (L89, L139) — 다른 곳 없음 ✓
- `useRouter` import L24, 인스턴스화 L81 — 제거 시 함께 제거 가능 (Manager 가 명시하지 않았으나 자명)

### 추가 검증 — TASK-220 Depends On 변경
- **task-board L124 (TASK-220) Depends On 컬럼**: 실측 `TASK-218` ✓ (1차 review 시 `-` 였음)
- **L128 권고**: "**TASK-218 (page.tsx 대규모 재구성)** 과 **TASK-220 (page.tsx REBALANCE_OPTIONS 한 줄 추가)** 가 같은 파일 수정 → **순차 진행**: 218 DONE 후 220 시작 (TASK-220 Depends On = TASK-218)" — 일관 ✓
- **L130**: "진행 순서: (218 ∥ 219) → 220" — 219 는 frontend 변경 0 이므로 page.tsx 충돌 없음, 218 과 병렬 안전. 220 만 순차. ✓

### 태스크 완결성
- DoD 4개 (a/b/c/d) 측정 가능. (d) 가 1차 review 의 "기존 결과 화면 회귀 0" 을 명시적으로 박제 ✓
- 자동 회귀 테스트 2종 (persona harness e2e + useFormPersistence 단위) 명시 ✓
- 회귀 의도 commit msg 가이드 1차 누락 → ver 2 보완 ✓
- 인용 모든 라인 번호 실측 일치 ✓

### 의존성·순서
- TASK-218 의 Depends On = `-` (선행 없음, 정확) ✓
- TASK-220 의 Depends On = TASK-218 (page.tsx 동일 파일 수정) ✓
- TASK-219 는 218/220 과 파일 교집합 0 (allocators/* + services/* + api/*) — 218 과 병렬 안전 ✓

### 목적성·클린 아키텍처·분리 원칙
- **목적성** ✓: "사용자 의도 정합성" 발견 (1) 직접 해결.
- **클린 아키텍처** ✓: presentation/hooks 만 수정. domain/data 미접근.
- **소스·함수 분리** ✓ (1차 △ 해소): localStorage 로직이 `useFormPersistence` 별도 hook 으로 분리되도록 명시. page.tsx 비대화 방지.
- **이름·인터페이스** ✓: `backtest:last_form_state:v1` 버전 키 포함, 9 필드 명시.
- **추후 수정 용이성** ✓ (1차 △ 부분 해소): ProgressPanel 의 router.push 두 곳 제거 명시. 단 1차 권장한 `onComplete?: callback` 패턴 (호출자 위임) 은 채택되지 않고 단순 제거 — 이력 진입 경로는 별도 (앱 메인 이력 카드) 라고 분리 명시함으로써 ProgressPanel 의 책임을 "진행률·결과 알림 표시" 로 단순화. **수용 가능** — 미래에 다른 진입점 추가 시 그때 callback 패턴 재도입 가능 (점진적 진화). v0 단순성 우선 결정으로 인정.

## 판정
**PASS**

## 수정 요청 (NEEDS_REVISION 시)
없음.

## Manager 에게 전달

1차 review 의 NEEDS_REVISION 9건 모두 반영 확인. 인용 라인 번호도 실측과 일치. TASK-220 의 Depends On 갱신 + 실행 순서 권고 일관성도 확인.

**다음 단계 (권고)**:
- TASK-218 과 TASK-219 는 파일 충돌 없음 — Coder 2 병렬 호출 가능. report 파일은 `coder-report-TASK-218.md`, `coder-report-TASK-219.md` 로 분리.
- TASK-220 은 TASK-218 DONE 직후 시작 (page.tsx 동일 파일 수정).
- 사용자 의도 정합성 섹션 진행 중 마일스톤 재검증: TASK-218 + TASK-219 둘 다 Coder DONE 후, TASK-220 호출 직전에 Reviewer 재호출 1회 권장 (page.tsx 의 새로운 구조 위에 REBALANCE_OPTIONS 한 줄 추가가 정확한 위치를 가리키는지 확인).

**경미한 관찰 (NEEDS_REVISION 사유 아님, FYI)**:
- ProgressPanel.tsx 에서 router.push 두 줄을 제거하면 `useRouter()` (L81) 와 `import { useRouter } from "next/navigation"` (L24) 가 unused 가 됨. Coder 가 자명하게 함께 제거할 것으로 기대하나, 불안하면 description 에 "단 useRouter import + 인스턴스화도 함께 제거 (unused)" 한 줄 추가 가능. 누락해도 lint/typecheck 에서 잡혀 회귀 위험 미미.
