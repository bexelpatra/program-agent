---
agent: reviewer
project_id: stock-backtest
target: Phase 2.1 — 테마주 추적 모듈 MVP (TASK-300~310 + TASK-311)
scope:
  - signal/stock-backtest/architecture.md L19 / L93 / L520 / L740~743 / L823~1102
  - signal/stock-backtest/task-board.md L228~290
  - projects/stock-backtest/CLAUDE.md (Phase 1/2 트랙 분리)
  - projects/stock-backtest/.env.example (NAVER_DATALAB_* 추가)
date: 2026-05-12
verdict: NEEDS_REVISION
---

# Reviewer Report — Phase 2.1 분해 검증

## 1. 판정 요약

**NEEDS_REVISION** — 코어 설계와 의존성 그래프, 검증 명령은 모두 실측과 일치하지만 **TASK-300 의 "AssetType Literal 3곳 동기" 주장이 불완전**하다. 실측 결과 동일 Literal 이 **5곳**에 존재하며, 누락된 2곳 중 1곳(`backend/app/data/seed/assets_catalog.py:16`)은 진짜 `Literal` 타입 정의이므로 동기하지 않으면 추후 STOCK 시드 등록 시 mypy/pyright 가 잡는다. 나머지 2건은 docstring/주석이라 비-블로커지만 같이 정리하는 편이 클린코드 원칙에 부합. 또한 TASK-303 본문에 **"6 엔드포인트" 라고 적어두고 ①~⑧ 8개를 나열**한 카운트 불일치가 있어 Coder/Reviewer 가 DoD 검증 시 혼선을 일으킬 수 있다. 위 2가지를 수정하면 PASS 가능.

---

## 2. 검증 결과 — 항목별

### A. 파일 존재 / 실측 정확성

| Manager 주장 | 실측 결과 | 판정 |
|---|---|---|
| alembic head = `0004_fractional_qty` (down_revision='0003_backtest_tables') | `backend/alembic/versions/0004_fractional_qty.py:30` 의 `down_revision = "0003_backtest_tables"` 확인. 0001~0004 4 파일만 존재 (`__pycache__` 외) | PASS |
| `backend/app/domain/asset/entity.py:18` 에 `AssetType` Literal 정의 | 실측 L18: `AssetType = Literal["EQUITY_INDEX", "ETF", "BOND", "COMMODITY", "CRYPTO"]` — STOCK 부재 확인 | PASS |
| `backend/app/schemas/asset.py:17` 동일 Literal | 실측 L17 동일 — STOCK 부재 확인 | PASS |
| `frontend/lib/api/schemas.ts:38-45` `AssetTypeEnum` | 실측 L38-45 `z.enum(["EQUITY_INDEX","ETF","BOND","COMMODITY","CRYPTO"])` — STOCK 부재 확인 | PASS |
| `backend/app/main.py:130-133` 4 `include_router` | 실측 L130-133: `health_router, assets_router, strategies_router, backtests_router` 4건 — 정확 | PASS |
| `backend/app/data/asset_repository.py` 163줄 | `wc -l` = 163 | PASS |
| `backend/app/data/repositories/backtest_repository.py` 273줄 | `wc -l` = 273 | PASS |
| `backend/app/api/assets.py` 268줄 | `wc -l` = 268 | PASS |
| `backend/app/domain/themes/` 부재 | `ls backend/app/domain/` 결과: `allocators asset filters calendar.py dividend.py engine.py metrics.py portfolio.py strategy.py tax.py trade.py` — `themes/` 디렉토리 없음 | PASS (신규) |
| `frontend/app/themes/` / `components/themes/` / `hooks/useThemeChartData.ts` 부재 | `find ... -path '*themes*'` 결과 0 hit | PASS (신규) |
| `period_adjustment.adjust_period_for_universe` 재사용 가능 | `backend/app/domain/asset/period_adjustment.py:62` 에 정의 존재 | PASS |
| `calendar.align_universe_prices` 재사용 가능 | `backend/app/domain/calendar.py:73` 에 정의 존재 | PASS |
| `frontend/lib/api/types.ts` SoT 패턴 (TASK-238) | `frontend/lib/api/` = `client.ts schemas.ts types.ts` 3 파일 — 존재 | PASS |
| `backend/app/services/backtest_runner.py` (TASK-309 검증 대상) | `app/services/` = `__init__.py backtest_runner.py data_loader.py` — 존재 | PASS |
| `backend/app/dependencies.py` (TASK-303 수정 대상) | `find ... -name dependencies.py` → `/backend/app/dependencies.py` 1 hit | PASS |
| `frontend/components/backtest/UniverseSelector.tsx` (TASK-311 대상) | `find ...` 결과 존재 (`UniverseCard` 는 0 hit) | NOTE: TASK-311 에 "UniverseCard (또는 UniverseSelector.tsx)" 로 적혀 있어 OK |
| `backend/tests/architecture/` 신규 디렉토리 (TASK-309) | `ls` 실패 — 부재 확인. TASK-309 가 생성 | PASS |
| `backend/tests/data/` (TASK-302 신규 테스트 대상) | `ls backend/tests/` 결과에 `data` 존재 | PASS |
| `backend/tests/e2e/` (TASK-310 신규 테스트 대상) | `ls backend/tests/` 결과에 `e2e` 존재 | PASS |

