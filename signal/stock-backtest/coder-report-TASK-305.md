---
agent: coder
task_id: TASK-305
status: DONE
timestamp: 2026-05-12T12:00:00
---

## 결과 요약

정규화 차트 API 2 endpoint (`GET /api/themes/{theme_id}/chart`, `GET /api/themes/compare`) 를 `backend/app/api/themes.py` 에 추가했다. Phase 2.1 백엔드 endpoint = 10개 (기존 8 + 2) 가 모두 OpenAPI 에 등록되었고, 4 통합 테스트 케이스 모두 PASS, 기존 회귀 0.

내부 데이터 흐름: `ThemeRepository.list_active_assets` → `AssetModel` 일괄 조회 → `Universe` 구성 → `period_adjustment.adjust_period_for_universe` → `OhlcvRepository` 대신 단일 IN 쿼리로 `Ohlcv` 일괄 조회 → pandas DataFrame (index=date, columns=asset_id) 구성 + ffill → `normalization.rebase_multi_series` + `compute_theme_aggregate(weighting="equal")` → SeriesPoint 응답. 캘린더 정렬은 prices_df 의 자연 합집합 index + forward-fill 로 간소화 (정규화 차트는 표시용, 백테스트 회계가 아님).

## 변경된 파일

- `projects/stock-backtest/backend/app/schemas/theme.py` (수정) — `SeriesPoint`, `UniverseMeta`, `ThemeChartResponse`, `ThemeCompareItem`, `ThemeCompareResponse`, `ChartAdjustmentReason` Literal 추가.
- `projects/stock-backtest/backend/app/api/themes.py` (수정) — chart endpoint 2건 + 헬퍼 5개 (`_asset_model_to_entity`, `_fetch_ohlcv_prices_df`, `_series_to_points`, `_build_universe_meta_from_period`, `_compute_theme_chart`) + import (`pandas`, `period_adjustment`, `normalization`, `Universe`, `AssetEntity`, `OhlcvModel` 등) 추가. 라우팅 순서 정책: `/compare` 라우트를 `/{theme_id}` 라우트보다 먼저 정의해 path 매칭 충돌 회피.
- `projects/stock-backtest/backend/tests/api/test_themes_chart.py` (신규) — 4 통합 테스트 케이스.

## 테스트 결과

- `pytest tests/api/test_themes_chart.py -q` → **4 passed** (single chart / compare 2 themes / universe 교집합 통지 / market_cap 422).
- `pytest tests/ -q --ignore=tests/api/test_themes_chart.py` → 변경 무관 baseline 실패 7건 유지 (test_api_contract.py fuzz 5건 + test_theme_repository.py 1건 + test_persona_first_use.py 1건은 사전 BLOCKER-001 잔재 / schemathesis 누적 상태 이슈, 본 변경과 무관함을 git stash 비교로 확인).
- `npm run build` (frontend) → **PASS** (6 routes, 변경 없음).
- OpenAPI 등록 검증: `GET /api/themes/compare`, `GET /api/themes/{theme_id}/chart` 둘 다 `app.openapi()` 출력에 노출.

## 이슈/블로커

**환경 이슈 — fuzz 잔여 자산**: `test_api_contract_fuzz[POST /api/assets]` 가 schemathesis 의 이전 fuzz run 에서 생성된 `(symbol='d', market='CRYPTO')` 자산이 DB 에 잔존해 409 가 나오는 환경 의존성을 발견했다. 본 태스크 변경과 무관하나, DB cleanup (`DELETE FROM assets WHERE symbol='d' AND market='CRYPTO'`) 후 재실행하면 PASS. 별도 환경 정리 태스크 또는 contract fuzz test 가 자기 데이터를 cleanup 하도록 보강하는 follow-up 권장 (severity=observation).

**라우팅 순서 결정**: FastAPI 가 `/api/themes/compare` 를 `/{theme_id}` 동적 path 의 정수 파싱 시도로 잡지 않게 하기 위해 `/compare` 데코레이터 정의를 `/{theme_id}` 위로 옮겨야 했다 (테스트 케이스 2 첫 실행 시 422 RequestValidationError 발견). 라우터 모듈 docstring 과 인라인 주석에 명시.

**market_cap weighting**: Phase 2.2 placeholder 로 명시적 422 + 한국어 메시지("Phase 2.2 에서 지원 예정") 반환 (DoD (c) 충족).

## 다음 제안

TASK-306 (Frontend Zod 스키마 + API 클라이언트) 으로 진행 가능. Zod 스키마는 본 태스크의 `SeriesPoint` (time: datetime, value: Decimal→string), `UniverseMeta` (adjusted_start/end: date, affected_assets: list[int], reason: Literal 4값, message: str), `ThemeChartResponse` (members: Record<int, SeriesPoint[]>, aggregate: SeriesPoint[], universe_meta), `ThemeCompareResponse` (themes: Record<int, ThemeCompareItem>, universe_meta) 와 1:1 매핑.

화면 4·5 (TASK-307·308) 병렬 진행 시 본 차트 API 가 활용된다. 사용자 통지: universe_meta.message 는 한국어이며 affected_assets (int list) 가 frontend 토스트로 직접 노출 가능.
