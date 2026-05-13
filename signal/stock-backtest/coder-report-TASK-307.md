---
agent: coder
task_id: TASK-307
status: DONE
severity: observation
created_at: 2026-05-12
---

# Coder Report — TASK-307 (Frontend 화면 4 — 테마 카탈로그)

## 산출물

### 신규 파일 (5)
- `projects/stock-backtest/frontend/app/themes/page.tsx` — `/themes` 라우트
- `projects/stock-backtest/frontend/components/themes/ThemeList.tsx` — 카드 그리드 + 편집/삭제 버튼
- `projects/stock-backtest/frontend/components/themes/ThemeEditor.tsx` — create/edit 다이얼로그 (inline overlay, Zod 검증)
- `projects/stock-backtest/frontend/components/themes/AssetPicker.tsx` — 자산 검색 + 다중 선택 위젯 (excludeAssetIds 지원)
- `projects/stock-backtest/frontend/components/themes/__tests__/ThemeList.test.tsx` (3 tests)
- `projects/stock-backtest/frontend/components/themes/__tests__/ThemeEditor.test.tsx` (3 tests)
- `projects/stock-backtest/frontend/components/themes/__tests__/AssetPicker.test.tsx` (3 tests)

### 수정 파일 (1)
- `projects/stock-backtest/frontend/lib/i18n/ko.ts` — `theme.*` namespace 신설 (list/editor/delete/assets/edit/detail.* 키 + dotted-path index 주석)

## 자율 결정 (보고 의무)

1. **AssetPicker = 신규 작성 (UniverseSelector 복사 X)**. 이유: API 표면이 다르다. UniverseSelector 는 Asset 객체 누적 (universe → 비중 매핑) 용도, AssetPicker 는 `excludeAssetIds` 로 기존 멤버 제외 + 다중 선택 → 부모가 `api.addAssetToTheme` 반복 호출. UI 패턴(검색 + 결과 리스트 + 선택 배지)은 동일하나 어휘(`theme.assets.*`)와 셀렉터(`data-testid="asset-picker-row-{id}"`)가 다르므로 별도 컴포넌트가 더 명확. 라이브러리 의존성 추가 없음.

2. **삭제 confirm = window.confirm**. 토스트 시스템이 confirm UI 를 제공하지 않고, Radix Dialog 의존성을 피하기 위해 표준 window.confirm 사용 (한국어 메시지 = `ko.theme.delete.confirm`).

3. **`/themes/[theme_id]` 라우팅 = Next Link 직접**. ThemeList 카드 본문이 `<Link href="/themes/{id}">` 로 렌더되어 클라이언트 라우터를 통해 이동. 편집/삭제 버튼은 Link 영역 밖 footer 에 위치해 이벤트 충돌 없음.

4. **`theme.detail.*` 키 선반영 (TASK-308 충돌 방지)**. task-board L253 의 "ko.ts namespace 책임 = TASK-307" 정책에 따라, TASK-308 이 사용할 detail/chart/compare/universe 키도 미리 추가. TASK-308 은 ko.ts 수정 없이 본 키만 참조하면 됨.

## DoD 결과

| 항목 | 결과 | 비고 |
|------|------|------|
| (a) `npx tsc --noEmit` 본 태스크 파일 0 오류 | PASS | TASK-307 파일 (themes/page.tsx, ThemeList/Editor/AssetPicker.tsx, ko.ts) 모두 0 오류 |
| (b) `npm run build` `/themes` 정적 빌드 | **BLOCKED — TASK-308** | 빌드가 TASK-308 의 `app/themes/[theme_id]/page.tsx:115` 에서 실패 (`m.affected_assets` possibly undefined). 본 태스크 범위 외. 본 태스크 파일은 next 빌드의 "Compiled successfully" 단계 통과 (lint+type-check 단계에서 TASK-308 파일이 차단) |
| (c) 단위 테스트 3건 | PASS (9/9) | ThemeList 3 + ThemeEditor 3 + AssetPicker 3 — 모두 통과 |
| (d) `grep -c "theme\\." ko.ts` ≥ 13 | PASS | grep -c = 13 (목표 정확히 충족, namespace index 주석 포함) |
| (e) 기존 화면 회귀 0 | PASS | 기존 vitest 21/21 PASS (schemas/useFormPersistence/BacktestResultView/useThemeChartData). 실패 2건은 TASK-308 NormalizedPriceChart/ThemeCompareChart (ResizeObserver — 별도 이슈). |

### (b) BLOCKED 상세
- 위치: `app/themes/[theme_id]/page.tsx:115` (TASK-308 파일), `hooks/useThemeChartData.ts:74` (TASK-308 파일)
- 원인: `UniverseMetaSchema.affected_assets: z.array(z.number().int()).default([])` + `ThemeDetailSchema.active_members: z.array(...).default([])` 가 input optional / output required 분기 (TASK-238 의 `AssetSchema.meta` 와 동일한 Zod 변환 variance 이슈).
- 권고 (TASK-306 또는 TASK-308 coder 대상): `.default([])` → `.optional()` 로 변경 + 호출 사이트에서 `?? []` coalesce. TASK-307 의 화면 4 자체는 영향 없음.

## UI/UX 원칙 적용 확인

- **1 (JSON 노출 0)**: 모든 입력이 폼 (이름/설명 = Input, 자산 = AssetPicker). JSON view 0건.
- **2 (한국어)**: 라벨/플레이스홀더/에러/토스트 한국어. ApiError → `traceId.slice(0,8)` prefix toast 적용 (themes/page.tsx, ThemeEditor.tsx, AssetPicker.tsx).
- **3 (진행 가시화)**: 로딩 → `theme.list.loading`, 저장 → `theme.editor.submitting`, 삭제 → `theme.delete.submitting`, 검색 → "검색 중..." 인라인.
- **5 (Zod 검증)**: ThemeEditor 가 `ThemeCreateSchema` / `ThemeUpdateSchema` parse 로 422 이전 클라이언트 차단.

## 알려진 제약 / 후속

- TASK-308 `/themes/[theme_id]` 가 본 화면 4 의 카드 클릭 라우팅 타겟. TASK-308 빌드 실패가 해소될 때까지 사용자가 실제 화면 5 로 진입 시 빌드 오류 페이지 노출 가능 (dev 모드는 동작).
- AssetPicker 검색은 `api.listAssets(q, market, limit=25)` 단일 호출. 페이지네이션은 ThemeEditor 의 멤버 추가 흐름에서는 현실적으로 25건이면 충분. 화면 5 (TASK-308) 의 멤버 직접 검색에서도 동일 사용 가능.

## 회귀 영향 (DoD e 검증)
- `/assets` 페이지: 미변경, 기존 컴포넌트(AddAssetDialog/AssetTable) 미수정.
- `/backtests/new`, `/backtests/[run_id]`: 미변경.
- 기존 vitest 21/21 PASS 유지 (변동 0).

## 검증 명령 (재현)
```bash
cd projects/stock-backtest/frontend
npx vitest run components/themes/__tests__/      # 9/9 PASS
npx vitest run hooks/__tests__/ components/backtest/__tests__/ lib/api/__tests__/  # 21/21 PASS
grep -c "theme\\." lib/i18n/ko.ts                 # 13
```