**AssetType Literal "3곳 동기" 주장 — 누락 적발 (블로커)**:

`grep -rn "EQUITY_INDEX.*ETF.*BOND.*COMMODITY.*CRYPTO" backend frontend` 결과:

| 파일:라인 | 종류 | TASK-300 포함 여부 |
|---|---|---|
| `backend/app/domain/asset/entity.py:18` | 진짜 Literal 정의 | 포함 |
| `backend/app/schemas/asset.py:17` | 진짜 Literal 정의 | 포함 |
| `frontend/lib/api/schemas.ts:38-45` | 진짜 `z.enum` | 포함 |
| **`backend/app/data/seed/assets_catalog.py:16`** | **진짜 Literal 정의 (SeedAsset TypedDict 의 asset_type 필드 타입)** | **누락** |
| `backend/app/api/assets.py:132` | description 문자열 (FastAPI Query) — 사용자 노출 docstring | 누락 (UX 노이즈, 비-블로커) |
| `backend/app/models/asset.py:36` | 컬럼 위 주석만 | 누락 (비-블로커, 정보용 주석) |

→ **TASK-300 의 (c) DoD "AssetType Literal 3곳 grep 'STOCK' = 3 hits" 는 최소 "Literal/Enum 4곳 grep = 4 hits" 로 수정 필요**.

### B. 의존성 그래프 무결성

`Depends On` 컬럼 ↔ 그래프 대조:

| TASK | Depends On (테이블) | 그래프 표기 | 일치 |
|---|---|---|---|
| 300 | - | root | PASS |
| 301 | TASK-300 | 300→301 | PASS |
| 302 | TASK-301 | 301→302 | PASS |
| 303 | TASK-302 | 302→303 | PASS |
| 304 | TASK-301 | 301→304 | PASS |
| 305 | TASK-303, TASK-304 | 303→305 (304 의존 별기) | PASS |
| 306 | TASK-303 | 303→306 | PASS |
| 307 | TASK-306 | 306→307 | PASS |
| 308 | TASK-306 | 306→308 | PASS |
| 309 | TASK-301 | 301→309 | PASS |
| 310 | TASK-307, TASK-308, TASK-309 | 309·307·308→310 ("모두 완료 후" 표기) | PASS |
| 311 | TASK-310 | 310→311 | PASS |

→ **전 항목 일치**.

**병렬 충돌 검사**:

- 2차 (TASK-302 + TASK-304 + TASK-309 병렬):
  - 302 → `backend/app/data/theme_repository.py` (신규)
  - 304 → `backend/app/domain/themes/normalization.py` (신규)
  - 309 → `backend/tests/architecture/test_no_cross_import.py` (신규)
  - **충돌 0**
