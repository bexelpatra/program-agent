---
task_id: TASK-300
status: DONE
---

# Coder Report: TASK-300

## 변경 파일 (상대 경로)

신규 (4):
- `projects/stock-backtest/backend/alembic/versions/0005_theme_tables.py` — Phase 2 마이그레이션 (themes / theme_assets / asset_theme_history / asset_market_cap)
- `projects/stock-backtest/backend/app/models/theme.py` — Theme + ThemeAsset + AssetThemeHistory ORM
- `projects/stock-backtest/backend/app/models/market_cap.py` — AssetMarketCap ORM (Phase 2.2 선행)
- `signal/stock-backtest/coder-report-TASK-300.md` — 본 보고서

수정 (5):
- `projects/stock-backtest/backend/app/domain/asset/entity.py` L18-19 — AssetType Literal 에 `"STOCK"` 추가 + Phase 2 트랙 주석
- `projects/stock-backtest/backend/app/schemas/asset.py` L17-18 — 동일 Literal 동기
- `projects/stock-backtest/backend/app/data/seed/assets_catalog.py` L16-17 — SeedAsset TypedDict 의 AssetType Literal 동기 (Reviewer r1 적발)
- `projects/stock-backtest/frontend/lib/api/schemas.ts` L38-47 — `AssetTypeEnum` z.enum 에 `"STOCK"` append (변경 최소화)
- `projects/stock-backtest/backend/app/models/__init__.py` — 신규 모델 4개 (AssetMarketCap, Theme, ThemeAsset, AssetThemeHistory) re-export

## 핵심 결정 / 주의점

- **alembic 0005 본문 = DDL only**: 테이블 생성 4개 + 부분 인덱스 1개 + CHECK 1개. AssetType `STOCK` 동기는 Python/TS Literal 정적 변경만 (assets.asset_type = `String(32)`, NO ENUM — Reviewer r2 PASS 확인).
- **부분 인덱스 `ix_theme_assets_active`**: `op.execute("CREATE INDEX ... WHERE removed_at IS NULL")` 로 SQL 직접 명시. SQLAlchemy 의 partial index Postgresql_where 옵션 대신 op.execute 채택 — alembic downgrade 에서도 명시적 `DROP INDEX IF EXISTS` 로 대응.
- **CHECK 제약 `ck_asset_theme_history_event_type`**: `sa.CheckConstraint` 로 등록 (sqlalchemy 가 DDL 생성). ORM 모델 `AssetThemeHistory.__table_args__` 에도 동일 CheckConstraint 등록 — metadata 일관성.
- **TimescaleDB hypertable**: `asset_market_cap` 은 try/except 로 graceful 변환 (패턴: `0002_timeseries_tables.py` L87-96). 일반 PG 환경에서는 일반 테이블로 동작.
- **`Theme` mixin 정책**: r1 분석대로 `themes` 만 `created_at` 보유 — TimestampedModel mixin 적용하면 `updated_at` 까지 강제되어 부담. mixin 미적용, `created_at` 만 명시. 다른 3 테이블 (`theme_assets`/`asset_theme_history`/`asset_market_cap`) 도 mixin 미적용 (append-only / 시계열).
- **`AssetTypeEnum` 추가 위치**: r1 권고대로 enum 멤버 끝 append (변경 최소화). 기존 위치별 검색 / 정렬 의존 코드 영향 0.

## 검증 결과

### DoD (a) `alembic upgrade head` 성공
```
$ ../.venv/bin/python -m alembic current
0004_fractional_qty
$ ../.venv/bin/python -m alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade 0004_fractional_qty -> 0005_theme_tables
$ ../.venv/bin/python -m alembic current
0005_theme_tables (head)
```
- 4 테이블 + 컬럼/PK/FK/부분 인덱스/CHECK 모두 inspect 로 확인:
  - `themes` PK=[theme_id], `theme_assets` PK=[theme_id, asset_id, added_at], `asset_theme_history` PK=[history_id] (BIGINT), `asset_market_cap` PK=[asset_id, time]
  - `ix_theme_assets_active`: `CREATE INDEX ... ON public.theme_assets USING btree (theme_id) WHERE (removed_at IS NULL)` 정상 생성
  - `ck_asset_theme_history_event_type`: `CHECK (event_type IN ('ADDED','REMOVED','RECLASSIFIED'))` 정상 등록

