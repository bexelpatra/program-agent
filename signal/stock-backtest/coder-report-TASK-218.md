---
agent: coder
task_id: TASK-218
status: DONE
timestamp: 2026-04-30T17:30:00
---

## 결과 요약

`/backtests/new` 화면을 좌(폼 sticky) + 우(진행률/결과) 2-column 레이아웃으로
재구성하고, 백테스트 실행 후 URL 변경 없이 같은 페이지에 결과를 in-place
렌더링하도록 변경했다. ProgressPanel 의 router.push 두 곳을 제거해 자동
라우팅을 차단했고, 폼 입력값은 신규 `useFormPersistence` hook 으로
localStorage 에 디바운스(500ms) 저장 + 마운트 시 복원되도록 분리했다.
이력 화면 `/backtests/[run_id]` 는 손대지 않아 회귀 0.

## 변경된 파일

신규:
- `projects/stock-backtest/frontend/hooks/useFormPersistence.ts` (신규, 138 lines)
  - 제네릭 form state ↔ localStorage 영속화 hook. 버전 필드(`__version`)
    포함, debounce 저장, migrate 콜백 지원. SSR 안전 (typeof window 가드).
  - 반환: `[value, setValue, hydrated, clear]` 4-tuple.
- `projects/stock-backtest/frontend/hooks/__tests__/useFormPersistence.test.ts` (신규, 178 lines)
  - vitest + @testing-library/react + jsdom. 6 케이스: save / restore /
    version mismatch (no migrate) / version mismatch (with migrate) /
    clear / malformed JSON.
- `projects/stock-backtest/frontend/vitest.config.ts` (신규, 22 lines)
  - environment=jsdom, alias `@/*` → 프런트 루트.

수정:
- `projects/stock-backtest/frontend/app/backtests/new/page.tsx` (539 → 615 lines)
  - 단일 컬럼 → 2-column (lg:grid-cols-2). 좌측 폼은 lg 이상에서 sticky.
  - 폼 9 필드를 `PersistedFormState` interface 로 묶어 `useFormPersistence`
    훅 1회 호출로 일괄 직렬화/복원. 키: `backtest:last_form_state:v1`.
  - universe 는 asset_id 배열만 영속화하고, 마운트/복원 시 `api.getAsset`
    으로 entity 재조회 (Asset 카탈로그가 변동할 수 있으므로).
  - 실행 후 `router.push` 제거 → `setSubmittedRunId(run.run_id)` 만 갱신,
    우측 패널이 ProgressPanel 폴링 → done 시 BacktestResult fetch → 결과
    컴포넌트 (EquityChart/DrawdownChart/MetricsTable/MonthlyHeatmap/
    TradesTable) in-place 렌더.
  - `BacktestResultPanel` 내부 컴포넌트 신규 (page 파일 안) — 결과 영역
    렌더 전담. 같은 시각화 컴포넌트를 `/backtests/[run_id]` 와 공유.
  - "다시 시작" / 새 run 트리거 시 직전 result state 자동 클리어.
- `projects/stock-backtest/frontend/components/backtest/ProgressPanel.tsx` (237 → 230 lines)
  - `useRouter` import + 인스턴스 + `router.push` 두 곳 모두 제거 (L24/L81/L89/L139).
  - status='done' 카드: "결과 보기 →" 버튼 제거 → "새 백테스트" 버튼만
    유지. 자동 라우팅 useEffect 통째로 제거. `AUTO_REDIRECT_MS` 상수 제거.
  - 호출부에서 결과를 in-place 렌더하므로 done 카드는 안내 문구만 노출.
- `projects/stock-backtest/frontend/lib/i18n/ko.ts`
  - `progress.doneInPlace` 키 추가 ("결과를 아래에서 확인하세요.").
- `projects/stock-backtest/frontend/package.json`
  - devDependencies 추가: `jsdom@^25`, `@testing-library/react@^16`,
    `@testing-library/dom@^10` (vitest 가 이미 있어서 추가 안 함).

## DoD 검증 결과

| DoD | 검증 방법 | 결과 |
|-----|----------|------|
| (a) 시나리오 실행 → URL 변경 없음 + 결과 자동 표시 | router.push 호출 제거 + in-place 렌더 코드 확인 (page.tsx L545-575). `grep "router.push" components/ app/` → ProgressPanel 0건, page.tsx "/backtests/" 라우팅 0건 (cancel 시 router.push("/") 만 있음, 의도적). | PASS |
| (b) 새로고침 후 폼 값 복원 | useFormPersistence 단위 테스트 "restore: 마운트 시 동일 버전 stored 를 채택" 통과. 9 필드 모두 단일 object 로 저장. universe 는 asset_id 만 저장 후 마운트 시 `api.getAsset` 으로 hydrate. | PASS |
| (c) 파라미터 1개만 바꿔 재실행 → 폼 유지 | submittedRunId 만 새 run_id 로 갱신. 폼 state 는 useFormPersistence 가 보유 → 유지됨. setResult(null) 만 트리거되어 직전 결과 클리어. | PASS |
| (d) 이력에서 /backtests/[run_id] 진입 시 기존 결과 화면 정상 동작 (회귀 0) | `/backtests/[run_id]/page.tsx` 미수정 (`git status` 로 확인). 같은 시각화 컴포넌트 (EquityChart 등) 사용. 빌드 산출물에서 `/backtests/[run_id]` 라우트 정상 빌드됨 (`Route (app) ... ƒ /backtests/[run_id]  1.98 kB`). | PASS |
| 빌드 성공 | `npm run build` → ✓ Compiled successfully + ✓ Generating static pages (6/6). 모든 라우트 정상 빌드. | PASS |
| 단위 테스트 통과 | `npm test -- useFormPersistence --run` → 6/6 통과 (532ms). | PASS |
| 추가 — typecheck | `npm run typecheck` → 무에러. | PASS |
| 추가 — lint | `npm run lint` → No ESLint warnings or errors. | PASS |