- 5차 (TASK-307 + TASK-308 병렬):
  - 307 → `frontend/app/themes/page.tsx`, `frontend/components/themes/{ThemeList, ThemeEditor, AssetPicker}.tsx`, `lib/i18n/ko.ts` (`theme.*` namespace)
  - 308 → `frontend/app/themes/[theme_id]/page.tsx`, `frontend/components/themes/charts/{NormalizedPriceChart, ThemeAggregateChart, ThemeCompareChart}.tsx`, `frontend/hooks/useThemeChartData.ts`
  - 두 태스크 모두 `frontend/components/themes/` 디렉토리에 파일 추가하지만 **서로 다른 파일명** + **307 은 components/themes/ 직하, 308 은 components/themes/charts/ 서브** 으로 분리.
  - **잠재 충돌 1건 (권고급)**: 둘 다 `lib/i18n/ko.ts` 의 `theme.*` namespace 를 건드릴 수 있음. TASK-307 에는 명시 (DoD "lib/i18n/ko.ts theme.* namespace 신규"), TASK-308 에는 i18n 언급 없음. 단 TASK-308 본문에 "recharts LineChart 다중 라인 + tooltip 한국어" 명시 → ko.ts 또는 컴포넌트 내 inline 라벨로 처리 가능. 병렬 실행 시 last-write-wins 충돌 잠재 위험.

### C. DoD 측정 가능성

각 태스크 DoD 의 PASS/FAIL 판정 가능성:

- **TASK-300**: (a) `alembic upgrade head` 성공 → 명령 명확. (b) 테이블 생성 확인 → `\dt` 또는 `pg_tables` 쿼리. (c) **"grep 3 hits" 주장은 실측 누락 1건으로 인해 "4 hits 이상" 으로 수정 필요 (블로커)**. (d) `pytest tests/api/test_api_contract.py` 회귀 0 — 명령 명확하나 "5/16 baseline" 표현이 모호 (실측 `def test_` = 11). → 권고: baseline 표현을 일반화하거나 정확히 인용.
- **TASK-301**: (a) banned imports 0 → `grep -E "^from sqlalchemy|^from fastapi" backend/app/domain/themes/` = 0 hit 로 강제 가능. (b) Protocol 8 메서드 → grep 명확. (c) 단위 테스트 5건 → pytest count 명확. PASS
- **TASK-302**: (a) Protocol 만족 → mypy/pyright 또는 isinstance 런타임 체크 명시. (b) 통합 테스트 5건 → 명확. PASS
- **TASK-303**: **본문 "6 엔드포인트" 라고 적고 ①~⑧ 8개 나열 + DoD (a) "8 엔드포인트 OpenAPI 등록"**. → **카운트 모순 (6 ≠ 8)** (블로커). Coder 가 6개만 구현하면 DoD 의 8 등록과 충돌.
- **TASK-304**: 단위 테스트 8건 + 수학적 성질 명시 → PASS
- **TASK-305**: 통합 테스트 3건 + OpenAPI 등록 → PASS. **데이터 의존**: theme 에 active 자산 + ohlcv 적재 필요 → "test fixture 로 mock" 명시 → PASS
- **TASK-306**: `tsc 통과`, `npm run build` PASS, round-trip 테스트 3건 → PASS
- **TASK-307**: 라우트 정적 빌드 + 한국어 라벨 grep 5건 + 단위 테스트 3건 → PASS
- **TASK-308**: 차트 라우트 빌드 + 단위 테스트 3건 → PASS
- **TASK-309**: importlib/ast 로 3 invariant 검증 → PASS. **검증 가능 패턴 명확** (banned imports grep).
- **TASK-310**: 회귀 baseline 모두 실측 검증됨:
  - **`pytest tests/golden/` 9/9** — 실측: snapshots/ 디렉토리에 9 JSON (3 scenario × 3 strategy). PASS
  - **`python -m scripts.validation.run_all` 11/11** — 실측: validation-report.md L7-14 (L1=5, L2=3, L3=1, L4=2 = 11). PASS
  - **`pytest tests/regression/` 50/50** — 실측: `grep -c "def test_"` = 23 (calendar_defense) + 8 (lookahead) + 19 (cash_by_ccy) = **50**. PASS
  - **`pytest tests/api/test_api_contract.py` 회귀 0** — 실측: `def test_` 함수 = 11. TASK-310 본문에 baseline 비교 표현 OK.
- **TASK-311**: 토스트 노출 + 단위 테스트 2건 → PASS

### D. 클린 아키텍처 / 격리 원칙

