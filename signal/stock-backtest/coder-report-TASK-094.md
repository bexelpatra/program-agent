---
agent: coder
task_id: TASK-094
status: DONE
timestamp: 2026-04-29T12:10:00
---

## 결과 요약

`/backtests/new` 화면에 in-place 진행률 패널을 부착해 폼 모드 ↔ 진행 모드를 토글하도록 구현했다. 별도 라우트(`/backtests/[run_id]/progress` 등)를 만들지 않아 UI/UX 원칙 6 (점진적 노출, 화면 3개 한도 — `/assets`, `/backtests/new`, `/backtests/[run_id]`) 를 그대로 유지한다. status='done' 시 ProgressPanel 이 1.5s 후 결과 화면 (TASK-093) 으로 자동 라우팅하며, 사용자가 "결과 보기" 버튼을 누르면 즉시 이동한다.

폴링 cadence·terminal 분기·취소 트리거를 useBacktestPolling 훅으로 분리해 ProgressPanel 은 순수 표현 컴포넌트가 되도록 클린 아키텍처를 유지했다. 한국어 메시지 (진행률·취소·완료·실패·취소됨·에러 가이드 5종) 은 `lib/i18n/ko.ts` 에 `progress` / `errorGuide` 키로 추가 — 기존 `backtest.*` (폼 라벨) 과 의도적으로 분리.

DELETE /api/backtests/{run_id} 는 백엔드가 204 No Content 를 반환 (응답 body 없음) 이라 `fetchAndValidate` (JSON 파싱 강제) 우회를 위해 `cancelBacktest` 만 별도 fetch 로직을 둔 뒤, 비2xx 시에만 ApiError 던지도록 처리.

## 변경된 파일

- `projects/stock-backtest/frontend/lib/i18n/ko.ts` (수정 — `progress`, `errorGuide` 키 append)
- `projects/stock-backtest/frontend/lib/api/client.ts` (수정 — `api.cancelBacktest(runId)` append, 204 No Content 대응)
- `projects/stock-backtest/frontend/hooks/useBacktestPolling.ts` (신규 — 1초 폴링 훅, terminal 자동 정지, cancel 트리거)
- `projects/stock-backtest/frontend/components/backtest/ProgressPanel.tsx` (신규 — pending/running/done/failed/cancelled/error 6개 분기 카드)
- `projects/stock-backtest/frontend/app/backtests/new/page.tsx` (수정 — `submittedRunId` state + `useBacktestPolling` 훅 연결 + JSX 분기 추가, `router.push` 즉시 라우팅 제거)

### 추가/변경된 public API 시그니처

`lib/api/client.ts` — `api` 객체에 추가:
- `cancelBacktest(runId: number): Promise<void>` — DELETE /api/backtests/{run_id}, 204 No Content 정상, 비2xx 시 ApiError throw

`hooks/useBacktestPolling.ts` — 신규:
- `useBacktestPolling(runId: number | null): { run, loading, error, cancelRun }`

## DoD 검증

| 항목 | 결과 |
|------|------|
| `npx tsc --noEmit` | exit 0 (출력 없음) |
| `npm run build` | exit 0 — `/backtests/new` 5.48 kB / 119 kB First Load |
| 라우트 생성 확인 | `/backtests/new` (Static) + `/backtests/[run_id]` (Dynamic) — 별도 진행 라우트 없음 |
| dev curl `/backtests/new` | HTTP 200, 한국어 라벨 (`기축통화`, `백테스트 실행`, `취소`, `새 백테스트`) 노출 |
| 화면 3개 한도 | 빌드 출력상 정확히 3개: `/assets`, `/backtests/new`, `/backtests/[run_id]` |

## UI/UX 원칙 6 (점진적 노출 — 화면 3개 한도) 준수 증거

`npm run build` 출력 (Route table):
```
├ ○ /                                    7 kB     (홈, 카드 navigation 만)
├ ○ /assets                              2.86 kB  (자산 카탈로그 — TASK-091)
├ ƒ /backtests/[run_id]                  106 kB   (결과 화면 — TASK-093)
└ ○ /backtests/new                       5.48 kB  (생성 화면 — TASK-092 + 진행률 패널 in-place)
```

