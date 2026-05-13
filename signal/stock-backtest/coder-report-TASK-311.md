---
task_id: TASK-311
status: DONE
severity: none
---

# TASK-311 — UniverseSelector STOCK 생존편향 경고 토스트 (C5 후속)

## 요약

`UniverseSelector` 에 STOCK (Phase 2 테마주 트랙 · 개별주) 자산이 universe 에
1개 이상 포함될 때 한국어 경고 토스트를 1회 노출. 사용자에게 백테스팅 결과의
낙관 편향 (delisted 종목 미포함 → 생존편향) 위험을 알리고 "테마 관찰" 트랙으로
유도. small change — 1 컴포넌트 + ko.ts 1 키 + 단위 테스트 2건.

## 변경 파일

| 파일 | 변경 | 목적 |
| --- | --- | --- |
| `frontend/components/backtest/UniverseSelector.tsx` | +18 / -1 | `useRef<boolean>` 기반 warned-once flag. `add()` 시점에 STOCK 포함 여부 체크 → `toast({ title: ko.warning.survivorshipBias, variant: 'destructive' })` 1회. |
| `frontend/lib/i18n/ko.ts` | +7 / -0 | `warning.survivorshipBias` 신규 키. (`error` 키 바로 아래 `warning` namespace 신설 — `error` 와 의미 분리: error 는 발생한 실패, warning 은 사전 위험 경고.) |
| `frontend/components/backtest/__tests__/UniverseSelector.test.tsx` | 신규 (+126 LOC) | vi.mock 으로 `api.listAssets` + `useToast` 대체. STOCK 추가 → spy 1회 / ETF·EQUITY_INDEX 만 추가 → spy 0회. |

## 설계 결정

1. **노출 위치 — UniverseSelector 내부 `add(asset)`**:
   - 대안 (page.tsx useEffect 로 selected universe 감지) 보다 위치 결합도가 낮음.
   - page 가 `<UniverseSelector value={universe} onChange={...} />` 로 컴포넌트를
     사용하는 한, 어디서 호출되든 동일 정책 적용.
   - 추가/제거 흐름이 단일 진입점 (`add()`) 이라 1회 표시 보장이 쉽다.

2. **debounce 대신 useRef warned-once 패턴**:
   - 태스크 본문은 "debounce 500ms 또는 useRef warned flag" 두 선택지 모두 허용.
   - useRef 는 동일 마운트에서 1회만 표시 — 동일 세션 노이즈 0.
   - 사용자가 STOCK 을 모두 제거하고 다시 추가해도 같은 마운트에서는 재노출 X
     (잔소리 방지). 다른 페이지로 이동했다가 돌아오면 마운트 reset 으로 재표시
     가능 — 합리적 동작.

3. **i18n namespace — `warning.*`**:
   - `error.*` 와 동격 (사후 오류 vs 사전 경고).
   - 향후 다른 종류의 사전 경고 (예: 짧은 기간 / 적은 자본 / 단일 자산) 가
     생길 때 동일 namespace 에 누적 가능. 코멘트로 의도 명시.

4. **테스트 — useToast 자체를 mock**:
   - ToastProvider 래핑 없이 `useToast()` 가 `{ toast: toastSpy }` 를
     반환하도록 vi.mock. AssetPicker 테스트는 ToastProvider 래핑 후
     실제 토스트 DOM 노드를 검증하는 방식인데, 본 태스크는 "spy 호출 횟수"
     검증이 단순/직접적이라 useToast mock 이 더 가볍다.
   - `api.listAssets` 도 mock 으로 검색 결과 주입 → "검색 → 결과 클릭 → 추가"
     실제 사용 흐름을 그대로 재현.

## DoD 검증

| DoD | 결과 | 증거 |
| --- | --- | --- |
| (a) STOCK 선택 시 토스트 노출 | PASS | 테스트 1 `toastSpy.toHaveBeenCalledTimes(1)` + variant=destructive + title 에 "생존편향" 포함. |
| (b) 단위 테스트 2건 PASS | PASS | `npx vitest run components/backtest/__tests__/UniverseSelector.test.tsx` → `Tests 2 passed (2)` (679ms). |
| (c) ETF/EQUITY_INDEX 만 선택 → 토스트 0건 | PASS | 테스트 2 `toastSpy.not.toHaveBeenCalled()`. |
| (d) `npm run build` PASS | PASS | Next.js 14.2.15 — Compiled successfully, 7 routes, `/backtests/new` 8.92 kB (변경 전 대비 +18 LOC 흡수). 회귀 0. |
| (e) `lib/i18n/ko.ts` 신규 키 1건 | PASS | `grep survivorshipBias frontend/lib/i18n/ko.ts` → L68 발견. |

## 검증 명령 (재현용)

```bash
cd /home/jai/pa/stock-backtest/projects/stock-backtest/frontend
npx vitest run components/backtest/__tests__/UniverseSelector.test.tsx
# Tests  2 passed (2)

npm run build
# ✓ Compiled successfully
# ✓ Generating static pages (7/7)

grep -n survivorshipBias lib/i18n/ko.ts components/backtest/UniverseSelector.tsx
# lib/i18n/ko.ts:68:    survivorshipBias:
# components/backtest/UniverseSelector.tsx:56,87,90,92 (Ref + 호출처)
```

## 이슈 / 블로커

없음.

## 후속 제안 (Manager 판단)

- 토스트 노출 후 사용자가 "테마 관찰" 트랙으로 이동할 수 있는 CTA 버튼이
  있으면 더 친절. (현재는 본문만 안내.) 본 태스크 범위 밖이라 미구현.
  필요 시 별도 태스크 (`warning.survivorshipBias.cta` + Link to /themes).