- TASK-301 "도메인 순수 (banned imports 0)" 강제 → TASK-309 가 정확히 이를 정적 검증으로 박제 (AST 또는 importlib). PASS
- TASK-309 격리 정적 검증 → architecture.md L1063-1067 "양방향 import 금지" 정책과 정확히 일치. 검증 대상 6 모듈 (engine/strategy/allocators/filters/trade/portfolio) 명시. **추가 권고**: TASK-309 invariant 3 ("backtest_runner.py 안에서 themes 의존 0 hit") 을 "services/* 전체에서 themes 의존 0 hit" 로 일반화하면 향후 회귀 방지에 더 강건. 현재 `app/services/` 에 backtest_runner.py + data_loader.py 2 파일 존재.
- TASK-303 단일 파일 크기 우려 → themes.py 에 6+2 = 8 endpoint + 2 차트 endpoint (TASK-305) = **총 10 endpoint**. 패턴 reference `assets.py` 268줄 (~12 endpoint) → themes.py 10 endpoint 약 220-260줄 예상. **단일 파일 우려 낮음**.

### E. 누락 / 과잉 점검

architecture.md "Phase 2.1" 범위 (L1083):
> Theme 모델 + DB 마이그레이션 + 기본 CRUD API + 화면 4 + 화면 5 정규화 차트(가격만)

task-board L228-260 매핑:

| Phase 2.1 항목 | 매핑 태스크 |
|---|---|
| Theme 모델 (DB) | TASK-300 |
| DB 마이그레이션 | TASK-300 |
| Theme 도메인 entity + service | TASK-301 |
| Repository | TASK-302 |
| 기본 CRUD API | TASK-303 |
| 정규화 도메인 | TASK-304 |
| 정규화 차트 API | TASK-305 |
| Frontend client | TASK-306 |
| 화면 4 | TASK-307 |
| 화면 5 정규화 차트 (가격만) | TASK-308 |
| 격리 정적 검증 | TASK-309 |
| e2e 회귀 | TASK-310 |
| C5 후속 | TASK-311 |

→ **Phase 2.1 범위 100% 커버**.

**Phase 2.2/2.3/2.4 항목이 섞였는지 검사**:

- 시가총액 수집 (`PykrxMarketCapSource` + cron + market_cap_weighting) → Phase 2.2 임에도 **TASK-300 이 `asset_market_cap` 테이블 생성을 포함**.
  - 분석: 테이블 생성 자체는 Phase 2.1 마이그레이션에서 미리 만들어둬도 무방 (DDL only, 데이터 흐름 0). market_cap weighting placeholder 도 TASK-304 가 "Phase 2.2 placeholder (NotImplementedError)" 로 명시 → **일관됨 (선반영, 비-과잉)**.
- 관심도 (NaverDataLab/GoogleTrends) → Phase 2.3 임에도 **`.env.example` 에 키 빈칸 선반영**.
  - 분석: architecture.md L977 + .env.example 끝 명시 "Phase 2.3 시작 직전 사용자 발급 후 채움" + TODO 코멘트. **정책 일관**.
- 테마 변경 이력 분석 도구 → Phase 2.4. task-board 에 0 hit.

→ **Phase 2.2/2.3 선반영은 정책 일치 + Phase 2.4 항목 0**. 과잉 없음.

### F. 정책 충돌 RESOLVED 일관성

architecture.md L19 / L93 / L520 / L740 갱신 ↔ L1069-1077 충돌 표 ↔ CLAUDE.md 미션 일관성:

| 충돌 | L1069 표 결정 | architecture 본문 | CLAUDE.md | 일관 |
|---|---|---|---|---|
| C1 | RESOLVED — ETF/지수 권고, Phase 2 STOCK 예외 + 생존편향 경고 | L19 정확 매핑 | "Phase 1 백테스팅 / Phase 2 관찰·탐색 트랙" 명시 | PASS |
| C2 | RESOLVED — `asset_type` 두 위치 STOCK 추가 | L93 + L520 STOCK 추가 + 설명 | 직접 언급 없음 | architecture 본문은 PASS, **TASK-300 의 코드 위치 카운트는 NEEDS_REVISION (A 항)** |
| C3 | RESOLVED — Phase 1/2 트랙 분리, 절대 원칙 1·5 양 트랙 | architecture L832: "V3 절대 원칙 (UI 폼 우선, 한국어, 진행 가시화 등) 은 동일 적용" — enumerate 만, "1·5 만" 직접 명시 없음 | CLAUDE.md L7: "절대 원칙 1·5 는 동일 적용되지만 2·3·4 는 백테스팅 트랙 전용" — 명확 | architecture 본문이 CLAUDE.md 보다 모호 (권고급 개선, 비-블로커) |
| C4 | RESOLVED — Phase 2 화면 5개 확장 | L740-743: "Phase 1 화면 3개" + "Phase 2 화면 5개" 명시 | 미언급 (절대 원칙 아님) | PASS |
| C5 | RESOLVED (정책) — 백테스트 화면 STOCK 경고 토스트, Phase 2.1 후속 별도 태스크 | task-board TASK-311 (Phase 2.1 후속) 분리 | 미언급 | PASS |