진행률 표시는 `/backtests/new` 가 `submittedRunId === null` 분기로 폼 모드 ↔ ProgressPanel 모드를 토글한다. 별도 라우트 미생성.

## 한국어 메시지 신규 키 (`ko.progress` + `ko.errorGuide`)

진행 흐름: `pending` / `running` / `progressPct` / `cancel` / `cancelConfirm` / `cancelled` / `failed` / `failedTitle` / `done` / `doneTitle` / `doneRedirecting` / `seeResult` / `retry` / `newBacktest` / `creating` / `waiting` / `errorOccurred` / `stage` / `traceId`.

에러 가이드 (액션 포함): `networkFailure` (서버 연결 + 백엔드 확인 + 재시도) / `invalidUniverse` (자산 데이터 없음 + 카탈로그 백필 확인) / `periodTooShort` (최소 30일) / `insufficientCash` (universe 최소 가격 고려) / `notice` (기간 자동 조정 알림).

`errorGuide.*` 키는 본 태스크에서는 message catalogue 등록까지 — 실제 매핑 분기 (백엔드 error.type → guide key) 는 ProgressPanel 의 다음 iteration 또는 TASK-100 통합 시점에 백엔드 에러 type 목록과 함께 매핑할 후보. 현재는 ProgressPanel 이 backend 의 `error.message` 를 그대로 노출 (백엔드가 한국어 message 를 보내는 구조).

## 클린 아키텍처 점검

- presentation 레이어 (ProgressPanel) → application 레이어 (useBacktestPolling 훅) → data 레이어 (api.cancelBacktest, api.getBacktest) 의 단방향 의존. 역방향 import 없음.
- ProgressPanel 은 표현만, 폴링 / cancel 호출 / 상태 머신은 훅에 격리 (Single Responsibility).
- `lib/api/client.ts` 변경은 append-only — 기존 9개 메서드 무수정.
- `lib/i18n/ko.ts` 변경은 append-only — 기존 6개 섹션 (app/nav/asset/backtest/metric/error) 무수정.
- TASK-093 가 동시 작업 중인 `lib/api/schemas.ts` / `app/backtests/[run_id]/page.tsx` / 차트·테이블 컴포넌트는 일체 미터치 (병렬 안전).

## 이슈/블로커

없음.

## 다음 제안

1. **TASK-100 (e2e 통합) 시점 — 데이터 갭 통지 토스트 매핑**: 백엔드 `period_adjusted` (TASK-032 universe 시작일 교집합) 응답 필드를 폼 제출 직후 toast 로 띄우는 분기가 아직 없음. POST 응답 BacktestRun 에 `period_start_adjusted` 같은 필드가 노출되면 page.tsx 에서 detect 후 `ko.errorGuide.notice` + 차이 일수 표시. 현재는 백엔드 응답 schema 에 해당 필드가 없어 TASK-100 통합 시 백엔드 측과 동시 검토.
2. **ProgressPanel 자동 회복 정책**: useBacktestPolling 은 폴링 실패 (네트워크 끊김) 시 1초 후 재시도 — 무한 재시도. 일정 시도 횟수 (5회) 초과 시 backoff (5s → 30s) 또는 명시적 사용자 액션 요구로 강화하는 옵션. 현재는 한 명의 사용자가 잠깐 와이파이 끊기는 정도를 가정한 단순 정책.
3. **window.confirm 대신 dialog 컴포넌트**: 취소 확인은 `window.confirm(ko.progress.cancelConfirm)` 으로 단순 처리. 후속 design system 작업에서 shadcn/ui AlertDialog 도입 시 교체 후보.
4. **errorGuide 매핑 테이블**: `errorGuide.*` 키가 등록만 되었고 실제 백엔드 `error.type` → guide key 매핑이 없음. 백엔드가 어떤 type 코드를 보낼지 (TASK-082 schemathesis 출력) 확정되면 ProgressPanel 의 failed 분기에서 `error.type` switch → guide 노출 추가.
