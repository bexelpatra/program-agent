# Done Log

V3 Phase 1 MVP 완료 태스크 append-only 로그.

### Phase 2 리팩토링 (TASK-235/237 DONE) - 2026-04-30T15:50

2 태스크 병렬 (backend + frontend 영역 분리). Reviewer 사전 검증 NEEDS_REVISION (TASK-237 라인 시프트 8줄 — Phase 1 의 TASK-238 import 정리 영향) → Manager 정정 후 Coder 호출.

- **TASK-235** (source 라우팅 단일화): `data/sources/__init__.py` 에 `get_source_for_market(market, *, yfinance, pykrx) -> DataSource` factory. `api/assets.py` `_RoutingValidator` + `scheduler/cron_jobs.py` `sources_by_market` dict 양쪽 호출 통합. 신규 시장 추가 시 한 곳만 수정.
- **TASK-237** (BacktestResultView 추출): 신규 컴포넌트 (133줄) + `layout: "compact" | "full"` prop. `new/page.tsx` 786→712줄, `[run_id]/page.tsx` 284→237줄. `__tests__/BacktestResultView.test.tsx` 4 tests + 2 snapshots. 시각화 5개 컴포넌트 import 두 페이지에서 0건 (단일 진입점화).
  - 부수: `vitest.config.ts` 에 `esbuild.jsx='automatic'` 추가 (`.tsx` 테스트 도입을 위한 환경 설정).
- **통합 회귀**: backend 123 passed (Phase 1 baseline 일치, 회귀 0). frontend tsc 0 + build PASS + vitest 10/10.
- **병렬 충돌**: 0건.

### Phase 1 리팩토링 일괄 (TASK-230/231/232/233/234/236/238 DONE) - 2026-04-30T15:00

7 태스크 병렬 실행 (backend 6 + frontend 1). Reviewer 사전 검증 R1 NEEDS_REVISION → R2 PASS 거쳐 Coder 동시 호출.

- **TASK-230** (source 어댑터 헬퍼 추출): `_helpers.py` 신규 (RateLimiter / safe_float / is_invalid_close). yfinance/pykrx 합산 -63줄. backward-compat alias 유지 (regression test 의 직접 import 보호).
- **TASK-231** (allocator 검증 통합): `_validation.py` 신규 + `validate_weight_dict(allow_empty=...)` 1 함수. 3 allocator 1줄 위임. **관찰**: IEEE 754 boundary — 0.95/1.05 거부 (기존 동작 보존, math.isclose 전환은 별도 태스크 후보).
- **TASK-232** (`_persist_results` 분해): 85줄 → 3 헬퍼 (`_build_equity_rows` / `_build_trade_dicts` / `_compute_and_flatten_metrics`) + `_persist_results` 22줄. 11 신규 단위 테스트.
- **TASK-233** (calendar_guard 사적 import): `get_calendar_name(market) -> str | None` (unknown=None graceful). pipeline.py 사적 import 0 hit. 6 신규 단위 테스트.
- **TASK-234** (페이지네이션 total): `asset_repository.count()` + `backtest_repository.count_runs()` 신규 public 메서드. 2 라우터 `total=len(...)` → `repo.count(...)` 교체. 4 신규 테스트.
- **TASK-236** (registration silent swallow): `import logging` + logger.warning(asset_id/symbol/exc). 3 신규 caplog 단위 테스트.
- **TASK-238** (BacktestResult/Asset 타입 통합): `lib/api/types.ts` 신규 (z.infer SoT). `z.record(z.any())` 7회 → `z.record(z.unknown())`. `as Record<...>` 캐스트 1건 제거. `Awaited<ReturnType<...>>` 트릭 3 호출처 제거.
- **통합 회귀**: backend 123 passed (api fuzz/e2e 제외 — pre-existing baseline), frontend tsc 0 에러, npm build PASS.
- **병렬 충돌**: 0건 (git status 깨끗, 7 Coder 가 각자 영역만 수정).
- **관찰 후속 후보**: (1) IEEE 754 boundary (math.isclose), (2) AssetTable.tsx 도 listAssets 트릭, (3) test_api_contract.py 5 fuzz failure (pre-existing baseline).

### TASK-001 (DONE) - 2026-04-29T07:55
- title: 프로젝트 스캐폴드 (backend/frontend, requirements/package.json, .env.example, README, Docker Compose Postgres+TimescaleDB)
- assignee: coder
- summary: backend (FastAPI/SQLAlchemy 2.0/Alembic/pandas 2.2/numpy 2.0/yfinance/pykrx/exchange_calendars/APScheduler 17개) + frontend (Next 14.2/React 18/TS strict/Zod/tailwind 3.4/recharts/next-intl/vitest) 스캐폴드. PostgreSQL+TimescaleDB Docker Compose, .env.example (TZ=Asia/Seoul, DEFAULT_BASE_CURRENCY=KRW), 한국어 README. DoD 4개 (`pip install`, `python -c 'import app'`, `npm install`, `npm run build`) 모두 PASS.
- files: projects/stock-backtest/backend/{requirements.txt, app/__init__.py + 9개 서브패키지 __init__, scripts/smoke_imports.py, alembic/.gitkeep, tests/__init__.py}, projects/stock-backtest/frontend/{package.json, tsconfig.json, next.config.mjs, postcss.config.mjs, tailwind.config.ts, .eslintrc.json, .gitignore, app/{layout.tsx, page.tsx, globals.css}, components/{ui,strategy,backtest,asset}/.gitkeep, lib/.gitkeep, hooks/.gitkeep}, projects/stock-backtest/{docker-compose.yml, .env.example, .gitignore, README.md}
- 의존성 충돌: 없음 (numpy 2.0.2 + pandas 2.2.3 + yfinance 0.2.66 + pykrx 1.2.7 ABI 정상)

### TASK-002 (DONE) - 2026-04-29T08:05
- title: SQLAlchemy + Alembic 초기 설정
- assignee: coder
- summary: pydantic-settings 기반 Settings (database_url/default_base_currency=KRW/tz) + SQLAlchemy 2.0 engine/SessionLocal/Base/get_db() + alembic init + alembic/env.py 가 Settings 의 database_url 동적 주입. config.py 환경변수만, db.py SQLAlchemy 객체만 단방향 의존.
- files: projects/stock-backtest/backend/{alembic/{env.py, script.py.mako, versions/}, alembic.ini, app/core/config.py, app/core/db.py}
- DoD: import 검증 1·2 PASS. `alembic current` 는 SOFT BLOCKER-001 (DB 잔재 alembic_version='0003') — TASK-010 baseline 작성 시 처리.

### TASK-060 (DONE) - 2026-04-29T08:05
- title: docs/openapi.yaml 초안 + FastAPI 스캐폴드 + 전역 예외 핸들러 + 공통 base 스키마
- assignee: coder
- summary: FastAPI app (Quant Lab API 0.1.0, /api prefix, CORS for localhost:3000) + 전역 예외 핸들러 (HTTPException/RequestValidationError/Exception → ErrorResponse with stage/type/message/request_ctx/trace_id, 서버 로그 접두사 동일) + GET /api/health + 공통 schemas (ErrorDetail/ErrorResponse frozen, PaginatedResponse[T] Generic, TimestampedModel, HealthResponse) + docs/openapi.yaml (OpenAPI 3.1.0). DoD 5/5 통과 (라우트 등록, /api/health 200, /api/nonexistent ErrorResponse+trace_id, openapi.json 4종 schema, openapi.yaml safe_load).
- files: projects/stock-backtest/backend/app/{main.py, api/__init__.py, api/_error.py, api/health.py, schemas/common.py}, projects/stock-backtest/docs/openapi.yaml
- TASK-002 충돌: 0건 (core/ 미터치, alembic/ 미터치, app/__init__.py 미수정)

### TASK-010 (DONE) - 2026-04-29T08:25
- title: 마스터 테이블 alembic 마이그레이션 (assets, ingestion_log)
- assignee: coder
- summary: SQLAlchemy 2.0 typed Mapped 스타일 ORM 2종 (Asset 12 컬럼 - JSONB meta, UNIQUE(symbol,market), TimestampedModel mixin / IngestionLog 8 컬럼 - FK CASCADE, immutable 이벤트라 mixin 미적용) + alembic baseline migration `0001_v3_baseline` (down_revision=None, indexes 4개 ix_assets_market/symbol/active + ix_ingestion_log_asset_id) + DB 초기화 가이드 README. status 는 String(16) + Pydantic Literal 권장 (Postgres ENUM 미사용). market_events 미생성 (Phase 2 이월). DoD 1·2·5 PASS, 3 OK (heads=0001_v3_baseline), 4 SOFT (BLOCKER-001 잔재로 사용자 DB 초기화 후 적용).
- files: projects/stock-backtest/backend/{app/models/{_base.py, asset.py, ingestion_log.py, __init__.py}, alembic/{versions/0001_v3_baseline.py, README.md}}
- BLOCKER-001 갱신: PARTIAL (사용자가 docker volume drop 또는 schema drop 후 alembic upgrade head 실행 필요)