### G. 추가 검증 — 모델 무결성

- `backend/app/models/asset.py:37` `asset_type` 컬럼 = `String(32)` (NO ENUM) → TASK-300 의 "Python 정적 Literal 변경, DB ENUM 미사용이므로 alembic 본문 변경 없음" 주장 정확. STOCK 값 삽입은 String column 에 즉시 가능.
- TASK-300 의 "`__init__.py` re-export 갱신" → 실측 `backend/app/models/__init__.py` 존재. 신규 `theme.py` + `market_cap.py` 추가 시 re-export 패턴 따름. DoD 에 명시되어 있어 PASS.

---

## 3. Manager 수정 사항 (NEEDS_REVISION → PASS 조건)

### 필수 (블로커)

1. **`signal/stock-backtest/task-board.md` TASK-300 본문 — AssetType 동기 위치 카운트**:
   - 현재: "**AssetType Literal 3곳 동기** ... `backend/app/domain/asset/entity.py:18` + `backend/app/schemas/asset.py:17` + `frontend/lib/api/schemas.ts:38-45`"
   - 수정 (예시):
     ```
     AssetType Literal/Enum 4곳 동기 (mypy/pyright 강제 대상):
     - backend/app/domain/asset/entity.py:18 (Literal 정의)
     - backend/app/schemas/asset.py:17 (Literal 정의)
     - backend/app/data/seed/assets_catalog.py:16 (Literal 정의 — Reviewer 적발)
     - frontend/lib/api/schemas.ts:38-45 (AssetTypeEnum — z.enum 정의)
     추가 docstring/주석 정리 (비-블로커): backend/app/api/assets.py:132 description 문자열 + backend/app/models/asset.py:36 comment.
     ```

2. **`signal/stock-backtest/task-board.md` TASK-300 DoD (c)**:
   - 현재: "(c) AssetType Literal 3곳 grep 'STOCK' = 3 hits"
   - 수정: "(c) AssetType Literal/Enum 4곳 STOCK 추가: `grep -nE 'STOCK' backend/app/domain/asset/entity.py backend/app/schemas/asset.py backend/app/data/seed/assets_catalog.py frontend/lib/api/schemas.ts` = 4 hits 이상"

3. **`signal/stock-backtest/task-board.md` TASK-303 본문 — 엔드포인트 카운트 모순**:
   - 현재: "**6 엔드포인트**: ①... ⑧..." (6 ≠ 8 모순)
   - 수정 (단순): "**8 엔드포인트**: ①... ⑧..."
   - 또는 (분리): "**themes.py 6 엔드포인트 + assets.py 1 endpoint 추가 (`/assets/{asset_id}/theme_history`) + dependencies.py 1 endpoint 의존성 추가 = 본 태스크 8 라우트 영향**" — DoD (a) 의 "8 엔드포인트 OpenAPI 등록" 과 정합.

### 권고 (비-블로커, 향후 회귀 방지)

4. **`signal/stock-backtest/task-board.md` TASK-308 DoD 끝에 추가**: "`lib/i18n/ko.ts` 수정 금지 — TASK-307 에서 정의한 `theme.*` namespace 의 sub-key 만 재사용. 신규 차트 라벨이 필요하면 TASK-307 namespace 에 미리 포함시킬 것."

5. **`signal/stock-backtest/architecture.md` L832** (C3 일관성 강화):
   - 현재: "V3 절대 원칙 (UI 폼 우선, 한국어, 진행 가시화 등) 은 동일 적용한다"
   - 권고: "CLAUDE.md 절대 원칙 1·5 (JSON 미노출, 프리셋 제한) 만 동일 적용. 2·3·4 (3요소 전략 / 실거래 70% / 메트릭) 는 백테스팅 트랙 전용 — 본 트랙 무관."

