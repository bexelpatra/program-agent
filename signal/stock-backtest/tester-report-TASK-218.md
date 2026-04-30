---
agent: tester
task_id: TASK-218
status: DONE
timestamp: 2026-04-30T17:35:00
severity: observation
---

## 결과 요약

TASK-218 (`/backtests/new` 인플레이스 결과 표시) 검증 완료. 7개 검증 항목 모두 PASS:
단위 테스트 6/6, build 6/6 페이지, typecheck 무에러, lint 무경고, router.push 자동
라우팅 제거 확인, localStorage 키 충돌 0건, `/backtests/[run_id]` 회귀 0건. Coder 코드
결함은 발견되지 않았다. 다만 (1) coder-report 의 line count 와 실측치가 큰 폭으로
어긋나고, (2) `app/backtests/new/page.tsx` 가 794 라인까지 비대화되어 함수 1개
(`BacktestResultPanel`, L725-L794) 가 같은 파일에 in-line 으로 들어가 있다는 점을
observation 으로 기록한다 (코드 결함 아님).

## 검증한 파일

신규 (Coder 가 생성):
- `projects/stock-backtest/frontend/hooks/useFormPersistence.ts` (164 lines · report=138)
- `projects/stock-backtest/frontend/hooks/__tests__/useFormPersistence.test.ts` (218 lines · report=178)
- `projects/stock-backtest/frontend/vitest.config.ts` (23 lines · report=22)

수정:
- `projects/stock-backtest/frontend/app/backtests/new/page.tsx` (539 → 794 lines · report=615, 실측 +179 차이)
- `projects/stock-backtest/frontend/components/backtest/ProgressPanel.tsx` (237 → 221 lines · report=230)
- `projects/stock-backtest/frontend/lib/i18n/ko.ts` (`progress.doneInPlace` 키 추가)
- `projects/stock-backtest/frontend/package.json` (devDeps + jsdom/@testing-library)

Tester 가 새로 작성한 테스트는 없음 (Coder 의 6 케이스가 핵심 분기 — save / restore /
version-mismatch (no migrate) / version-mismatch (with migrate) / clear / malformed
JSON — 을 모두 커버하므로 추가 케이스 불필요).

## 테스트 결과

### 1. useFormPersistence 단위 테스트 (vitest)

```
$ cd projects/stock-backtest/frontend && npx vitest run hooks/__tests__/useFormPersistence.test.ts
 RUN  v2.1.3 /home/jai/pa/stock-backtest/projects/stock-backtest/frontend
 ✓ hooks/__tests__/useFormPersistence.test.ts  (6 tests) 16ms
 Test Files  1 passed (1)
      Tests  6 passed (6)
   Duration  525ms
```

- 통과: 6
- 실패: 0
- 측정 시간: 525ms (env 189ms + transform 29ms + collect 69ms + tests 16ms + prepare 138ms)
- 검증 분기: save · restore · version-mismatch (no migrate) · version-mismatch (with migrate) · clear · malformed JSON

### 2. typecheck (npx tsc --noEmit)

```
$ npx tsc --noEmit
(무출력 = success)
```
무에러 → PASS.

### 3. lint (npm run lint)

```
> next lint
✔ No ESLint warnings or errors
```
PASS.

### 4. production build (npm run build)

```
✓ Compiled successfully
✓ Generating static pages (6/6)

Route (app)                              Size     First Load JS
┌ ○ /                                    7 kB           94.4 kB
├ ○ /_not-found                          876 B          88.3 kB
├ ○ /assets                              2.86 kB         116 kB
├ ƒ /backtests/[run_id]                  1.98 kB         220 kB
└ ○ /backtests/new                       9.22 kB         227 kB
```
- 6/6 페이지 빌드 성공.
- `/backtests/new` (Static, 9.22 kB) — TASK-218 변경 대상, 이전 build 대비 페이지 크기
  증가 확인 (인플레이스 결과 컴포넌트 5종을 같은 페이지에 임포트하므로 자연스러운 증가).
- `/backtests/[run_id]` (Dynamic, 1.98 kB) — 기존 결과 화면 정상 빌드 (회귀 없음).

### 5. router.push 자동 라우팅 제거 검증

```
$ grep -rn "router.push" app/backtests/new components/backtest
components/backtest/ProgressPanel.tsx:79:  // 진입점(앱 메인 이력 카드 등) 은 그쪽에서 직접 router.push 한다.
app/backtests/new/page.tsx:8: *     기존에는 status='done' 시 `/backtests/[run_id]` 로 router.push 했지만,
app/backtests/new/page.tsx:430:      // TASK-218: router.push 하지 않는다. 같은 페이지 우측 패널에서
app/backtests/new/page.tsx:671:                <Button variant="secondary" onClick={() => router.push("/")}>
```

- ProgressPanel 의 코드 호출: 0건 (L79 는 docstring 코멘트). useRouter import + 인스턴스
  + 두 곳의 router.push 모두 제거 확인 (L23-28 import 만 보면 `next/navigation` 라인 자체
  없음).
- page.tsx L430 은 자동 라우팅 제거 의도를 명시한 코멘트, L671 은 폼 cancel 시 홈
  (`/`) 으로 이동하는 정당한 사용 (`/backtests/[run_id]` 라우팅 0건).
- DoD (a) "URL 변경 없음 + 결과 자동 표시" 충족.