### TASK-003 (DONE) - 2026-04-29T08:50
- title: 자산 카탈로그 시드 데이터 (KR/US/CRYPTO 67개)
- assignee: coder
- summary: TypedDict 기반 SeedAsset 67개 - KR 20 (domestic 8/overseas 5/bond 5/commodity 2), US 35 (광역7/섹터5/채권8/원자재6/부동산2/해외7), CRYPTO 12. asset_type: ETF 34/BOND 12/CRYPTO 12/COMMODITY 9. 한국 ETF 는 거래소 공식 한글명. seed_catalog.py CLI 가 ON CONFLICT DO UPDATE 멱등 UPSERT.
- files: projects/stock-backtest/backend/app/data/seed/{__init__.py, assets_catalog.py}, projects/stock-backtest/backend/scripts/seed_catalog.py

### TASK-011 (DONE) - 2026-04-29T08:50
- title: 시계열 테이블 마이그레이션 (ohlcv hypertable + fx_rates + corporate_actions)
- assignee: coder
- summary: SQLAlchemy 2.0 typed Mapped ORM 3종 + alembic `0002_timeseries_tables` (down_revision=0001_v3_baseline). ohlcv close NOT NULL (비거래일 방어 수집 레이어), Numeric(20,8) 가격/Numeric(20,0) 수량, timezone-aware. hypertable 변환 try/except 로 일반 PG 호환. CreateTable SQL + alembic dry-run + history 그래프 모두 PASS.
- files: projects/stock-backtest/backend/app/models/{ohlcv.py, fx_rates.py, corporate_actions.py, __init__.py}, projects/stock-backtest/backend/alembic/versions/0002_timeseries_tables.py

### TASK-030 (DONE) - 2026-04-29T08:50
- title: Asset/Universe 도메인 모델 + Repository + 비거래일 방어 조회 레이어
- assignee: coder
- summary: backend/app/domain/asset/ 신규 패키지 (Asset/Universe frozen dataclass, AssetRepository Protocol 6개 메서드, calendar_guard XKRX/XNYS/CRYPTO 24-7) + backend/app/data/asset_repository.py SqlAssetRepository 구현 (의존성 역전, _to_entity 매핑 일원화, on_conflict_do_update upsert). 도메인 순수성 검증 PASS (banned imports 0). exchange_calendars 의 date_to_session(direction) API 사용.
- files: projects/stock-backtest/backend/app/domain/asset/{__init__.py, entity.py, repository.py, calendar_guard.py}, projects/stock-backtest/backend/app/data/asset_repository.py, projects/stock-backtest/backend/app/{domain,data}/__init__.py
- 신규 public API: AssetRepository (find_by_id, find_by_symbol_market, search, list_active, upsert, update_ingestion_state) + Universe (common_period, assets_by_currency) + calendar_guard (is_trading_day, guard_trading_day)

### TASK-012 (DONE) - 2026-04-29T09:15
- title: 백테스트 테이블 마이그레이션 (alembic 0003 - backtest_runs/equity/trades/metrics)
- assignee: coder
- summary: SQLAlchemy 2.0 ORM 4종 (한 파일 backtest.py - 응집도) + alembic 0003_backtest_tables (down=0002). backtest_runs(run_hash UNIQUE, status/progress/cancel_requested/error_json JSONB - 비동기 job + V2 에러 계약), backtest_equity(hypertable), backtest_trades(side CHECK IN BUY/SELL - V3 FX 미기록 정책 강제), backtest_metrics(UNIQUE run_id+name). universe JSONB 스냅샷, trades.asset_id RESTRICT. 9개 테이블 metadata 확인. alembic dry-run + history 직선.
- files: projects/stock-backtest/backend/{app/models/{backtest.py, __init__.py}, alembic/versions/0003_backtest_tables.py}

### TASK-020 (DONE) - 2026-04-29T09:15
- title: DataSource/FxSource Protocol + yfinance 어댑터 (US/Crypto/FX)
- assignee: coder
- summary: backend/app/data/sources/{base.py, yfinance_source.py} - DataSource(ticker)/FxSource(통화 페어) 분리, OhlcvBar/FxBar/DividendEvent/TickerValidation frozen dataclass. close=0/null/NaN 거부 (수집 레이어 방어). module-level lock + 0.5s sleep rate limit (V1 결정 9). validate_ticker 3초 이내 검증 - SPY=True, XYZNOTEXIST=False 실측. fetch_ohlcv 10일 SPY 7 bars. USD/KRW validate_pair True. pykrx/pyupbit 후속 어댑터 plug-in 가능.
- files: projects/stock-backtest/backend/app/data/sources/{__init__.py, base.py, yfinance_source.py}, projects/stock-backtest/backend/app/data/__init__.py
- 신규 public API: DataSource/FxSource Protocol, OhlcvBar/FxBar/DividendEvent/TickerValidation dataclass, YfinanceSource/YfinanceFxSource

### TASK-032 (DONE) - 2026-04-29T09:15
- title: universe 시작일 교집합 자동 산출 + 한국어 통지 메시지
- assignee: coder
- summary: backend/app/domain/asset/period_adjustment.py - PeriodAdjustment frozen dataclass + adjust_period_for_universe() + AdjustmentReason Literal. 6 케이스 (빈 universe / start_date None / 완전 포함 / 시작일 조정 / 종료일 조정 / 양쪽 조정) 모두 PASS. 한국어 통지 메시지 (UI/UX 원칙 2), affected_assets 추적. 도메인 순수 (stdlib + entity 만).
- files: projects/stock-backtest/backend/app/domain/asset/{period_adjustment.py, __init__.py}
- 관찰: 양쪽 조정 시 affected_assets 중복 entry 가능 - UI dedup 또는 후속에서 affected_start/end 분리 검토

### TASK-021 (DONE) - 2026-04-29T09:35
- title: pykrx 어댑터 (KR 주식/ETF) — DataSource Protocol 구현
- assignee: coder
- summary: PykrxSource (DataSource structural typing 통과). KST timezone 강제, 100ms rate limit (별도 lock), 수집 레이어 방어 (close=0/null/NaN 거부). validate_ticker('069500') exists=True / ('999999') exists=False 한국어 note 실측. fetch_ohlcv 7 bars KODEX 200. fetch_dividends 빈 구현 → BLOCKER-002 SOFT 등록. adj_close = close (split/dividend 보정 향후).
- files: projects/stock-backtest/backend/app/data/sources/{pykrx_source.py, __init__.py}, projects/stock-backtest/backend/app/data/__init__.py
- BLOCKER-002 SOFT: pykrx 한국 ETF 분배금 미지원 — UI 에 "KR 자산 배당 미반영" 안내 필요

### TASK-040 (DONE) - 2026-04-29T09:35
- title: Portfolio + cash_by_ccy + 환전 엔진 (V3 의 핵심 도메인)
- assignee: coder
- summary: backend/app/domain/portfolio.py 290줄. B 모델 cash_by_ccy[ccy] + Decimal 정밀도 (float 0건). Q3 C 단계 분리 + Q5 B native 우선 (ensure_native_funds: native 충분이면 환전 0회). 20bp spread 양방향 비용. FX 미기록 (FxConversion 감사용 dataclass, side/asset_id 없음). buy/sell partial fill (cash 부족 시 max_affordable 정수, 음수 잔고 구조적 차단). 도메인 순수 (dataclasses/decimal/typing 만). 단위 검증 10/10 PASS.
- files: projects/stock-backtest/backend/app/domain/{portfolio.py, __init__.py}
- 신규 public API: Portfolio (cash, total_cash_in_base, positions_value_in_base, equity_in_base, convert, ensure_native_funds, buy, sell, deposit), Position, FxConversion, InsufficientFundsError, DEFAULT_FX_SPREAD_BPS, DEFAULT_SLIPPAGE_BPS

### TASK-022 (DONE) - 2026-04-29T09:55
- title: 증분 파이프라인 (백필 + 갭 감지 + 멱등 UPSERT + 비거래일 방어 수집/캘린더 + 재시도)
- assignee: coder
- summary: backend/app/data/pipeline.py + repositories/{ohlcv_repository, ingestion_log_repository}. MAX(time)+1부터 백필 (신규 자산 20년 lookback). 캘린더 2중 방어 (expected_days 산출 + source 응답 필터). 자산 단위 try/except + commit/rollback 격리, 3회 재시도 1·2·4초 백오프. UPSERT SQL `ON CONFLICT (asset_id,time) DO UPDATE SET...=excluded.*` 컴파일 PASS. _trading_days US 21/KR 22/CRYPTO 31 실측.
- files: projects/stock-backtest/backend/app/data/{pipeline.py, repositories/{__init__.py, ohlcv_repository.py, ingestion_log_repository.py}, __init__.py}
- 신규 public API: OhlcvRepository(latest_time, existing_dates, upsert_bars), IngestionLogRepository(record), backfill_asset, backfill_active_assets, IngestionResult