6. **`signal/stock-backtest/task-board.md` TASK-309 invariant 3**:
   - 현재: "`backend/app/services/backtest_runner.py` 안에서 themes 의존 0 hit"
   - 권고: "`backend/app/services/**` 전체에서 themes 의존 0 hit" — 향후 services/ 새 모듈 추가 시 회귀 방지.

7. **`signal/stock-backtest/task-board.md` TASK-300 DoD (d) — baseline 표현 명확화**:
   - 현재: "`pytest tests/api/test_api_contract.py` 회귀 0 (기존 5/16 baseline 유지)"
   - 권고: "Coder 가 호출 직전 `pytest --co -q backend/tests/api/test_api_contract.py` 로 현재 baseline (예상 11 collected) 측정 후 STOCK 추가 후 동일 측정으로 비교 — PASS/FAIL 비율 동일 유지" — "5/16" 의 의미가 11 def 와 정합하지 않음.

---

## 4. PASS 조건

위 **필수 1·2·3 (TASK-300 본문 + DoD c, TASK-303 본문 카운트)** 만 수정하면 **PASS**. 권고 4~7 은 동일 PR 에 포함하면 견고하나 PASS 차단 요소 아님.

수정 후 Manager 가 재호출하면 Reviewer 는 task-board.md L244 / L247 만 재독해 즉시 PASS 판정 가능.

---

## 5. 검증 명령 (Reviewer 가 실행한 실측 명령)

```bash
ls backend/alembic/versions/                                      # 0001~0004 확인
grep -rn "down_revision\|revision = " backend/alembic/versions/*.py
grep -rn "EQUITY_INDEX.*ETF.*BOND" backend frontend/lib            # AssetType 5곳 적발
wc -l backend/app/data/asset_repository.py \
     backend/app/data/repositories/backtest_repository.py \
     backend/app/api/assets.py                                     # 163/273/268 일치
ls backend/app/domain/                                            # themes/ 부재
find frontend -path '*themes*' -not -path '*/node_modules/*'      # 0 hit
ls backend/app/models/                                            # _base.py 존재
grep -rcE "    def test_|^def test_" backend/tests/regression/*.py # 50 total
ls backend/tests/golden/snapshots/                                # 9 JSON
grep -n "11/11" signal/stock-backtest/validation-report.md        # 11/11 확인
ls backend/tests/architecture/                                    # 부재 (신규)
ls backend/app/services/                                          # backtest_runner.py, data_loader.py
find . -name dependencies.py                                      # backend/app/dependencies.py
find frontend/components -name "UniverseSelector*"                # 존재
```

— Reviewer Agent

---

## r2 (2026-05-12, NEEDS_REVISION → PASS 재검증)

### 1. 판정 요약

**PASS** — r1 의 블로커 3건 모두 정확히 해소되었고, 권고 4 / 6 도 반영되었다. 미반영 권고 2 (architecture.md L832 명확화) 는 CLAUDE.md L8 본문에서 적용 범위가 이미 정확히 박혀 있으므로 Manager 의 보류 판단이 합리적이다. Coder 가 **TASK-300 부터 시작 가능**.

### 2. r2 검증 결과 — 항목별 (재실측 + diff 검증)

#### A. 블로커 3건 해소 확인

| 블로커 | r2 수정 위치 | 실측 인용 | 판정 |
|---|---|---|---|
| ① TASK-300 본문 "Literal 3곳" → "4곳" | task-board.md L238 + L245 | L238: "`AssetType` Literal **4곳** 동기 필요 (Reviewer 2026-05-12 NEEDS_REVISION 반영): `backend/app/domain/asset/entity.py:18`, `backend/app/schemas/asset.py:17`, `backend/app/data/seed/assets_catalog.py:16`, `frontend/lib/api/schemas.ts:38-45` (`AssetTypeEnum`)" — 4 위치 전부 명시. L245: "**AssetType Literal 4곳 동기** ... 4 위치: ① ... ② ... ③ ... ④ ..." 동일 4 위치 번호 부여 | PASS |
| ② TASK-300 DoD (c) "3 hits" → "4 hits 이상" + grep 명령 | task-board.md L245 DoD (c) | "(c) `grep -rn "STOCK" backend/app/domain/asset/entity.py backend/app/schemas/asset.py backend/app/data/seed/assets_catalog.py frontend/lib/api/schemas.ts` 에서 "STOCK" Literal 멤버 등장 **4 위치 모두**" — 구체 grep 명령 + "4 위치 모두" 표현 (3 hits 라는 carry-over 카운트 부재) | PASS |
| ③ TASK-303 본문 "6 엔드포인트" + DoD (a) "8 엔드포인트" 모순 | task-board.md L248 | 본문 "**8 엔드포인트** (Reviewer 2026-05-12 적발 — 본문 "6" → "8" 정정): ①... ⑧..." + DoD (a) "**8 엔드포인트** OpenAPI 등록" — 본문 카운트 + DoD 카운트 + ①~⑧ 8개 enum 모두 일관 (8) | PASS |

