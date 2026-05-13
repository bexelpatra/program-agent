---
task: TASK-308
agent: coder
status: DONE
severity: -
---

# TASK-308 — Frontend 화면 5 (테마 상세 + 정규화 차트) 구현 결과

## 작업 요약

- 신규 라우트 `/themes/[theme_id]` 추가 (Next.js App Router 동적 라우트).
- 정규화 차트 3종 (멤버 라인, 합산 라인, 다중 테마 비교) 신규 컴포넌트.
- `useThemeChartData` 훅 신규 — `api.getThemeChart` 호출 + 로딩/에러/refetch.
- 단위 테스트 10건 신규 (DoD 3건 이상 충족).

## 신규/수정 파일

신규
- `projects/stock-backtest/frontend/app/themes/[theme_id]/page.tsx` (370 LOC) — 테마 상세 페이지. 메타/멤버 표/기간 선택/정규화·합산 차트/비교 영역.
- `projects/stock-backtest/frontend/components/themes/charts/NormalizedPriceChart.tsx` — recharts `LineChart` 다중 라인 + 색상 팔레트 + `mergeMembers` 헬퍼.
- `projects/stock-backtest/frontend/components/themes/charts/ThemeAggregateChart.tsx` — 단일 라인 + 기준 100 ReferenceLine + 한국어 tooltip.
- `projects/stock-backtest/frontend/components/themes/charts/ThemeCompareChart.tsx` — 다중 테마 aggregate 비교 + `mergeThemes` 헬퍼.
- `projects/stock-backtest/frontend/hooks/useThemeChartData.ts` — opts 변경 시 자동 refetch, cleanup-safe.
- `projects/stock-backtest/frontend/hooks/__tests__/useThemeChartData.test.ts` — 3 시나리오 (loading→data, error, opts refetch).
- `projects/stock-backtest/frontend/components/themes/charts/__tests__/NormalizedPriceChart.test.tsx` — 4 케이스 (mergeMembers 2건 + render 2건).
- `projects/stock-backtest/frontend/components/themes/charts/__tests__/ThemeCompareChart.test.tsx` — 3 케이스 (mergeThemes 1건 + render 2건).

수정 (라인 0)
- `frontend/lib/i18n/ko.ts` — **본 태스크 수정 0 라인** (DoD d). 기존 working tree 변경분은 TASK-307 책임. `theme.detail.*` 키 부재 → inline 한국어 문자열 사용 (예: "테마 조회 실패", "기간이 자동 조정됐습니다", "비교 차트 그리기" 등).

## DoD 검증 결과

| DoD | 결과 | 증거 |
|------|------|------|
| (a) `npx tsc --noEmit` 통과 | PASS | 0 error |
| (b) `npm run build` PASS | PASS | `/themes/[theme_id]` 동적 라우트 빌드 성공 (4.67 kB, 224 kB FLJ) |
| (c) 단위 테스트 3건 PASS | PASS (10건) | `npx vitest run themes` → 16 tests, 5 files PASS (TASK-307의 9건 포함, 본 태스크 7건) |
| (d) `git diff ko.ts` = 0 라인 (TASK-308 기여분) | PASS | 본 태스크는 ko.ts 미수정. 기존 working tree 변경분은 TASK-307 IN_PROGRESS의 라벨 추가. |
| (e) NormalizedPriceChart 다중 자산 정상 렌더 | PASS | `members 2 시리즈 → recharts Line 2개 + 범례 2개 (한글 자산명 노출)` 테스트 통과 |

## 구현 노트

### 1. Zod input/output variance 우회
`schemas.ts` 의 `ThemeDetailSchema.active_members: z.array(...).default([])` 와 `UniverseMetaSchema.affected_assets: z.array(...).default([])` 가 input/output variance 를 발생시켜 `z.infer<...>` 와 `api.X()` 반환 타입 호환성이 깨졌다 (TASK-238 이 backtest 결과에서 다룬 것과 동일 패턴). 본 페이지/훅은 `Awaited<ReturnType<typeof api.X>>` 로컬 타입 alias 사용 + 방어적 `?? []` fallback 으로 우회. `schemas.ts` 수정 없이 해결.

### 2. recharts jsdom 호환 (테스트)
recharts `ResponsiveContainer` 는 ResizeObserver 미존재 시 throw + jsdom 의 0px layout 에서 SVG 미렌더. 테스트는 (i) ResizeObserver noop polyfill + (ii) `ResponsiveContainer` 를 width=800/height=320 cloneElement stub 으로 모킹. recharts 의 `<Line>`·`<Legend>` 자체는 그대로 사용 — 결과적으로 `.recharts-line` / `.recharts-legend-item` querySelector 카운트가 안정적.

### 3. universe 교집합 통지
`chartData.universe_meta.affected_assets.length > 0 && reason !== "ok"` 일 때만 토스트. hash 가드 (adjusted_start|adjusted_end|affected_ids) 로 동일 응답 재토스트 방지. 비교 결과는 별도 hash state 로 격리.

### 4. AssetPicker 미사용
TASK-307 가 `AssetPicker` 컴포넌트를 책임지므로 본 화면에서는 자산 추가 UI 생략 (멤버 표의 "제거" 버튼만 제공). TASK-307 DONE 후 Manager 가 `<AssetPicker>` import 추가하는 follow-up 가능.

### 5. ko.ts 사용 보류
TASK-307 가 `theme.detail.*` namespace 를 ko.ts 에 신규 추가하는 책임을 가져, 본 태스크는 inline 한국어 fallback 사용. TASK-307 DONE 후 후속 follow-up 으로 inline 문자열을 `t("theme.detail.xxx")` 호출로 치환 가능.

## 후속 follow-up 제안 (Manager 판단)

1. TASK-307 DONE 후 본 페이지의 inline 한국어 라벨 → `t("theme.detail.*")` 치환. 라벨 위치: 헤더/멤버 표/기간 선택/3종 차트 카드 제목/비교 영역. 약 15곳.
2. `AssetPicker` 컴포넌트 import → 자산 추가 인라인 UI 활성화.
3. ThemeAggregateChart 의 weighting 선택 (현재 `equal` 고정) — Phase 2.2 market_cap 지원 시 prop 추가.

## 테스트 산출물

```
$ npx vitest run themes
Test Files  5 passed (5)
Tests       16 passed (16)
```

상세 (본 태스크 신규):
- `useThemeChartData.test.ts` → 3 PASS
- `NormalizedPriceChart.test.tsx` → 4 PASS
- `ThemeCompareChart.test.tsx` → 3 PASS

전체 회귀:
```
$ npx vitest run
Test Files  9 passed (9)
Tests       37 passed (37)
```