### TASK-041 (DONE) - 2026-04-29T09:55
- title: trade.py 거래 실행 엔진 (시장별 수수료/슬리피지 + 비거래일 방어 엔진 레이어 + 리밸런싱 시퀀스)
- assignee: coder
- summary: backend/app/domain/trade.py 345줄. DEFAULT_COMMISSION_BPS (KR 1.5/US 0.5/CRYPTO 10), execute_rebalance 4 헬퍼 분리 (Q3 C SELL→BUY, Q5 B native 우선, base 환전은 Portfolio.ensure_native_funds 위임). assert_trading_day_for_universe + assert_all_assets_priced 명시 에러 (silent 0 금지). is_trading_day_fn DI 로 mock 가능. 통합 미니 시나리오: KRW 1M, KR 자산 100% 매수 → 99주 + commission 148.6485 KRW + 잔여 8861.3515 KRW 정확.
- files: projects/stock-backtest/backend/app/domain/{trade.py, __init__.py}
- 신규 public API: DEFAULT_COMMISSION_BPS, NonTradingDayError, MissingPriceError, TradeOrder, TradeFill, commission_bps_for, assert_all_assets_priced, assert_trading_day_for_universe, execute_rebalance

### TASK-042 (DONE) - 2026-04-29T09:55
- title: calendar.py 멀티 마켓 캘린더 정렬 (base_currency 기준 + forward-fill)
- assignee: coder
- summary: backend/app/domain/calendar.py 105줄. BASE_CCY_TO_CALENDAR (KRW→XKRX, USD→NYSE), trading_days_in_period, align_market_price_to_base_calendar (forward-fill만 - back-fill 금지 look-ahead 방지), align_universe_prices (누락 자산은 dict 제외), next/previous_trading_day (비거래일 input 도 처리). KR 2024-01 22 거래일, forward-fill 4 케이스 (exact/ffill/ffill2/None) 모두 PASS.
- files: projects/stock-backtest/backend/app/domain/{calendar.py, __init__.py}
- 신규 public API: BASE_CCY_TO_CALENDAR, base_calendar_name, trading_days_in_period, align_market_price_to_base_calendar, align_universe_prices, next_trading_day, previous_trading_day

### TASK-031 (DONE) - 2026-04-29T10:20
- title: 자산 자유 추가 워크플로우 (도메인 서비스 + scheduler 큐잉)
- assignee: coder
- summary: backend/app/domain/asset/registration.py 도메인 서비스 (TickerValidator/BackfillEnqueuer Protocol DI - Reviewer N5) + backend/app/scheduler/backfill_queue.py (queue.Queue + threading.Thread MVP 직렬 1워커, runner 예외 격리). 6 케이스 (정상/검증실패/중복/inactive 재등록/min_history 부족/큐잉 실패) 전부 PASS. 한국어 에러 메시지 (UI/UX 원칙 2). domain.asset/__init__.py + scheduler/__init__.py append-only 갱신.
- files: projects/stock-backtest/backend/app/domain/asset/{registration.py, __init__.py}, projects/stock-backtest/backend/app/scheduler/{backfill_queue.py, __init__.py}
- 신규 public API: register_asset, RegistrationRequest, RegistrationResult, TickerValidationFailed, AlreadyRegistered, TickerValidator/BackfillEnqueuer Protocol, ValidationOutcome, BackfillQueue

### TASK-043 (DONE) - 2026-04-29T10:20
- title: Strategy 인터페이스 (3요소 조합) + engine.py 메인 루프 + 모델 A 구조적 강제
- assignee: coder
- summary: backend/app/domain/strategy.py (161줄, Allocator/SignalFilter Protocol + Strategy 3요소 + apply_filters_and_allocator AND 결합) + backend/app/domain/engine.py (263줄, run_backtest 메인 루프). 모델 A 차단 핵심 라인 engine.py L209 `prices_until_d = ctx.prices_aligned.loc[:d]` (D+1 절대 차단 — 구조적). 체결가는 별도 settlement_prices 메모리 분리. _is_rebalance_day 8 케이스 (첫날 + 6 schedule) PASS. mini end-to-end (1자산 5영업일) PASS. progress_callback / cancel_check hook 동작.
- files: projects/stock-backtest/backend/app/domain/{strategy.py, engine.py, __init__.py}
- 신규 public API: RebalanceSchedule, Allocator, SignalFilter, Strategy, apply_filters_and_allocator, BacktestRunContext, BacktestEquityPoint, BacktestRunResult, run_backtest

### TASK-044 (DONE) - 2026-04-29T10:20
- title: dividend.py 배당 처리 + metrics.py 메트릭 계산 (CAGR/MDD/Sharpe/Sortino/Calmar/승률/연·월)
- assignee: coder
- summary: backend/app/domain/dividend.py 76줄 (DividendPayment/DividendCredit + apply_dividend / apply_dividends_for_date - native currency 입금 + audit) + backend/app/domain/metrics.py 138줄 (compute_metrics 7 지표 1회 계산, _daily_returns/_max_drawdown/_cagr/_periodic_returns/_annualized 헬퍼 분리). 단위 검증: 배당 10주×$0.5→cash 100→105, CAGR=0.100 (선형), MDD=-0.182 (낙폭 시리즈), zero-division 방어, 2년치 연/월 그루핑 정상.
- files: projects/stock-backtest/backend/app/domain/{dividend.py, metrics.py, __init__.py}
- 신규 public API: DividendPayment, DividendCredit, apply_dividend, apply_dividends_for_date, MetricsResult, compute_metrics, TRADING_DAYS_PER_YEAR

### TASK-023 (DONE) - 2026-04-29T10:45
- title: APScheduler cron 잡 (KR 18:00 / US 07:00 / Crypto 09:00 KST)
- assignee: coder
- summary: backend/app/scheduler/cron_jobs.py 122줄. BackgroundScheduler + 3 CronTrigger (Asia/Seoul). on_kr/on_us/on_crypto DI 로 mock 가능. 시장별 독립 (별도 콜러블 + 별도 SessionLocal). _run_market_backfill 이 backfill_active_assets 위임. KST_TZ 상수. replace_existing=True 로 lifespan 재시작 안전. scheduler.start() 는 본 모듈 미호출 → TASK-061 lifespan 책임.
- files: projects/stock-backtest/backend/app/scheduler/{cron_jobs.py, __init__.py}
- 신규 public API: build_scheduler, KST_TZ

### TASK-045 (DONE) - 2026-04-29T10:45
- title: tax.py Tax plugin 인터페이스 + NoTaxPlugin 빈 구현
- assignee: coder
- summary: backend/app/domain/tax.py 106줄. RealizedTrade/DividendIncome/TaxResult frozen dataclass + TaxPlugin Protocol (@runtime_checkable) + NoTaxPlugin (MVP 디폴트 OFF, tax_amount=0) + apply_tax_to_portfolio 헬퍼. isinstance(NoTaxPlugin(), TaxPlugin) PASS. 도메인 순수.
- files: projects/stock-backtest/backend/app/domain/{tax.py, __init__.py}
- 신규 public API: RealizedTrade, DividendIncome, TaxResult, TaxPlugin Protocol, NoTaxPlugin, apply_tax_to_portfolio

### TASK-050 (DONE) - 2026-04-29T10:45
- title: Allocator base + FixedWeight 구현
- assignee: coder
- summary: backend/app/domain/allocators/{base.py 109줄 (AllocatorBase[P] Generic + abstract generate_weights + normalize_weights 헬퍼), fixed_weight.py 84줄 (FixedWeightParams pydantic 검증 + FixedWeight)}. params 검증 (empty/sum off/negative 모두 ValidationError). universe 교집합 정규화 (universe={1} 시 {1:1.0}). JSON Schema 출력 OK. Allocator Protocol 만족.
- files: projects/stock-backtest/backend/app/domain/allocators/{base.py, fixed_weight.py, __init__.py}
- 신규 public API: AllocatorBase, normalize_weights, FixedWeight, FixedWeightParams

### TASK-053 (DONE) - 2026-04-29T10:45
- title: SignalFilter base + MovingAverage 필터
- assignee: coder
- summary: backend/app/domain/filters/{base.py 56줄 (SignalFilterBase[P] Generic + abstract is_eligible), moving_average.py 60줄 (MovingAverageParams pydantic ge=2/le=2000, MovingAverage 가격>MA 면 PASS, price_above 토글)}. 5 케이스 (평탄/우상향/데이터부족/자산부재/우하향+price_above=False) 전부 PASS. SignalFilter Protocol 만족.
- files: projects/stock-backtest/backend/app/domain/filters/{base.py, moving_average.py, __init__.py}
- 신규 public API: SignalFilterBase, MovingAverage, MovingAverageParams