## 핵심 결정

1. **9 필드 단일 object 영속화**: useFormPersistence 를 필드별 호출 (n번)
   하지 않고 PersistedFormState 묶음 1회 호출. 디바운스가 필드별 분산되지
   않고 통합되어 storage write 횟수 최소화 + JSON.stringify 한 번에.

2. **universe 는 asset_id 배열만 저장**: Asset entity 의 symbol/name/market
   은 카탈로그 변동 시 stale 가능 → 마운트 시 `api.getAsset(id)` 로 재조회.
   조회 실패 (자산 삭제됨) 시 silent drop. 사용자가 다시 검색해 추가 가능.

3. **버전 필드 도입**: `backtest:last_form_state:v1` + `__version: 1` 페이로드.
   향후 PersistedFormState shape 변경 시 stored payload 가 sliently 깨지지
   않도록 안전망. migrate 콜백 옵션도 hook 에서 지원.

4. **ProgressPanel `onComplete?: callback` 패턴 채택 X**: Reviewer ver 2
   PASS report 의 권고대로 단순화 우선 — done 안내 카드만 표시 + onReset
   으로 폼 모드 복귀. 미래에 다른 진입점 추가 시 callback 패턴 도입 가능.

5. **결과 컴포넌트 공유**: `BacktestResultPanel` 을 page.tsx 내부 함수로
   배치 (별도 파일 신규 분리 X). `/backtests/[run_id]` 와 동일한 5개 시각화
   컴포넌트를 import 해 결과 영역 렌더. 두 화면이 같은 모양 보장 + 미래
   중복 제거 시 컴포넌트로 승격 후보 (현재는 2회 사용에 그쳐 추상화 보류).

6. **vitest 도입 + jsdom env**: vitest 는 package.json 에 이미 있었으나
   환경 미설정 + jsdom 미설치. 이번에 vitest.config.ts + jsdom + @testing-library/react
   설치. 기존 dev/build/typecheck/lint 스크립트와 분리되어 영향 없음.

7. **persona harness 미수정**: `backend/tests/e2e/test_persona_first_use.py`
   를 grep 한 결과 router/push/navigate/location 키워드 0건 → router.push
   동작에 의존하지 않는다. 폴링 검증 (`/api/backtests/{run_id}` 직접 GET)
   과 한국어 키워드 검증만 수행 → 변경 불필요. (참고: coder.md L188 은
   tests/ 수정을 Tester 전담으로 명시 — 코더가 손대지 않는 것이 안전.)

## 변경된 파일에 추가된 public 메서드 시그니처

신규:
- `useFormPersistence<T>(options: UseFormPersistenceOptions<T>): [T, (next: T | ((prev: T) => T)) => void, boolean, () => void]`

기존 ProgressPanelProps 에서 변경 없음 (그대로 `{ run, loading, error, onCancel, onReset }`).

## 이슈/블로커

없음.

## 다음 제안

1. **이력 카드에서 `/backtests/[run_id]` 진입 경로 명시**: TASK-218 description
   에 "이력에서 /backtests/[run_id] 진입 시 기존 결과 화면 정상 동작" 이
   DoD (d) 로 박혔지만, 현재 어플 메인 (`/`) 에 이력 카드가 있는지 별도
   확인 필요. `/backtests` 인덱스 라우트 미존재일 수 있음 → 후속 태스크
   (별도 ID) 로 이력 화면 추가 검토 권장.

2. **localStorage 가 잠겨 있을 때 amber 토스트**: useFormPersistence 는
   quota/permission 실패 시 silent. 사용자가 incognito mode 등에서 폼 값이
   안 살아남는 이유를 모를 수 있음. 후속에 hydrated state + storage 가
   사용 가능한지 별도 감지해 toast 안내 추가 가능.

3. **결과 컴포넌트 추상화 (3회 사용 시)**: 현재 `/backtests/[run_id]/page.tsx`
   와 `/backtests/new/page.tsx` 두 곳에서 EquityChart 등을 거의 동일 구조로
   조합. 3번째 사용처 (예: 비교 대시보드) 가 등장하면 `<BacktestResultView>`
   컴포넌트로 승격 후 양쪽 page 가 import 하도록 리팩터.