### 6. localStorage 키 충돌 검증

```
$ grep -rn "backtest:last_form_state" .
hooks/useFormPersistence.ts:32:  /** localStorage 키. 호출부가 버전을 포함시킨다 (예: "backtest:last_form_state:v1"). */
app/backtests/new/page.tsx:11: *     후에도 복원된다 (키: backtest:last_form_state:v1).
app/backtests/new/page.tsx:123:const FORM_STORAGE_KEY = "backtest:last_form_state:v1";
```

- 실제 사용 (storageKey 값으로 전달) 은 page.tsx:123 의 단일 정의. hook 주석 + page
  파일 docstring 외에 키 충돌 없음. PASS.

### 7. `/backtests/[run_id]/page.tsx` 회귀 0건

```
$ git status projects/stock-backtest/frontend/
수정함: app/backtests/new/page.tsx
수정함: components/backtest/ProgressPanel.tsx
수정함: lib/api/schemas.ts             # ← TASK-220 변경분 (semi_annual)
수정함: lib/i18n/ko.ts
수정함: package-lock.json
수정함: package.json

$ git diff --stat HEAD -- 'projects/stock-backtest/frontend/app/backtests/[run_id]/page.tsx'
(빈 출력 = 변경 없음)
```

- `[run_id]/page.tsx` 는 working tree 에서 미수정. 마지막 commit 은 29a4fa7 (V3 Phase 1).
- 빌드 산출물에서 `/backtests/[run_id]` 라우트 정상 (1.98 kB). 회귀 0.

### 8. 클린 아키텍처 위반 감지 (Tester 표준 절차)

| 체크 | 결과 |
|------|------|
| domain 코드의 HTTP/DB/UI import | 변경 없음 (presentation 레이어만 수정) |
| presentation → data 직접 import | useFormPersistence 는 hooks 레이어에 분리, page.tsx 는 `lib/api` (data 어댑터) 만 호출 — 정상 |
| feature 간 직접 import | 없음 |
| 함수 과대 (40 lines+) | `BacktestResultPanel` (L725-L794, 70 lines) 1개. 결과 영역 렌더 전담이라 분기는 단순. observation 수준 |
| 매개변수 6개 이상 | 없음 |
| DTO ↔ Entity 누수 | 없음. `PersistedFormState` 는 page 내부 interface, asset_id 만 직렬화 (entity 는 마운트 시 재조회) |
| ProgressPanel unused import | useRouter / next/navigation 모두 제거 확인 (L23-28). PASS |

### 9. 추가 검증

- ProgressPanel 의 `AUTO_REDIRECT_MS` 상수: grep 결과 잔존 0건 → 깨끗이 제거됨.
- vitest.config.ts alias `@/*` → `path.resolve(__dirname, "./")` 가 tsconfig paths 와 동기.
  실행 시 `@/hooks/useFormPersistence` resolve 정상.
- jsdom 환경에서 fake timer 로 debounce flush 검증 — 16ms 만에 6 케이스 PASS, 환경 설정
  적정.

## 이슈/블로커

### Observation 1: coder-report 의 line count 가 실측과 어긋남

| 파일 | report 주장 | 실측 | 차이 |
|------|------------|------|------|
| useFormPersistence.ts | 138 | 164 | +26 |
| useFormPersistence.test.ts | 178 | 218 | +40 |
| vitest.config.ts | 22 | 23 | +1 |
| page.tsx | 615 | 794 | **+179** |
| ProgressPanel.tsx | 230 | 221 | -9 |

특히 page.tsx 가 539 → 794 (실제 +255 lines) 로 늘었지만 report 는 539 → 615 (+76)
로 작성되어 있다. 코드 자체에는 문제가 없지만, 다음 검증/회고 단계에서 라인 수
비교가 부정확해질 수 있다. severity=observation. Manager 가 후속 코드 수정 태스크를
만들 필요는 없으나, Coder 의 자기 보고 정확도 권고 (회고 항목 candidate).

### Observation 2: `BacktestResultPanel` 이 `page.tsx` 에 in-line (L725-L794, 70 lines)

Coder report 결정 5: "현재는 2회 사용에 그쳐 추상화 보류" 라고 명시. 합리적 결정
이지만 page 파일이 794 라인까지 비대화된 직접 원인이다. 미래 3번째 사용처가 등장하면
`components/backtest/BacktestResultPanel.tsx` 로 분리할 것을 권장 (Coder 도 동일
권고). severity=observation, 코드 결함 아님.

### 코드 결함

없음. router.push 자동 라우팅 제거 / 폼 영속화 / hook 분리 / typecheck / lint / build
모두 정상.

## 다음 제안

1. **Manager 처리**: 본 보고서는 severity=observation 이므로 코드 수정 후속 태스크
   불필요. TASK-218 을 DONE 으로 갱신하면 된다.
2. **회고 후보**: Coder 의 자기 보고 line count 정확도 — 향후 회고에서 "Coder report
   의 wc -l 값을 실제 wc 결과로 직접 산출하도록" 가이드 추가 검토 (현재 coder.md 에
   명시 안 됨).
3. **후속 작업 (TASK-218 와 별개)**: Coder report 의 "다음 제안" 3개 (이력 카드 진입
   경로 명시 / amber toast 추가 / `BacktestResultPanel` 컴포넌트 승격) 는 이미 잘
   정리되어 있어 그대로 backlog 에 보관 권장.
