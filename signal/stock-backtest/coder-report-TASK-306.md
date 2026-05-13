---
task_id: TASK-306
status: DONE
agent: coder
severity: none
---

# Coder Report — TASK-306: Frontend Zod 스키마 + API 클라이언트 (Theme CRUD + STOCK enum 동기)

## 산출물

수정/추가된 4 파일 (지시 범위 준수):

1. `projects/stock-backtest/frontend/lib/api/schemas.ts` — Theme 관련 13 Zod 스키마 추가.
2. `projects/stock-backtest/frontend/lib/api/client.ts` — 10 신규 API 메서드 + `deleteNoContent` 헬퍼.
3. `projects/stock-backtest/frontend/lib/api/types.ts` — `z.infer` SoT 패턴으로 12 신규 타입 export.
4. `projects/stock-backtest/frontend/lib/api/__tests__/schemas.test.ts` (신규) — 4 describe / 8 it.

`lib/i18n/ko.ts` 는 손대지 않음 (TASK-307 책임).

## 주요 결정

- **STOCK enum**: `AssetTypeEnum` L45 에 이미 존재 (TASK-300 산출물). 재추가 없음. `grep -n "STOCK" schemas.ts` = L44(주석) + L45(enum 값) 2 hit, 의미상 1 멤버.
- **PaginatedResponse[T] 제네릭 envelope**: 백엔드 `app/schemas/common.py` 의 `PaginatedResponse[T]` 1:1 미러. 기존 `PaginatedAssetsSchema` 가 자산 전용으로 굳어 있어 신규 `paginatedResponseSchema<T>(item)` 팩토리 추가 후 `PaginatedThemesSchema = paginatedResponseSchema(ThemeReadSchema)` 로 인스턴스화.
- **Decimal → number coerce**: 백엔드 `SeriesPoint.value` 는 Pydantic Decimal → JSON string 직렬화. `z.coerce.number()` 로 string/number 양쪽 수용 후 number 로 강제. recharts 호환성 확보.
- **dict[int, ...] key 문자열화**: 백엔드 `ThemeChartResponse.members: dict[int, list[SeriesPoint]]` 가 JSON 직렬화 시 key 가 string 화 됨 (`"101"`). Zod `z.record(z.array(SeriesPointSchema))` 로 받고, 호출 사이트가 `Number(k)` 로 복원하는 패턴.
- **204 No Content DELETE 헬퍼**: 기존 `cancelBacktest` 의 raw fetch 패턴을 `deleteNoContent(path)` 로 추출. `deleteTheme` / `removeAssetFromTheme` 두 곳에서 재사용.
- **`api.compareThemes`**: 백엔드가 `?theme_ids=1&theme_ids=2` 반복 + `1,2,3` 콤마 둘 다 지원하지만 클라이언트는 반복 형식으로 고정 (URLSearchParams.append).
- **타입 import 분리**: `ThemeCreate`/`Update`/`AssetAdd` 같은 z.infer 타입은 schemas.ts 가 아닌 types.ts 에서 import. 타입 SoT 가 types.ts 임을 client.ts 가 따른다.

## DoD 검증

- (a) `npx tsc --noEmit` → PASS (출력 없음).
- (b) `npm run build` → PASS (`✓ Compiled successfully`, 6 페이지 정적 생성, /backtests/new 8.84 kB 등 기존 라우트 사이즈 유지).
- (c) `npx vitest run lib/api/__tests__/schemas.test.ts` → 8 tests PASS (567ms). 3 round-trip 그룹: ThemeRead 정상 + null 필드, ThemeCreate 누락 throw + 정상, ThemeChartResponse Decimal string/number coerce + dict key 문자열 + universe_meta + SeriesPoint 단독.
- (d) `grep -n "STOCK" lib/api/schemas.ts` → 2 hit (주석 L44 + enum 멤버 L45). 멤버 카운트 1 (AssetTypeEnum 의 6번째 값) — 의도와 일치.
- (e) 신규 10 메서드 모두 `api.*:` 패턴으로 노출 확인: listThemes / createTheme / getTheme / updateTheme / deleteTheme / addAssetToTheme / removeAssetFromTheme / getThemeChart / compareThemes / getAssetThemeHistory.

## 알려진 한계 / 후속 권장

- `compareThemes` 백엔드는 멤버 0 / 가용 OHLCV 0 / weighting=market_cap 일 때 422 를 반환한다. UI 호출 사이트에서 ApiError.status === 422 분기 처리 필요 (TASK-307 또는 UI 통합 태스크에서).
- `ThemeChartResponse.members` 의 string key 가 호출 사이트에서 `Number(k)` 변환 시 NaN 방어 필요 (백엔드는 항상 정수 문자열만 보내지만 type level 에서는 모름). UI 통합 시 가이드.

## 이슈/블로커

없음.