**추가 점검**: `grep -nE '"STOCK"\|'\''STOCK'\''' projects/stock-backtest/backend/app projects/stock-backtest/frontend/lib` → 4 위치 모두 **STOCK 부재** (models/backtest.py:77 / repositories/backtest_repository.py:81 은 `market_mode` 컬럼 / 변수로 AssetType 와 무관, TASK-300 동기 대상 4 위치는 정확히 STOCK 부재 상태 — Coder 가 추가하면 4 hits 발생). 실측 일치.

#### B. 권고 반영 일관성

| 권고 | r2 수정 위치 | 실측 인용 | 판정 |
|---|---|---|---|
| 권고 1 (TASK-308 ko.ts 수정 금지 명시) | task-board.md L253 본문 + DoD (d) | 본문: "**충돌 방지** (Reviewer 권고 2026-05-12): `lib/i18n/ko.ts` 의 `theme.*` namespace 추가는 **TASK-307 전담** — 본 태스크는 ko.ts 의 기존 키 사용만 허용 ... 병렬 last-write-wins 방지." + DoD (d): "`lib/i18n/ko.ts` 수정 라인 = 0 (충돌 방지 정책)" — TASK-307 (`theme.*` namespace 신규) 와 책임 경계 명확 분리 | PASS |
| 권고 3 (TASK-309 invariant ③ services 전체 일반화) | task-board.md L254 | "③ `backend/app/services/**` 전체 (현재 `backtest_runner.py` + `data_loader.py`, 향후 추가될 모듈 포함) 에서 `from app.domain.themes` 또는 `from app.data.theme_repository` import 0 hit (Reviewer 권고 2026-05-12 — 단일 파일 → services 전체 일반화)" — services/** 일반화 + theme_repository import 도 추가 검사 (data 레이어 격리까지 박제) | PASS |
| 권고 4 (TASK-300 DoD (d) baseline "5/16" 모호 → 명확화) | task-board.md L245 DoD (d) | "`pytest tests/api/test_api_contract.py` 회귀 0 (현 baseline: 5 PASS + 6 SKIP, `def test_` 정의 11건 — DB-의존 SKIP 은 BLOCKER-001 잔재)" — "5/16" 의 모호한 표현이 "5 PASS + 6 SKIP" + `def test_` 11 + SKIP 원인 (BLOCKER-001) 까지 명시되어 측정 가능 | PASS |

**미반영 권고 2 (architecture.md L832 명확화) 의 합리성 검증**:

- CLAUDE.md L8 (실측): "절대 원칙 1·5 (JSON 미노출, MVP 프리셋 제한) 는 동일 적용되지만 2·3·4 (3요소 전략, 실거래 70%, 메트릭) 는 백테스팅 트랙 전용." — **적용 범위 1·5 vs 2·3·4 가 본문에 명시적으로 박혀 있음**.
- architecture.md L832 (실측): "V3 절대 원칙 (UI 폼 우선, 한국어, 진행 가시화 등) 은 동일 적용한다." — 표현은 모호하지만 "동일 적용" 의 범위는 CLAUDE.md L8 + L1069-1077 결정 표 (C3 RESOLVED) 가 권위적 출처.
- **판단**: Manager 의 "CLAUDE.md 본문 명시 + L1069 결정 표 박제 → architecture.md L832 단독으로는 추가 명확화 불필요" 주장 합리적. Coder 가 L832 단독을 읽어도 같은 페이지의 결정 표로 즉시 disambiguate 가능. 단독 PR 가치 < diff 비용. **합의 + 비-블로커 보류 OK**.

#### C. 신규 위험 점검 (6 수정 → 의존성 그래프 / 다른 태스크 영향)

| 영향 검사 항목 | 결과 | 판정 |
|---|---|---|
| 의존성 그래프 (L266-289) 변경 여부 | 그래프 L266-279 + 병렬 계획 L281-289 — diff 0 (블로커 수정은 본문/DoD 만 갱신, depends_on 컬럼 무변경) | PASS |
| TASK-306 (Frontend Zod) 의 "AssetTypeEnum STOCK 추가" — TASK-300 동기 위치 4곳 중 frontend/lib/api/schemas.ts:38-45 와 일관 | L251: "① `AssetTypeEnum` L38-45 에 `"STOCK"` 추가 (TASK-300 백엔드 동기)" — 동일 위치 + "TASK-300 백엔드 동기" 명시. 4곳 중 4번째 위치 (frontend) 의 동기 책임이 TASK-306 으로 위임됨 (백엔드 3곳은 TASK-300, frontend 1곳은 TASK-306). 책임 경계 명확 | PASS |
| TASK-307 의 ko.ts namespace 신규 책임 vs TASK-308 의 수정 금지 정책 일관 | TASK-307 L252 (i18n/ko.ts theme.* namespace 신규 — DoD (b) 한국어 라벨 grep 5건 이상) ↔ TASK-308 L253 DoD (d) "수정 라인 = 0" — TASK-307 이 모든 신규 키를 사전 정의하고 TASK-308 은 reuse 만. **last-write-wins 방지** 정책으로 병렬 실행 가능 (5차 병렬, L285) | PASS |
| TASK-309 services/** 일반화로 향후 `app/services/` 신규 모듈 추가 시 회귀 자동 차단 | invariant ③ 가 `from app.domain.themes` + `from app.data.theme_repository` 양쪽 import 0 hit 강제 — Phase 2.2 (market_cap 수집 서비스) 추가 시 위반 검출됨 | PASS (회귀 방지 강화) |
| TASK-303 의 "8 엔드포인트" 중 ⑧ (`GET /api/assets/{asset_id}/theme_history`) 은 assets.py 라우터에 append → TASK-305 (themes.py 차트 2 endpoint) 와 파일 충돌? | TASK-305 L250 본문: "`backend/app/api/themes.py` (TASK-303 후) 에 차트 endpoint 2건 추가" — themes.py 동일 파일이지만 **TASK-303 → TASK-305 순차** (의존성 L283 "3차 (TASK-302 + TASK-304 후): TASK-303 → TASK-305 순차 (themes.py 동일 파일)") 명시. ⑧ 는 assets.py append 라 themes.py 와 무관. 순차 + 파일 분리로 충돌 0 | PASS |

### 3. r2 종합 판정

- **블로커 3건 100% 해소** (TASK-300 본문 + DoD c, TASK-303 본문/DoD a 일관)
- **권고 4건 중 3건 반영** (1 ko.ts 충돌 / 3 services 일반화 / 4 baseline 명확화)
- **미반영 권고 1건** (architecture.md L832) — CLAUDE.md L8 + L1069 결정 표가 권위 → 보류 합리
- **신규 위험 0** (의존성 그래프 / 병렬 계획 / 책임 경계 모두 일관)

**최종 판정: PASS**

Manager 는 **TASK-300 부터 Coder 호출** 가능. r2 추가 수정 불필요.

### 4. PASS 조건 charter (다음 라운드 호출 시 참조)

- TASK-300 코드 수정 후 다음 grep 으로 4 위치 동기 확인:
  ```bash
  grep -nE '"STOCK"|'\''STOCK'\''' \
    projects/stock-backtest/backend/app/domain/asset/entity.py \
    projects/stock-backtest/backend/app/schemas/asset.py \
    projects/stock-backtest/backend/app/data/seed/assets_catalog.py \
    projects/stock-backtest/frontend/lib/api/schemas.ts
  # 기대: 4 hits (각 파일 정확히 1개)
  ```
- TASK-303 themes.py + assets.py append 후 OpenAPI 등록 검증:
  ```bash
  curl -s http://localhost:8000/api/openapi.json | jq '.paths | keys[] | select(test("theme"))'
  # 기대: 7 keys (themes 6 라우트 + assets/{id}/theme_history 1) — themes.py 의 ① POST 와 ② GET /api/themes 가 동일 path 다른 method 이므로 path key 단위로는 7개
  ```

— Reviewer Agent (r2)