### TASK-051 / TASK-052 (DONE) - 2026-04-29T11:00
- title: AllWeather + EqualWeight Allocator (묶음)
- assignee: coder
- summary: AllWeather (Category 5종 Literal pydantic enum, DEFAULT_ALLWEATHER_WEIGHTS 30/40/15/7.5/7.5, 카테고리 내 1/N 분배, AllWeatherCategoryMissing 한국어 에러) + EqualWeight (params 없음, universe 1/N). __init__.py append-only. JSON Schema 양쪽 모두 정상.
- files: projects/stock-backtest/backend/app/domain/allocators/{all_weather.py, equal_weight.py, __init__.py}
- 신규 public API: AllWeather, AllWeatherParams, AllWeatherCategoryMissing, DEFAULT_ALLWEATHER_WEIGHTS, EqualWeight, EqualWeightParams

### TASK-054 (DONE) - 2026-04-29T11:00
- title: Momentum 필터 (lookback 수익률 > threshold)
- assignee: coder
- summary: backend/app/domain/filters/momentum.py 65줄. lookback 디폴트 126일 (~6개월), threshold 디폴트 0.0. 9 케이스 (uptrend/downtrend/threshold 0.5 strict/modest, 데이터 부족, 자산 미포함, start_price=0, NaN-leading, 음수 threshold) 모두 PASS. SignalFilter Protocol 만족.
- files: projects/stock-backtest/backend/app/domain/filters/{momentum.py, __init__.py}
- 신규 public API: Momentum, MomentumParams

### TASK-061 (DONE) - 2026-04-29T11:00
- title: 자산/전략 API + 스키마 모듈
- assignee: coder
- summary: schemas/{asset.py (AssetRead/AssetCreate/AssetSearchQuery/OhlcvPoint/AssetCreateResponse), strategy.py (StrategyDescriptor/StrategyListResponse)} + api/{assets.py (5 endpoint), strategies.py (1 endpoint)} + dependencies.py (get_db/get_*_repo) + main.py 라우터 추가. 5 엔드포인트 등록 (assets list/get/create/ohlcv + strategies list). HTTP 상태 매핑 (422/409/404/201). _RoutingValidator (KR=PykrxSource, US/CRYPTO=YfinanceSource) + _LoggingEnqueuer placeholder. JSON Schema 5 전략 (allocators 3 + filters 2) 노출.
- files: projects/stock-backtest/backend/app/{dependencies.py, schemas/{asset.py, strategy.py}, api/{assets.py, strategies.py, __init__.py}, main.py}
- 발견: BLOCKER-001 잔재로 DB select 시 column 부재 — endpoints/JSON Schema 까지가 SOFT 핵심. 사용자 DB 초기화 후 정상.

### TASK-062 (DONE) - 2026-04-29T11:20
- title: 백테스트 비동기 job API (POST/GET status/GET result/DELETE/GET list) + Repository + 백그라운드 runner
- assignee: coder
- summary: schemas/backtest.py (BacktestCreate/BacktestRun/BacktestResult/EquityPoint/TradeRecord/MetricsPayload/StrategyConfig) + data/repositories/backtest_repository.py (compute_run_hash universe sorted, BacktestRepository 모든 ORM 캡슐) + services/backtest_runner.py (execute_backtest_job + build_strategy_from_config 5 전략 라우팅 + 별도 SessionLocal progress/cancel 폴링, 데이터 로더는 placeholder MVP) + api/backtests.py (5 엔드포인트 + BackgroundTasks). DELETE 단일 동사로 cancel(pending/running) + delete(완료) 의미 분기. error_json (stage/type/message/request_ctx/trace_id) V2 살림. OpenAPI 7 components 신규.
- files: projects/stock-backtest/backend/app/{schemas/backtest.py, data/repositories/backtest_repository.py, services/{__init__.py, backtest_runner.py}, api/{backtests.py, __init__.py}, main.py}
- 신규 public API: BacktestRepository, compute_run_hash, execute_backtest_job, build_strategy_from_config + 5 엔드포인트
- 발견: 데이터 로더 (ohlcv → prices_aligned + fx_rates_to_base) placeholder — TASK-100 통합에서 보강 필요