### DoD (b) `alembic history` 직선 + heads=0005
```
0004_fractional_qty -> 0005_theme_tables (head), Phase 2 — themes / theme_assets / asset_theme_history + asset_market_cap.
0003_backtest_tables -> 0004_fractional_qty
0002_timeseries_tables -> 0003_backtest_tables
0001_v3_baseline -> 0002_timeseries_tables
<base> -> 0001_v3_baseline
$ ../.venv/bin/python -m alembic heads
0005_theme_tables (head)
```
직선 + 단일 head 확인.

### DoD (c) AssetType Literal 4곳 STOCK
```
$ grep -nE '"STOCK"' projects/stock-backtest/backend/app/domain/asset/entity.py \
    projects/stock-backtest/backend/app/schemas/asset.py \
    projects/stock-backtest/backend/app/data/seed/assets_catalog.py \
    projects/stock-backtest/frontend/lib/api/schemas.ts
backend/app/domain/asset/entity.py:19:AssetType = Literal[..., "STOCK"]
backend/app/schemas/asset.py:18:AssetType = Literal[..., "STOCK"]
backend/app/data/seed/assets_catalog.py:17:AssetType = Literal[..., "STOCK"]
frontend/lib/api/schemas.ts:45:  "STOCK",
```
4 위치 모두 STOCK 등장 — PASS.

### DoD (d) `pytest tests/api/test_api_contract.py` 회귀 0
baseline (git stash 후 변경 전): 6 FAILED + 10 PASSED + 5 SKIPPED (21 items, fuzz parametrize)
변경 후: 5 FAILED + 12 PASSED + 4 SKIPPED (21 items)
- 신규 FAIL = 0
- 신규 SKIP = 0
- 1 FAIL → PASS (`POST /api/assets` — STOCK Literal 추가로 fuzz validator 가 더 잘 통과; 의도된 부수효과)
- 회귀 0 — PASS

### DoD (e) `npm run build` PASS
```
✓ Compiled successfully
✓ Generating static pages (6/6)
```
tsc 0 에러, 빌드 6 라우트 정상 생성.

## 후속 / 발견

- **task-board status 갱신 권고**: TASK-300 → DONE (Manager 책임).
- **TASK-301 즉시 가능**: Theme 도메인 entity + Repository Protocol + service (TASK-300 만 의존). 본 태스크 산출물 (4 ORM 모델 + STOCK Literal) 이 TASK-301 의 frozen dataclass entity 와 1:1 매핑 가능 상태.
- **`from_theme_id` FK 정책**: RECLASSIFIED 이벤트가 출처 테마 삭제 시 어떻게 동작할지에 대해 `ON DELETE SET NULL` 선택. r1 본문은 명시 없었으나 history 보존이 핵심 의도이므로 가장 안전한 선택. TASK-301 service 가 RECLASSIFIED 이벤트 발생 시 from_theme_id 채우는 책임을 가짐.
- **TASK-306 STOCK enum 추가 책임 일관성**: frontend `AssetTypeEnum` 은 본 태스크에서 이미 추가 완료 — TASK-306 본문이 "AssetTypeEnum L38-45 에 STOCK 추가 (TASK-300 백엔드 동기)" 라고 명시했지만 본 태스크에서 4곳 일괄 처리한 것이 task-board L237 후속 (Reviewer r2 PASS) 와도 정합. TASK-306 시작 시 frontend 부분은 skip 가능.
- **CI/test 환경 hypertable**: `asset_market_cap` hypertable 변환은 try/except 처리. 현재 dev DB 는 TimescaleDB 환경이므로 hypertable 생성 성공했으나 로그 미확인 (성공 시 INFO 미출력). 향후 일반 PG 환경 fixture 필요 시 0002 패턴 재사용.
- **테스트 분담**: 본 태스크는 ORM/마이그레이션 + Literal 동기까지만. ThemeRepository 단위/통합 테스트는 TASK-301 / TASK-302 / TASK-309 / TASK-310 (Tester 책임) 에서 처리.