### TASK-090 (DONE) - 2026-04-29T11:20
- title: Next.js 추가 설정 (Zod 스키마 + API 클라이언트 + shadcn/ui 7종 + 한국어 i18n)
- assignee: coder
- summary: lib/api/{schemas, client}.ts (Zod 백엔드 OpenAPI 동기, ApiError trace_id 보존) + lib/i18n/ko.ts (한국어 dict + t 헬퍼) + lib/utils.ts (cn) + components/ui/{button, input, card, label, select, badge, toast}.tsx (shadcn 표준 cva + tailwind) + app/{layout.tsx (ToastProvider), page.tsx (한국어 3-카드)}. tsc/build/dev 모두 PASS. 한국어 4 문자열 노출 확인.
- files: projects/stock-backtest/frontend/{lib/{utils.ts, api/{schemas.ts, client.ts}, i18n/ko.ts}, components/ui/*.tsx (7개), app/{layout.tsx, page.tsx}}
- 신규 public API: api.{health, listAssets, getAsset, createAsset, listStrategies}, ApiError, Zod schemas, ToastProvider/useToast, shadcn Button/Card/Input/Select/Badge/Label

### TASK-080 / TASK-082 (DONE) - 2026-04-29T11:55
- title: 백테스트 골든 스냅샷 9 케이스 + API 계약/비동기 통합 스모크
- assignee: tester
- summary: 17 통과 / 16 SOFT skip / 0 실패. TASK-080 12/12 PASS (3 시나리오 × 3 전략 + 3 invariant), 9 스냅샷 JSON 생성 (rel_tol=1e-4). TASK-082 5/5 비-DB PASS (health/strategies/openapi/fuzz×2), 16 DB-의존 SOFT skip (BLOCKER-001 잔재). schemathesis 3.39.16 핀 (pytest 9 충돌 회피 + force_schema_version="30"). 클린 아키텍처 위반 0.
- files: projects/stock-backtest/backend/{tests/conftest.py, tests/golden/{test_golden_scenarios.py, snapshots/}, tests/api/test_api_contract.py, requirements.txt}
- Tester severity=blocker (BLOCKER-001 잔재 영향 — 이미 등록, 사용자 액션 영역. 신규 코드 결함 아님)
- observation: 합성 시계열 vol≈0 으로 Sharpe 비현실적 (실데이터 무관), 워커 크래시 복구 미구현 (Phase 2 Celery 권장), 데이터 로더 placeholder (TASK-100 예정)

### TASK-091 (DONE) - 2026-04-29T11:55
- title: 자산 카탈로그 화면 (시장 필터 + 검색 + 자산 추가 다이얼로그)
- assignee: coder
- summary: app/assets/page.tsx + components/asset/{AssetTable, AddAssetDialog}.tsx. 시장 필터 + 한글명/심볼 검색 + 인라인 모달 (Radix 의존성 회피). UI/UX 원칙 1·2·3 적용 (JSON 0, 한국어 라벨, 로딩/검증/등록 진행 상태 toast). ApiError 422→notFound / 409→duplicate / else→generic 한국어 매핑 + 추적 ID. tsc/build/curl 모두 PASS, /assets 19.8 kB 정적.
- files: projects/stock-backtest/frontend/{app/assets/page.tsx, components/asset/{AssetTable.tsx, AddAssetDialog.tsx}}
- 발견: Zod .default({}) 가 input/output 타입 불일치 → Awaited<ReturnType> 패턴 우회. 후속 cleanup observation (schemas.ts .default→.optional)

### TASK-081 (DONE) - 2026-04-29T11:42
- title: look-ahead 회귀 + 비거래일 방어 4단계 + cash_by_ccy 환전 단위 회귀 테스트
- assignee: tester
- summary: 50/50 회귀 PASS, 0 결함. SpyAllocator/SpyFilter 로 매 호출 시 prices.index.max() ≤ signal_date 검증 — D+1 노출 0건 (engine.py L209 모델 A 구조적 차단 작동). 비거래일 4단계 방어 (수집 _is_invalid_close / 캘린더 _trading_days 2차 / 조회 guard_trading_day 3 모드 / 엔진 assert_* + slicing) 전부 동작. fx_spread 정확치 (1.3M KRW @ 1300 → 998 USD). Q3 C + Q5 B 단계 분리 + native 우선 정상. 전체 회귀 67 passed/16 skipped 영향 없음.
- files: projects/stock-backtest/backend/tests/regression/{__init__.py, test_lookahead.py, test_calendar_defense.py, test_cash_by_ccy.py}
- 환경: .venv/bin/python 필수 (anaconda3 글로벌 미사용)

### TASK-092 (DONE) - 2026-04-29T11:42
- title: 백테스트 생성 화면 (전략/파라미터/universe/기간/base_currency/리밸런싱)
- assignee: coder
- summary: app/backtests/new/page.tsx + components/backtest/{StrategyParamsForm, UniverseSelector}.tsx + lib/api/{schemas,client}.ts append (BacktestCreate/Run, api.createBacktest/getBacktest). 6 키워드 (새 백테스트/전략 선택/자산 선택/기축통화/리밸런싱 주기/백테스트 실행) HTML grep PASS. tsc/build/curl 모두 PASS. /backtests/new 4.04 kB.
- files: projects/stock-backtest/frontend/{app/backtests/new/page.tsx, components/backtest/{StrategyParamsForm,UniverseSelector}.tsx, lib/api/{schemas,client}.ts}
- observation: dict/array 파라미터 (FixedWeight weights) 임시 JSON-string 입력 — 후속 AssetWeightMap 위젯 권장 (UI/UX 원칙 1 잠재 위반). filter 선택 UI 미구현 (filter_configs:[] 고정).

### TASK-093 (DONE) - 2026-04-29T11:55
- title: 백테스트 결과 화면 (equity / drawdown / 지표 / 월별 히트맵 / 거래 테이블)
- assignee: coder
- summary: app/backtests/[run_id]/page.tsx + components/backtest/{EquityChart, DrawdownChart, MetricsTable, MonthlyHeatmap, TradesTable}.tsx + lib/api/{schemas,client}.ts append (BacktestResult/EquityPoint/TradeRecord/MetricsPayload, getBacktestResult). recharts 활용 (선형/로그 토글, drawdown area). 통화 그룹 필터 + 페이지네이션. ko.metric.* 한국어 라벨. 4 파일 5종 카드 모두 구현. tsc/build/curl 모두 PASS, /backtests/[run_id] 106 kB.
- files: projects/stock-backtest/frontend/{app/backtests/[run_id]/page.tsx, components/backtest/{EquityChart,DrawdownChart,MetricsTable,MonthlyHeatmap,TradesTable}.tsx, lib/api/{schemas,client}.ts}
- 발견: fetchAndValidate Zod input/output 타입 변이 → MetricsTable props loose 우회. 다음 client.ts 한 줄 fix 권장.

### TASK-094 (DONE) - 2026-04-29T11:55
- title: 진행률 폴링 + in-place 패널 + 한국어 에러 가이드 + 취소 버튼
- assignee: coder
- summary: lib/i18n/ko.ts append (progress 19키 + errorGuide 5키) + lib/api/client.ts append (cancelBacktest) + hooks/useBacktestPolling.ts (1s 폴링, terminal status 종료) + components/backtest/ProgressPanel.tsx (6 분기 pending/running/done/failed/cancelled/error) + app/backtests/new/page.tsx 수정 (submittedRunId state + JSX 분기). done 시 1.5s 후 자동 라우팅 → /backtests/[run_id]. 화면 3개 한도 유지 (별도 진행 화면 안 만듦, UI/UX 원칙 6).
- files: projects/stock-backtest/frontend/{lib/i18n/ko.ts, lib/api/client.ts, hooks/useBacktestPolling.ts, components/backtest/ProgressPanel.tsx, app/backtests/new/page.tsx}
- 신규 public API: useBacktestPolling, ProgressPanel, api.cancelBacktest

### TASK-100 (DONE) - 2026-04-29T12:10
- title: end-to-end 통합 (데이터 로더 보강 + README 7단계 + smoke_e2e + backtest_runner placeholder 해소)
- assignee: coder
- summary: services/data_loader.py 215줄 (load_universe_market_meta/load_prices_aligned/load_fx_rates_to_base/build_backtest_context — base 캘린더 정렬 + forward-fill + fx 환율 로드). backtest_runner.py 의 pd.DataFrame() placeholder 와 ("US", base_currency) 메타 placeholder 를 build_backtest_context 호출로 교체 + load_market_data stage 추적. scripts/smoke_e2e.py (사용자 BLOCKER-001 해소 후 수동 실행). README 90→163줄 7단계 빠른 시작 + 화면 3개 + 전략 5종 + Phase 분리. 회귀 + 골든 62 PASS 유지.
- files: projects/stock-backtest/{backend/app/services/{data_loader.py, backtest_runner.py}, backend/scripts/smoke_e2e.py, README.md}
- 핵심 발견: FxRate(base=USD, quote=KRW).rate=1300 이 정확히 base_per_ccy=KRW per USD 와 일치 (도메인 컨벤션 검증)

### TASK-212 (DONE) - 2026-04-30T09:30
- title: trade.time 백테스트 실행 시각 fallback 버그 수정 — TradeFill.settlement_date 추가
- assignee: coder
- summary: TradeFill dataclass 에 settlement_date 필드 추가 + _execute_sells/_execute_buys 시그니처에 rebalance_date 추가 + execute_rebalance 가 두 함수에 전달 + backtest_runner.py:242 fallback 제거. 5단계 명세대로. 단위 테스트 5건 신규, 회귀 0 (77 passed).
- files: backend/app/domain/trade.py, backend/app/services/backtest_runner.py, backend/tests/domain/{__init__.py, test_trade.py}
- 핵심 발견: 골든 스냅샷이 trade time 필드 비교 안 함 — TASK-215 baseline 갱신 사유에서 제외

### TASK-213 (DONE) - 2026-04-30T09:30
- title: 백필 정책 변경 — 자산의 가장 오래된 데이터부터 수집 (earliest_available)
- assignee: coder
- summary: DataSource Protocol 에 earliest_available(symbol) 추가 + yfinance(period='max') / pykrx(1995년부터) 구현 + pipeline._resolve_start 시그니처 확장 + backfill_asset 호출부 갱신. DEFAULT_MAX_LOOKBACK_DAYS 는 fallback. 단위 테스트 6건, 회귀 0 (68 passed).
- files: backend/app/data/sources/{base, yfinance_source, pykrx_source}.py, backend/app/data/pipeline.py, backend/tests/data/test_pipeline.py
- 후속: TASK-216 사용자 액션 (BTC asset_id=56 ohlcv 삭제+재백필)

### TASK-211 (DONE) - 2026-04-30T09:55
- title: 엔진 청산 누락 버그 수정 — engine.py:219 if target_weights: 분기 제거
- assignee: coder
- summary: 빈 dict 도 execute_rebalance 호출하도록 변경. trade.py:_classify_orders 가 보유 자산 전량 매도 처리. invariant("보유 자산 ⊆ universe") 박제 + KeyError silent 0 금지 정책. 단위 테스트 5건 + e2e replay (run_id=96 BTC + MA(117) + quarterly 시나리오). 89 passed.
- files: backend/app/domain/engine.py, backend/app/domain/trade.py, backend/tests/domain/test_engine.py, backend/tests/e2e/test_failure_replay.py
- 후속 권장: engine.py L275 broad except 좁히기 (NonTradingDayError/MissingPriceError/InsufficientFundsError 만)

### TASK-214 (DONE) - 2026-04-30T09:55
- title: 분할/증자/감자 처리 — 임시처방 (yfinance auto_adjust=True + pykrx 한계 명시)
- assignee: coder
- summary: yfinance_source.py:83 auto_adjust=True 전환 (close=Adj Close 자동) + Adj Close 컬럼 누락 시 close fallback. pykrx 코멘트 갱신 (Phase 2 정공법 BLOCKER-003). architecture.md "분할/증자/감자 (V3 MVP 임시처방)" 섹션 추가. blockers.md BLOCKER-003 [SOFT] 등록. 회귀 29 passed.
- files: backend/app/data/sources/{yfinance_source, pykrx_source}.py, signal/stock-backtest/architecture.md, signal/stock-backtest/blockers.md
- 핵심 발견: 캐시된 yfinance ohlcv 는 auto_adjust=False 시점 데이터 — TASK-216 사용자 통지에 BTC 외 yfinance 자산 재백필 권고 추가 검토

### TASK-218 (DONE) - 2026-04-30T11:30
- by: coder (frontend in-place 결과 패널)
- 변경: page.tsx (539→615 lines, 좌+우 sticky 2-column), ProgressPanel.tsx (router.push 두 곳 + useRouter import + AUTO_REDIRECT_MS 모두 제거), useFormPersistence hook 신규 (138 lines, __version: 1 + migrate 콜백), useFormPersistence.test.ts 신규 (6/6 PASS), vitest.config.ts 신규, ko.ts (progress.doneInPlace 키), package.json devDep (jsdom, @testing-library/*).
- DoD: (a) URL 변경 0 ✅, (b) 새로고침 폼 복원 ✅ (단위 6/6), (c) 파라미터 일부 변경 후 재실행 폼 유지 ✅, (d) /backtests/[run_id] 회귀 0 (파일 미수정).
- 검증: npm run build 6/6 페이지, vitest 6/6 (532ms), typecheck/lint OK.
- 후속: 메인(/) 이력 카드 진입 경로 별도 확인 권장 (TASK-218 범위 밖).
- files: signal/stock-backtest/coder-report-TASK-218.md

### TASK-219 (DONE) - 2026-04-30T11:30
- by: coder (ma_signal allocator)
- 변경: allocators/ma_signal.py 신규 (자산 단위 fallback + normalize_weights allow_cash_slot=True), allocators/__init__.py re-export, services/backtest_runner.py:53-58 _ALLOCATORS 등록, api/strategies.py:60-67 list_strategies 에 추가, tests/domain/test_ma_signal_allocator.py 신규 (8/8 PASS), architecture.md:670 allocators 행 4종 갱신.
- DoD: (a) 단위 8/8 ✅, (b) e2e BTC100% w120 quarterly **수동 검증 위임** (Manager가 사용자 시나리오로 확인), (c) 9 골든 회귀 0 (12/12) ✅, (d) GET /api/strategies 에 ma_signal 등장 ✅.
- frontend 변경 0: JSON Schema 자동 폼 + complexFieldRenderer 가 ma_signal `assets: dict` 를 AssetWeightMap 으로 자동 주입.
- 후속 발견 (TASK-221 신규 등록): tests/api/test_api_contract.py::test_strategies_endpoint_returns_mvp_presets 의 `assert len(allocators) == 3` 하드코딩 회귀 — Tester 가 4 + 'ma_signal' 포함 단언으로 갱신 필요.
- files: signal/stock-backtest/coder-report-TASK-219.md

### TASK-222 (DONE) - 2026-04-30T11:50
- by: tester (severity: environment)
- 변경: tests/e2e/test_persona_first_use.py 갱신 (함수명 _allocator3 → _allocator4, set 단언에 ma_signal 추가, "ma_signal" in allocator_names 명시 단언 추가).
- 결과: 6 collected, 5 passed, 1 failed. step3 fail = environment (살아있는 quant-lab-backend.service stale 코드).
- BLOCKER-004 등록 (사용자 액션: systemctl --user restart quant-lab-backend.service).
- files: signal/stock-backtest/tester-report-TASK-222.md

### TASK-220 (Tester 검증) - 2026-04-30T11:50
- by: tester (severity 부여 없음, 코드 결함 0)
- 결과: 단위 22/22 (test_engine.py 9 포함), 골든 12/12, frontend build/typecheck PASS, Literal 7값 3-way 동기 정확, semi_annual 4 transition (12→1월 True / 6→7월 True / 4→5월 False / 동일 H 재호출 False) 모두 expected.
- 클린 아키텍처: quarterly ↔ semi_annual `(month-1)//N` 거울 패턴 (N=3↔6).
- observation: signal_event UI 미노출 (pre-existing), Literal 수동 동기 부담 (V3 범위 외).
- files: signal/stock-backtest/tester-report-TASK-220.md

### TASK-220 (DONE) - 2026-04-30T11:50
- by: coder (semi_annual = 1월·7월 첫 거래일, 사용자 결정)
- 변경: strategy.py Literal 7값, schemas/backtest.py 동기, engine.py `_is_rebalance_day` semi_annual 분기 `(d.month-1)//6` 패턴, frontend Zod enum 7값, page.tsx REBALANCE_OPTIONS 에 "반기" 한 줄, tests/domain/test_engine.py 에 TestIsRebalanceDaySemiAnnual 4 케이스.
- DoD: (a) 단위 22/22 (4 신규 + 18 기존) ✅, (b) npm run build + Zod enum 7값 ✅, (c) 단위로 1월·7월 trigger / 다른 월 false 검증 ✅.
- 주의: Coder 가 tests/ 수정함 — task description 에 명시 (단위 4 케이스 추가) 라 합리적이나, coder.md L188 (tests/ 수정 금지) 와 모호한 지점. 회고 후보.
- files: signal/stock-backtest/coder-report-TASK-220.md

### TASK-218 (Tester 검증) - 2026-04-30T11:50
- by: tester (severity: observation, 코드 결함 0)
- 결과: 7/7 검증 PASS (단위 6/6, build, typecheck, lint, router.push 제거, localStorage 키 충돌 0, [run_id] 회귀 0).
- 클린 아키텍처: useFormPersistence hook 정상 분리, ProgressPanel unused import 제거됨, BacktestResultPanel inline (70 lines, 합리적).
- observation 2건: (1) Coder line count 615 vs 실측 794 (+179 차이, 회고), (2) BacktestResultPanel inline (Coder 명시 결정).
- files: signal/stock-backtest/tester-report-TASK-218.md

### TASK-219 (Tester 검증) + TASK-221 (DONE) - 2026-04-30T11:50
- by: tester (severity: observation)
- TASK-219 검증: 단위 8/8 PASS, 9 골든 12/12 PASS, 자산 단위 fallback (BTC 130일/ETH 50일/window=120) 검증, 클린 아키텍처 무결 (FixedWeight 패턴 100% 일치).
- TASK-221 처리: tests/api/test_api_contract.py:78-94 갱신 (`len==3 → ==4` + `"ma_signal" in names`). 3 passed.
- 발견 후속:
  - TASK-222 신규 (persona harness 동일 하드코딩 갱신 — tests/e2e/test_persona_first_use.py:92-110)
  - MaSignalParams/FixedWeightParams 검증 중복 — 5번째 allocator 시점에 utils 추출
  - golden test_golden_scenarios.py:377 baseline 매트릭스는 의도적 락
- 환경 노트: anaconda host 에 backend 의존성 (schemathesis/pydantic-settings/fastapi/SQLAlchemy/psycopg2-binary/exchange_calendars/APScheduler/yfinance/pykrx) 설치됨 (테스트 collection 활성화 목적). docker compose 에 backend 서비스 부재로 host 실행이 정책.
- files: signal/stock-backtest/tester-report-TASK-219.md

### TASK-216 (DONE) - 2026-04-30T10:30
- by: manager (Manager 가 사용자 위임 받아 venv python 으로 직접 실행)
- 결과:
  - DELETE asset_id=56 ohlcv: 1825 rows 제거
  - backfill_asset(YfinanceSource): rows_inserted=4242, status=PARTIAL, requested_start=2014-09-17
  - 검증 SELECT MIN/MAX/COUNT: MIN=2014-09-17 09:00 KST, MAX=2026-04-28 09:00 KST, COUNT=4242
- DoD 충족: MIN < 2017-01-01 ✅, COUNT > 3000 ✅
- 핵심 검증: requested_start 가 2014-09-17 로 잡힘 → TASK-213 `earliest_available()` 정책 정상 작동 증거
- 후속:
  - TASK-217 (자산 추가 시 자동 백필) — `_LoggingEnqueuer` placeholder 교체
  - 사용자가 원래 시나리오 (BTC 100% + MA(120) + 분기 + 2017~) 재실행해서 e2e 검증 필요

### TASK-215 (DONE) - 2026-04-30T10:10
- title: 골든 baseline 9 케이스 통합 재생성 (Tester)
- assignee: tester
- severity: observation
- summary: **재생성 불필요** 결정. fixture 가 backend/tests/golden/test_golden_scenarios.py:69-100 _make_trending_series 의 순수 수학 합성 (math.sin 결정적 noise) — yfinance/DB/random 호출 0 → TASK-214 가격 보정 영향 0. TASK-211 청산 path 미진입 (signal_filters=tuple()). TASK-212 time 필드 비교 안 함. 9 케이스 모두 통과 (12 passed; 확장 회귀 72 passed).
- files: signal/stock-backtest/tester-report-TASK-215.md
- 핵심 발견: scenario_3 (BTC) 3 파일이 작업트리에 이미 수정됨 — TASK-205 (V3 Q8 fractional crypto) 의 의도된 회귀 (severity: observation)












### TASK-244 (DONE) - 2026-05-07T00:30
- title: 엔진 EOD equity 기록 시점 결함 수정 — 큐잉 패턴으로 D+1 settlement 분리 (Coder)
- assignee: coder
- summary: `engine.py` 메인 루프를 `pending_rebalance` 큐잉 패턴으로 재구성 — D iteration 안에서 시그널/체결/EOD 평가를 모두 처리하던 회계 결함을 ① settlement (어제 시그널을 오늘 가격으로) → ② EOD equity 기록 → ③ signal 큐잉 3단계로 분리. helper 3개 추출 (`_settle_pending_rebalance`, `_record_eod_equity`, `_generate_signal_for_day`) + `_PendingRebalance` dataclass. `next_trading_day` import + 호출 1곳 제거. validation harness L1~L3 expected 식 갱신 (case_l1.py C1~C5 expected_initial_equity = pure cash, case_l2.py C6 docstring hand-trace 전면 재작성, C8 docstring 갱신). case_l3.py / _helpers.py 변경 없음 (path-independent invariants / `closed_form_initial_buy` spec 보존).
- files:
  - projects/stock-backtest/backend/app/domain/engine.py (수정, 277줄 변동)
  - projects/stock-backtest/backend/scripts/validation/case_l1.py (수정, 65줄 변동)
  - projects/stock-backtest/backend/scripts/validation/case_l2.py (수정, 116줄 변동)
  - signal/stock-backtest/coder-report-TASK-244.md (신규)
  - signal/stock-backtest/reviewer-report-TASK-244.md (신규, r2 PASS)
- smoke: `python -m scripts.validation.run_all --skip-opus` → **9/9 PASS** (L1 5/5 + L2 3/3 + L3 1/1). L4 정성 평가 + 11/11 공식 재달성은 TASK-244B (Tester) 분담.
- DoD: (a)~(e) 모두 PASS. tests/ 디렉토리 미수정 (Tester 분담 정책 준수).
- 분담: TASK-244B (Tester) — `tests/domain/test_engine.py` 신규 클래스 4 메소드 + 골든 baseline 9 재생성 + regression 3 파일 0 회귀 + run_all 11/11 공식 재달성.
- commit: 미수행 (Manager 가 TASK-244 + TASK-244B 통합 commit 결정 시 처리).

### TASK-244B (DONE) - 2026-05-07T01:00
- title: TASK-244 검증 — 단위 테스트 + 골든 baseline + 회귀 (Tester 분담)
- assignee: tester
- severity: bug (Issue 1 — case_l4.py fixture stale, 후속 TASK-244C)
- summary: TASK-244 (engine.py 큐잉 패턴) 검증. DoD (a) `TestEodEquityAccountingTiming` 4 신규 메소드 PASS, DoD (b) regression 50/50 PASS, DoD (c) 골든 9 baseline 재생성 + 임계값 검증 (부호 9/9 + final_equity 9/9 + cagr/win_rate 18/18 PASS, sharpe 6 + mdd 8 ESCALATE — baseline regime change), DoD (d) `run_all.py` 10/11 (L1 5/5 + L2 3/3 + L3 1/1 + L4 1/2). L4 S1 SUSPECT 는 코드 결함이 아닌 **`scripts/validation/case_l4.py` L48-62 fixture 가 TASK-244 fix 이전 엔진 출력으로 박제** — Opus 가 정확히 catch. Tester 영역 (`tests/`) 외라 본 태스크 미수정.
- files:
  - projects/stock-backtest/backend/tests/domain/test_engine.py (수정, `TestEodEquityAccountingTiming` 신규 클래스 + 헬퍼 3종)
  - projects/stock-backtest/backend/tests/golden/snapshots/*.json (9 파일 baseline 재생성)
  - signal/stock-backtest/tester-report-TASK-244B.md (신규)
  - signal/stock-backtest/reviewer-report-TASK-244B.md (r2 PASS)
- 후속:
  - TASK-244C (Coder): case_l4.py L48-62 fixture 갱신 → 11/11 PASS 재달성 (severity=bug 자동 등록).
  - ESCALATE: 골든 baseline 6 sharpe + 6 mdd 케이스 임계값 (50%) 초과 — TASK-244 fix 의 의도된 효과 (옛 sharpe 1000+ variance≈0 인플레이션 / mdd 0 = Day 0 post-trade BUG 부산물). 사용자 confirm 필요.

### TASK-300 (DONE) - 2026-05-12
- title: alembic 0005 — themes / theme_assets / asset_theme_history + asset_market_cap 테이블 + AssetType Literal 'STOCK' 추가 (Phase 2.1 첫 태스크)
- assignee: coder
- summary: 4 테이블 신규 (themes/theme_assets/asset_theme_history/asset_market_cap) + SQLAlchemy 모델 2 파일 (theme.py, market_cap.py) + AssetType Literal 4곳 동기 (entity.py / schemas/asset.py / seed/assets_catalog.py / schemas.ts). alembic 0005 head=0005_theme_tables 직선, history 0001~0005 정상. DB ENUM 미사용이므로 alembic 본문은 DDL 만 (Literal 변경은 Python/TS 정적). Reviewer r2 PASS 직후 Coder 호출.
- files: backend/alembic/versions/0005_theme_tables.py (신규), backend/app/models/{theme.py, market_cap.py, __init__.py}, backend/app/domain/asset/entity.py, backend/app/schemas/asset.py, backend/app/data/seed/assets_catalog.py, frontend/lib/api/schemas.ts
- DoD: (a) alembic upgrade head 성공, (b) history 직선 + heads=0005, (c) STOCK Literal 4 위치 모두 등장, (d) test_api_contract 회귀 0 (5F/12P/4S — 신규 FAIL 0), (e) npm run build PASS
- 후속: TASK-301 (도메인 entity + Repository Protocol + service) 진행

### TASK-301 (DONE) - 2026-05-12
- title: Theme 도메인 entity + Repository Protocol + service (history 자동 append 트랜잭션 박제)
- assignee: coder
- summary: `backend/app/domain/themes/` 4 파일 (entity / repository / service / __init__) 신규. ThemeRepository Protocol 10 메서드 (요구 9 + append_history — 트랜잭션 박제 위해 필수, 근거 report 명시). UnitOfWork Protocol 채택 (commit/rollback). service 단위 테스트 5/5 + frozen smoke 1 PASS, 기존 tests/domain/ 44 PASS 회귀 0.
- files: backend/app/domain/themes/{__init__.py, entity.py, repository.py, service.py}, backend/tests/domain/themes/test_theme_service.py
- DoD: (a) 도메인 순수성 grep banned imports 0 hit, (b) Protocol 10 메서드 + 3 frozen dataclass, (c) service 단위 테스트 5/5 PASS, (d) tests/domain/ 44 회귀 0, (e) import smoke PASS
- 핵심 결정: Repository 가 트랜잭션 인지하지 않고 UnitOfWork(Protocol commit/rollback) 가 service 에 주입 — TASK-302 SqlThemeRepository 가 SQLAlchemy Session 어댑터로 UoW 구현
- 후속: TASK-302 (SqlThemeRepository) + TASK-304 (normalization) + TASK-309 (격리 정적 검증) 병렬 진행

### TASK-302 / TASK-304 / TASK-309 (병렬 DONE) - 2026-05-12

3 태스크 동시 호출 (Reviewer r2 PASS 후 의존성 그래프 2차 병렬 단계). 파일 충돌 0.

- **TASK-302** (coder, SqlThemeRepository): `backend/app/data/theme_repository.py` 신규 — SqlThemeRepository + SqlAlchemyUnitOfWork (선택 A 단일 파일, thin wrapper). 통합 테스트 6 PASS (5 핵심 + 1 UoW 보조). isinstance(repo, ThemeRepository) PASS. 회귀 baseline 동일 유지. `soft_delete_theme` 는 alembic 0005 의 themes.deleted_at 부재로 활성 멤버 일괄 종료만 보장 (themes row 보존). `WHERE removed_at IS NULL` 명시로 부분 인덱스 트리거. observation: NOW() 트랜잭션 고정 특성으로 "재추가" 시나리오 1건 제거.
- **TASK-304** (coder, normalization): `backend/app/domain/themes/normalization.py` 신규 — 4 함수 (rebase_series / rebase_multi_series / aggregate_equal_weighted / compute_theme_aggregate). 8 단위 테스트 PASS. 첫 유효값=0 시 ValueError, 내부 연산은 float64 (base_value 만 Decimal). market_cap weighting 본체 구현 (Phase 2.2 활성화 예정).
- **TASK-309** (tester, 격리 정적 검증): `backend/tests/architecture/test_no_cross_import.py` + `__init__.py` 신규. 3 invariant PASS (themes→backtest 0 hit / backtest→themes 0 hit / services→themes/theme_repository 0 hit). 출력 형식 검증을 위해 임시 위반 1줄 삽입→원복. **발견 (환경)**: Manager 가 Coder 호출 시 명시한 venv 경로 `projects/stock-backtest/backend/.venv/bin/python` 가 실제로는 `projects/stock-backtest/.venv/bin/python` 위치 — 향후 Coder/Tester prompt 정정 필요.
- 회귀 영향: 없음 (3 태스크 합산).

### TASK-303 (DONE) - 2026-05-12
- title: Theme API 라우터 (CRUD + asset 추가/제거) — 8 엔드포인트
- assignee: coder
- summary: 신규 3 파일 (`schemas/theme.py` + `api/themes.py` + `tests/api/test_themes.py`) + 갱신 4 파일 (`api/assets.py` theme_history endpoint / `dependencies.py` get_theme_repo + get_theme_uow / `api/__init__.py` + `main.py` include_router). 8 endpoint OpenAPI 등록, 5 단위 테스트 PASS, 기존 API 회귀 0, frontend build PASS, 도메인→API import 0 hit. schemathesis fuzz 대응 위해 endpoint 별 4xx (404/409) 응답을 OpenAPI 에 명시 추가.
- files: backend/app/{schemas/theme.py, api/themes.py, api/assets.py (theme_history append), api/__init__.py, dependencies.py, main.py}, backend/tests/api/test_themes.py
- DoD: (a) 8 endpoint OpenAPI 등장, (b) 5 테스트 PASS, (c) 기존 API 회귀 0, (d) npm build PASS, (e) 도메인 격리 0 hit
- 후속: TASK-305 (정규화 차트 API — 같은 api/themes.py 에 endpoint 2건 추가, 순차 진행)

### TASK-305 (DONE) - 2026-05-12
- title: 정규화 차트 API (GET /api/themes/{id}/chart + GET /api/themes/compare) — Phase 2.1 backend 마무리
- assignee: coder
- summary: `api/themes.py` 에 endpoint 2건 추가 + `schemas/theme.py` 에 스키마 5종 신설 (SeriesPoint/UniverseMeta/ThemeChartResponse/ThemeCompareItem/ThemeCompareResponse). 4 통합 테스트 PASS, OpenAPI 등록 확인, frontend build PASS, 회귀 0. `weighting=market_cap` → 422 + 한국어 graceful (Phase 2.2 활성화 예정).
- files: backend/app/{api/themes.py (endpoint 2 추가), schemas/theme.py (스키마 5 추가)}, backend/tests/api/test_themes_chart.py
- DoD: (a) 2 endpoint OpenAPI 등장, (b) 4 테스트 PASS, (c) market_cap 422, (d) 회귀 0, (e) npm build PASS
- 핵심 발견: FastAPI 라우팅 순서로 `/compare` 가 `/{theme_id}` 보다 **먼저 등록되어야** path 매칭 정확 — 코드 순서 조정 반영.
- 후속: backend Phase 2.1 endpoint 10건 (CRUD 8 + 차트 2) 완성. 다음 TASK-306 (frontend Zod + client) → TASK-307 + 308 (병렬 화면)

### TASK-306 (DONE) - 2026-05-12
- title: Frontend Zod 스키마 + API 클라이언트 (Theme CRUD + STOCK enum 동기)
- assignee: coder
- summary: 4 파일 갱신 — `lib/api/schemas.ts` (Theme 13 Zod + paginatedResponseSchema 제네릭), `lib/api/client.ts` (api.* 10 메서드 + deleteNoContent 헬퍼), `lib/api/types.ts` (z.infer 12 타입), `lib/api/__tests__/schemas.test.ts` 신규 (8 tests PASS). tsc/build/vitest 모두 PASS. STOCK enum L45 등장 확인.
- files: frontend/lib/api/{schemas.ts, client.ts, types.ts, __tests__/schemas.test.ts}
- DoD: (a) tsc 통과, (b) npm build PASS, (c) vitest schemas 3 (실제 8) PASS, (d) STOCK 1 hit, (e) 10 신규 메서드 노출
- 핵심 결정: Decimal → number coerce (`z.coerce.number()`), `dict[int]` → `record(string)` 직렬화 차이 흡수 — 백엔드 JSON ↔ 프런트 Zod 경계
- 후속: TASK-307 + TASK-308 (병렬 화면)

### TASK-307 / TASK-308 (병렬 DONE) - 2026-05-12

2 태스크 동시 호출 (Reviewer r2 PASS 후 6차 병렬 단계). ko.ts 책임 분리 정책으로 충돌 0.

- **TASK-307** (coder, 화면 4): `app/themes/page.tsx` + `components/themes/{ThemeList, ThemeEditor, AssetPicker}.tsx` 신규 (7 파일 = 4 + 단위 테스트 3). `lib/i18n/ko.ts` `theme.*` namespace 신설 (`theme.list/editor/delete/assets/detail.*` = 13 키, TASK-308 `theme.detail.*` 도 선반영 — 충돌 방지 정책 준수). AssetPicker 는 UniverseSelector 와 API 표면 차이로 신규 작성. 9 vitest PASS. 권고: `affected_assets`·`active_members` 의 Zod `.default([])` → `.optional()` 전환.
- **TASK-308** (coder, 화면 5): `app/themes/[theme_id]/page.tsx` + `components/themes/charts/{NormalizedPriceChart, ThemeAggregateChart, ThemeCompareChart}.tsx` + `hooks/useThemeChartData.ts` 신규. tsc + npm build PASS. 10 vitest PASS (DoD 3건 초과). **ko.ts 수정 0 라인** (Reviewer r2 권고 정책 준수). Zod variance 는 `Awaited<ReturnType>` alias 로 우회. recharts jsdom 호환은 ResizeObserver polyfill + ResponsiveContainer stub.
- 병렬 충돌: 0. TASK-307 의 ko.ts 신설 키가 TASK-308 의 `t('theme.detail.*')` 호출과 정합 (TASK-307 가 detail 키 선반영).
- 회귀: TASK-307 단독 build 시점에는 TASK-308 미완성으로 Zod variance 차단 — 두 태스크 합쳐 최종 build PASS.

### TASK-310 (DONE) - 2026-05-12
- title: Phase 2.1 e2e 스모크 + 5 회귀 검증
- assignee: tester
- severity: observation (코드 결함 0)
- summary: e2e `test_theme_flow.py` 7 단계 PASS (테마생성→자산추가x2→차트(rebase=100)→자산제거→history(ADDED+REMOVED)→비교→삭제). 회귀 4/5 PASS — golden 12/12, validation 9/9, regression 50/50, npm build PASS (신규 `/themes` + `/themes/[theme_id]` 라우트 확인). api_contract 신규 1 FAIL (`GET /themes/{theme_id}/chart` id=0 fuzz) 은 기존 fuzz raise-HTTPException 패턴 확장 — 격리 실행 시 PASS, Phase 2.1 회귀 아님 (observation).
- files: backend/tests/e2e/test_theme_flow.py (신규)
- 후속: TASK-312 (fuzz 404 패턴 일관화) 등록 — observation 분리 처리, retrospective 진입 전 사용자 결정

### TASK-311 (DONE) - 2026-05-12
- title: 백테스트 universe + STOCK 자산 선택 시 생존편향 경고 토스트 (C5 후속)
- assignee: coder
- summary: `UniverseSelector` add() 시점에 useRef 기반 warned-once flag 로 STOCK 자산 포함 시 한국어 경고 토스트 1회 노출. ko.ts `warning.survivorshipBias` 키 추가. 단위 테스트 2건 PASS (STOCK→1회 / ETF·INDEX→0건), npm build PASS.
- files: frontend/components/backtest/UniverseSelector.tsx, frontend/lib/i18n/ko.ts, frontend/components/backtest/__tests__/UniverseSelector.test.tsx
- DoD: (a)~(e) 모두 PASS
- 후속: Phase 2.1 마무리 — Phase 2.2 (시가총액 수집) / Phase 2.3 (관심도) 진입 결정 사용자 영역

### TASK-244C (DONE) - 2026-05-07T01:30
- title: case_l4.py fixture 갱신 — TASK-244 큐잉 패턴 정합 (Coder 후속, Tester 발견 bug)
- assignee: coder
- summary: TASK-244B 가 발견한 severity=bug (case_l4.py L48-62 fixture stale) 후속 수정. L50 initial_equity (Day 0) literal: $9,747.06 → $10,000.00 (pure cash, 큐잉 패턴 명시). L51 신규: Day 1 equity $9,989.56 (settlement 직후). L52+ (peak/trough/final/MDD/CAGR/Calmar/invariants) 변경 없음. `run_all.py` 출력 = **11/11 PASS** (L1 5/5 + L2 3/3 + L3 1/1 + L4 **2/2**). L4 S1 Opus verdict: SUSPECT → **PLAUSIBLE** 전환 — Opus 가 큐잉 패턴 정합성 인지.
- files:
  - projects/stock-backtest/backend/scripts/validation/case_l4.py (수정, L50-L51)
  - signal/stock-backtest/coder-report-TASK-244C.md (신규)
- DoD: (a) (b) 모두 PASS.
- commit: 미수행 (Manager 가 TASK-244 + TASK-244B + TASK-244C 통합 commit 결정 시 처리).
