# Done Log

### TASK-001 (DONE) - 2026-04-14T10:30
- title: 프로젝트 초기화
- assignee: coder
- summary: stock-backtest 프로젝트 골격 구축. requirements.txt, requirements-dev.txt, .env.example, .gitignore, README.md, pyproject.toml 생성. src/stock_backtest/ 하위 9개 서브패키지(data, ingestion, analysis, strategies/{static,dynamic}, backtest, metrics, web)와 tests, config, migrations 디렉토리 골격 마련. 의존성 설치는 사용자 venv에서 수행 예정.
- files: projects/stock-backtest/requirements.txt, requirements-dev.txt, .env.example, .gitignore, README.md, pyproject.toml, src/stock_backtest/__init__.py (+ 9개 서브패키지), tests/__init__.py, config/.gitkeep, migrations/.gitkeep

### TASK-002 (DONE) - 2026-04-14T10:50
- title: docker-compose.yml (Postgres 16 + TimescaleDB) + 기동 검증
- assignee: coder
- summary: timescale/timescaledb:latest-pg16 기반 docker-compose.yml 작성. named volume, healthcheck 포함. initdb SQL로 메인 DB + stock_backtest_test 양쪽에 timescaledb 확장(2.26.2) 자동 설치. 로컬 기동 검증 통과. README에 Docker 섹션 추가.
- files: projects/stock-backtest/docker-compose.yml, projects/stock-backtest/docker/initdb/001_extensions.sql, projects/stock-backtest/README.md

### TASK-003 (DONE) - 2026-04-14T11:30
- title: DB 스키마 초기 마이그레이션
- assignee: coder
- summary: Alembic 초기화 + 10개 테이블 + 2개 hypertable(ohlcv, backtest_equity, chunk 1년). 메인/테스트 DB 양쪽에 upgrade 성공, downgrade 왕복 검증, insert 스모크 통과. FK 7개, CHECK 6개 모두 확인. psql 실제 출력을 report에 포함. sqlalchemy 2.0.49 업그레이드됨.
- files: projects/stock-backtest/alembic.ini, migrations/env.py, migrations/script.mako, migrations/versions/0001_initial_schema.py, .env (로컬 실행용, gitignore됨)

### TASK-004 (DONE) - 2026-04-14T11:55
- title: ORM + DB 세션 + Repository 골격
- assignee: coder
- summary: SQLAlchemy 2.0 DeclarativeBase 기반 10개 ORM 모델 (migration 0001과 완전 일치). db.py에 .env 로드, engine pool, @contextmanager get_session, 테스트 DB 분기 구현. repository.py에 Asset/Ohlcv/FxRate/IngestionLog 레포지토리. bulk UPSERT는 pg_insert.on_conflict_do_update, FX는 7일 fallback. 스모크 5항목 모두 통과, DB 원상복구.
- files: projects/stock-backtest/src/stock_backtest/data/db.py, models.py, repository.py

### TASK-005 (DONE) - 2026-04-14T12:15
- title: defaults.yaml + 설정 로더
- assignee: coder
- summary: Pydantic v2 Settings 스키마 + YAML 로더 구현. 거래비용(KR 28bp 매도 포함), 리밸런싱, 캘린더, 크립토 기준시각 UTC 00:00, kr_resident 세금 프로파일, 수집 rate limit/재시도 모두 반영. market별 오버라이드 머지 함수 `get_costs`, 세금 프로파일 조회 `get_tax_profile`. extra='forbid'로 오타 방지, 음수 bps/잘못된 frequency/profile 누락 모두 ValidationError. 스모크 8/8 통과.
- files: projects/stock-backtest/config/defaults.yaml, projects/stock-backtest/src/stock_backtest/config.py

### TASK-006 (DONE) - 2026-04-14T12:45
- title: DataSource 추상 인터페이스
- assignee: coder
- summary: abc.ABC 기반 `DataSource` 추상 클래스 정의. `fetch_ohlcv`/`fetch_fx`/`list_symbols` + `source_name` property. 반환 DataFrame 컬럼 스키마(OHLCV: time/open/high/low/close/adj_close/volume, FX: time/rate, 1 base_ccy = rate quote_ccy) docstring에 명시. 공통 예외 `DataSourceError`, `SymbolNotFoundError`, `RateLimitError` 포함. import 검증 통과.
- files: projects/stock-backtest/src/stock_backtest/ingestion/base.py

### TASK-015 (DONE) - 2026-04-14T12:45
- title: Strategy 추상 베이스 + pydantic params_schema + 자동 스캔 registry
- assignee: coder
- summary: `StrategyParams(BaseModel)` + `Strategy(ABC)` (name/params_schema/description 클래스 속성, generate_weights·required_universe abstract). registry.py에 `@register` 데코레이터, 전역 STRATEGY_REGISTRY, pkgutil.walk_packages 기반 `discover_strategies`, get/list 헬퍼. 중복 이름 ValueError, 동일 클래스 재등록은 멱등. 빈 레지스트리/discover/KeyError/ValueError 모두 검증.
- files: projects/stock-backtest/src/stock_backtest/strategies/base.py, registry.py, __init__.py, static/__init__.py, dynamic/__init__.py

### TASK-024 (DONE) - 2026-04-14T12:45
- title: 기본 계절성 분석 (월/요일/월말/Sell-in-May/Halloween)
- assignee: coder
- summary: seasonality.py에 `daily_returns`, `monthly_effect`, `day_of_week_effect`, `month_edge_effect`, `sell_in_may`, `halloween_indicator` 6개 함수 구현. pandas/numpy 전용. DatetimeIndex 검증(아니면 ValueError), NaN dropna, 입·출력 스키마 docstring 완비. `halloween_indicator`는 Bouman & Jacobsen season_end_year 컨벤션(Nov-Dec → 다음 연도로 롤) 적용. 6년 합성 영업일 시리즈로 smoke test 통과.
- files: projects/stock-backtest/src/stock_backtest/analysis/seasonality.py, __init__.py

### TASK-007 (DONE) - 2026-04-14T13:05
- title: yfinance 기반 DataSource 구현
- assignee: coder
- summary: `YFinanceSource(DataSource)` 구현. market ∈ {US, CRYPTO, COMMODITY, FX} 지원, yfinance MultiIndex 컬럼 플래트닝·lowercase 정규화, end+1일 보정(yfinance end exclusive), threading.Lock 기반 rate limit(config 또는 0.7s 폴백), 빈 응답→SymbolNotFoundError, 429/throttle 키워드→RateLimitError. 재시도는 파이프라인 위임. 런타임 import 검증은 로컬 환경 numpy/pandas ABI 문제로 실패했으나 ast.parse 통과, TASK-009에서 numpy<2로 해결됨.
- files: projects/stock-backtest/src/stock_backtest/ingestion/yfinance_source.py

### TASK-008 (DONE) - 2026-04-14T13:05
- title: pykrx 기반 DataSource 구현 (KR)
- assignee: coder
- summary: `PykrxSource(DataSource)`. 6자리 숫자→`get_market_ohlcv`, 그 외→`get_index_ohlcv`. 한글 컬럼 매핑, `adj_close=close` 대입(docstring 명시). `fetch_fx`는 NotImplementedError, `list_symbols('KR')`은 KOSPI+KOSDAQ 합산. pykrx 지연 import, monotonic 기반 100ms 최소 간격.
- files: projects/stock-backtest/src/stock_backtest/ingestion/pykrx_source.py

### TASK-009 (DONE) - 2026-04-14T13:05
- title: 거래일 캘린더 모듈 (XKRX/XNYS/CRYPTO 365일 + 교집합)
- assignee: coder
- summary: `get_trading_days`, `is_trading_day`, `previous/next_trading_day`, `common_trading_days`, `union_trading_days`, `MarketNotSupportedError`. exchange_calendars + lru_cache, tz-naive 반환. 2024-01 검증: US 21일, KR 22일, CRYPTO 31일, KR∩US=21. 설치 시 numpy가 2.4.4로 업그레이드되어 pandas ABI 충돌 → numpy<2 (1.26.4)로 다운그레이드 필요.
- files: projects/stock-backtest/src/stock_backtest/backtest/calendar.py

### TASK-010 (DONE) - 2026-04-14T13:25
- title: 수집 파이프라인 (증분, 갭 감지, 재시도, REJECTED 기록)
- assignee: coder
- summary: `IngestionPipeline` 클래스 + `IngestionResult` dataclass. MAX(ohlcv.time)+1 ~ today 범위 산정 → 거래일 캘린더 필터 → DataSource 호출 지수백오프(1/2/4s) 3회 재시도 → close 0/null/NaN 행 제외 후 REJECTED 로그 → UPSERT + SUCCESS/PARTIAL + last_ingested_at 갱신. 자산 단위 예외 격리, logging 사용. repository.py에 모듈-레벨 함수 4개 추가: get_max_ohlcv_time, upsert_ohlcv_bulk, log_ingestion, list_active_assets (기존 클래스 시그니처 변경 없음).
- files: projects/stock-backtest/src/stock_backtest/ingestion/pipeline.py, data/repository.py

### TASK-036 (DONE) - 2026-04-14T13:25
- title: 한국 거주자 세금 모듈 + 단위 테스트
- assignee: coder
- summary: `KrResidentTax`, `RealizedTrade`, `TaxYearState`, `NoopTax`, `build_tax_policy`, `KrResidentTax.from_config`. Decimal 사용, KRW 정수 라운딩. 해외 실현익은 연간 250만 공제 후 22%, 같은 해 손실 상계(carry-over 미지원 — 한계 명시), 국내 주식형 ETF 비과세, 채권/혼합 ETF 및 배당 15.4%, 암호화폐 토글. 연말 roll-over, tax.enabled=false → Noop. 테스트 16개(요구 9 시나리오 포함) 전부 통과.
- files: projects/stock-backtest/src/stock_backtest/backtest/tax.py, projects/stock-backtest/tests/test_tax.py

### TASK-011 (DONE) - 2026-04-14T13:50
- title: 수집 CLI + cron 예제
- assignee: coder
- summary: argparse CLI (`--market KR|US|CRYPTO|ALL`, `--symbols`, `--dry-run`, `--log-level`). market→source 매핑 (KR→PykrxSource, US/CRYPTO→YFinanceSource), `db.get_session` 컨텍스트 매니저로 Pipeline 실행. ALL은 순차 실행, exit code 0/1/2. crontab.example은 CRON_TZ=Asia/Seoul + KR 18:00 / US 07:00 / Crypto 09:00 + 로그 리다이렉트.
- files: projects/stock-backtest/src/stock_backtest/ingestion/cli.py, docker/cron/crontab.example

### TASK-035 (DONE) - 2026-04-14T13:50
- title: 비거래일 방어 모듈
- assignee: coder
- summary: 독립 유틸 `calendar_guard.py` (repository/엔진 통합은 향후 태스크). `NonTradingDayError`, `MissingPriceError`, `validate_trading_day(align=error/previous/next)`, `validate_date_range(strict)`, `align_to_trading_day`(np.searchsorted 벡터화), `assert_universe_coverage`(다자산 결측 집계 에러). 15개 pytest 전부 통과.
- files: projects/stock-backtest/src/stock_backtest/backtest/calendar_guard.py, projects/stock-backtest/tests/test_calendar_guard.py

### TASK-025 (DONE) - 2026-04-14T13:50
- title: market_events seed + 이벤트 기반 계절성
- assignee: coder
- summary: seed_market_events.py에 US 대선 12, 중간선거 11, FOMC 124(최근 5년 실회의 + 이전 근사), 실적시즌 104, KR 대선 3, 총선 4 = 총 258개. `(country, type, event_date)` UNIQUE 제약 없어 SELECT-then-INSERT 멱등. political_cycle.py에 `presidential_term_year_effect`, `election_year_effect`, `fomc_week_effect`, `earnings_season_effect` 4개 함수. 합성 데이터 smoke test 통과.
- files: projects/stock-backtest/scripts/seed_market_events.py, src/stock_backtest/analysis/political_cycle.py, analysis/__init__.py

### TASK-013 (DONE) - 2026-04-14T14:15
- title: 초기 자산 universe 등록 스크립트
- assignee: coder
- summary: scripts/seed_universe.py. 총 81개 자산 (KR 23, US 지수·ETF 38, 채권 9, 원자재 9, CRYPTO 2). `AssetRow` dataclass + 카테고리 빌더, `--dry-run` 옵션, `AssetRepository.get_by_symbol`로 skip 처리. kr_tax_class meta 태깅. FX는 models.py의 CHECK 제약상 assets 제외 → 별도 fx ingestion 경로 필요(블로커). 305080 등 일부 KR 티커는 교차검증 불가로 `ticker_unverified` 태그.
- files: projects/stock-backtest/scripts/seed_universe.py

### TASK-016 (DONE) - 2026-04-14T14:15
- title: 벡터화 백테스트 엔진
- assignee: coder
- summary: engine.py + portfolio.py + fx.py + cache.py 구현. `BacktestEngine.run`이 공통 기간 산출 → 거래일 검증(`assert_universe_coverage`) → Strategy 호출 → 일별 시뮬레이션(체결·FX 환전·세금·연말 rollover). Decimal, market_mode STOCK/CRYPTO/MIXED, sell-first 체결로 현금 부족 완화. pandas<2.2 호환 위해 'ME'→'M' fallback, 초기 매수에 0.995 cushion. smoke test 2개(tax on/off) 통과. 블로커: `OhlcvRepository` 다자산 wide 로드 메서드 부재 → 엔진 내부 헬퍼로 우회.
- files: src/stock_backtest/backtest/engine.py, portfolio.py, fx.py, cache.py, tests/test_engine_smoke.py

### TASK-017 (DONE) - 2026-04-14T14:45
- title: 성과 지표 계산
- assignee: coder
- summary: metrics/performance.py에 cagr, annualized_volatility, sharpe/sortino, max_drawdown, calmar, turnover, win_rate, compute_all 구현. 내부는 float, Decimal coerce. CAGR 연수는 DatetimeIndex면 calendar days/365.25, 아니면 len/252. std=0 경계에서 ±inf 처리. compute_all은 유효 샘플<2일 때 zero bundle 반환. test_performance.py 21 tests 전부 통과.
- files: src/stock_backtest/metrics/performance.py, tests/test_performance.py

### TASK-020 (DONE) - 2026-04-14T14:45
- title: 정적 전략 (FixedWeight + Permanent Portfolio)
- assignee: coder
- summary: strategies/static/fixed_weight.py (pydantic model_validator로 합=1 검증, `@register`), permanent.py (25/25/25/25, 심볼 파라미터화). 설계 #8대로 60/40·올웨더 전용 파일 생략, FixedWeight 파라미터로 표현. 9 tests 전부 통과.
- files: src/stock_backtest/strategies/static/fixed_weight.py, permanent.py, tests/test_static_strategies.py

### TASK-012 (DONE) - 2026-04-14T14:45
- title: 수집 파이프라인 단위/통합 테스트
- assignee: tester
- summary: test_ingestion_pipeline.py 11 tests 전부 통과. MagicMock(spec=DataSource) + patch로 repository/calendar 모킹, sleep_fn 주입으로 지수백오프 수열(1s→2s) 검증. 커버: 정상 증분, 빈 DB 백필, 재시도 3회, FAILED/RateLimit, close=0/NaN REJECTED, 멱등성, 비거래일 필터, 갭 복구, run_for_market 부분실패 격리, SymbolNotFound SKIPPED. 코드 이슈 없음.
- files: projects/stock-backtest/tests/test_ingestion_pipeline.py

### TASK-018 (DONE) - 2026-04-14T15:20
- title: Run 저장/캐싱
- assignee: coder
- summary: cache.py 확장(compute_code_commit_hash, compute_data_hash, is_stale), run_store.py 신규(save_run/find_cached_run/load_run), repository.py 추가: insert_run/bulk_insert_equity/bulk_insert_trades/insert_metrics/get_run_by_hash. 엔진 자체 미수정. ohlcv에 updated_at 부재 → MAX(time)+COUNT(*) freshness proxy. NaN/inf 메트릭 자동 스킵. 16 tests + 전체 101 passed.
- files: src/stock_backtest/backtest/cache.py, run_store.py, data/repository.py, tests/test_run_store.py

### TASK-021 (DONE) - 2026-04-14T15:20
- title: 동적 전략 1 (Momentum, Dual Momentum)
- assignee: coder
- summary: momentum.py(상대 모멘텀 top_n + 양수 필터, equal/rank 가중), dual_momentum.py(GEM 단순화: risky 1위가 양수면 해당 자산, 아니면 safe). lookback 부족은 0. @register 자동 등록. 11 tests 통과.
- files: src/stock_backtest/strategies/dynamic/momentum.py, dual_momentum.py, tests/test_momentum.py

### TASK-022 (DONE) - 2026-04-14T15:20
- title: 동적 전략 2 (VAA, Risk Parity)
- assignee: coder
- summary: vaa.py(Keller 12*r1+4*r3+2*r6+r12 스코어, breadth_threshold 기반 공격/방어 전환), risk_parity.py(inverse-volatility, std=0 제외, lookback 부족 equal fallback). 8 tests 통과.
- files: src/stock_backtest/strategies/dynamic/vaa.py, risk_parity.py, tests/test_vaa_riskparity.py

### TASK-019 (DONE) - 2026-04-14T15:20
- title: 백테스트 엔진 회귀 테스트
- assignee: tester
- summary: test_engine_regression.py 9 시나리오 전부 통과(총 101 + 9 = 110). 현금 100%, buy-and-hold 2x, 월말 60/40 유지, FX 스프레드 영향, MissingPriceError, 세금 공제 이하/이상, 세금 on/off 비교, CRYPTO 주말 포함, known-good analytical ±1%. **코드 이슈 2건 → TASK-037/038로 이관**: (1) Portfolio._ensure_cash에서 fx_spread 부호 버그 (역방향 환전에서 equity 개선됨), (2) engine _build_rebalance_trades의 50bps 하드코딩 쿠션은 fx_spread>50bps에서 InsufficientFundsError.
- files: projects/stock-backtest/tests/test_engine_regression.py

### TASK-037 (DONE) - 2026-04-14T15:50
- title: Portfolio._ensure_cash FX-spread 부호 버그 수정
- assignee: coder
- summary: 기존 `FXConverter.convert` 역호출이 spread를 잘못된 방향으로 적용해 wider spread → 더 적은 source 소요(=equity 개선)되던 버그. `fx.py`에 `convert_for_target(target, src, tgt, date, apply_spread)` 신규 헬퍼 추가(내부 mid rate 환전량 × (1 + half_spread)). `_ensure_cash`가 이를 호출. monotonic 검증 테스트 추가(0/100/300bps), 11 tests 통과.
- files: src/stock_backtest/backtest/fx.py, portfolio.py, tests/test_portfolio_fx.py

### TASK-038 (DONE) - 2026-04-14T15:50
- title: 동적 현금 쿠션
- assignee: coder
- summary: engine에 `_compute_cushion_bps(universe_ccy, base, markets)` 추가. 공식: max_commission_buy + max_slippage + (cross-currency면 max_fx_spread) + 10bps safety. 상한 500bps clamp + 초과 시 warning. universe가 단일 통화면 fx_spread 0. fx_spread 100bps도 정상 실행. 16/16 cushion+regression+smoke, 전체 125/125 통과.
- files: src/stock_backtest/backtest/engine.py, tests/test_engine_cushion.py

### TASK-023 (DONE) - 2026-04-14T15:50
- title: 전략 통합 회귀 테스트
- assignee: tester
- summary: test_strategy_integration.py 30 tests 통과. 레지스트리 6개 전략 검증, params_schema 인스턴스화, weights 불변식(index/columns/row sum/non-neg), pydantic ValidationError, 빈 리밸런스일, BacktestEngine smoke (합성 GBM 2~3년, fake price_loader). engine 시그니처 드리프트에 대비해 pytest.skip 가드 — 실제 스킵 없음. 코드 이슈 없음. (메모: 환경의 dash plugin autoload 버그로 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 필요.)
- files: projects/stock-backtest/tests/test_strategy_integration.py

### TASK-027 (DONE) - 2026-04-14T15:50
- title: Dash 앱 스켈레톤
- assignee: coder
- summary: `create_app()` 팩토리 + `use_pages=True` 멀티페이지. 4개 placeholder (backtest/seasonality/data_explorer/history), `make_navbar()` 컴포넌트, `db_session.get_db_session()` lazy wrapper. `python -m stock_backtest.web.app`로 기동(Dash 2.x/3.x `run`→`run_server` 폴백). 환경 Dash 4.1.0이 comm import-time 버그 있으나 코드는 표준 API 준수.
- files: src/stock_backtest/web/app.py, components/layout.py, db_session.py, pages/{backtest,seasonality,data_explorer,history}.py, 각 __init__.py

### TASK-026 (DONE) - 2026-04-14T16:25
- title: 계절성 통계 유의성 검정 + 분석 모듈 테스트
- assignee: tester
- summary: analysis/stats.py 신규: welch_t_test(scipy), bootstrap_mean_diff/bootstrap_ci(numpy default_rng), annotate_significance(***, **, *). NaN/소표본/빈 표본 안전 처리. analysis/__init__.py에 export. test_seasonality_stats.py 15 tests 전부 통과 (PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 필요).
- files: src/stock_backtest/analysis/stats.py, __init__.py, tests/test_seasonality_stats.py

### TASK-028 (DONE) - 2026-04-14T16:25
- title: 웹 백테스트 페이지
- assignee: coder
- summary: 전략 Dropdown → pydantic params_schema.model_fields 순회로 동적 폼(bool/int/float/Literal/list/dict/str 매핑), pattern-matching id. Universe Textarea(`SYMBOL@MARKET`), DatePickerRange, base_currency/market_mode/initial_capital. 실행 콜백: compute_run_hash → find_cached_run + is_stale → 캐시 재사용 or engine.run + save_run. Plotly equity/drawdown + 성과지표 DataTable + run_id/code_hash/data_hash/STALE 배너. session_factory는 data.db.get_session 위임. 환경 Dash comm 버그로 import 검증은 ast.parse로 대체.
- files: src/stock_backtest/web/pages/backtest.py

### TASK-030 (DONE) - 2026-04-14T16:25
- title: 웹 데이터 탐색 페이지
- assignee: coder
- summary: 자산 multi-Dropdown(페이지 로드 시 lazy로 active 자산 로드), DatePickerRange(default 5y), RadioItems(Price/Return/Correlation), Normalize 체크박스. OhlcvRepository.get_range → wide DataFrame. Price=line(normalize 옵션), Return=cumprod(1+pct_change), Correlation=px.imshow. DB 실패 시 empty figure + 상태 메시지.
- files: src/stock_backtest/web/pages/data_explorer.py

### TASK-032 (DONE) - 2026-04-14T16:25
- title: Cron 설치 가이드
- assignee: coder
- summary: docs/cron.md 신규 (KST 스케줄 표, CRON_TZ=Asia/Seoul, crontab.example 링크, 로그 디렉토리 권한, 문제 해결, systemd timer 대안). README 맨 하단 ## Cron 설치 섹션 추가(docs/cron.md 링크). TASK-011의 crontab.example 유지.
- files: projects/stock-backtest/docs/cron.md, README.md

## Round 10 (2026-04-14T17:00) — 병렬 3건

- TASK-029 DONE (coder): `web/pages/seasonality.py` 완전 구현. 7개 카테고리 러너(monthly/day_of_week/sell_in_may/halloween/presidential_term/fomc/earnings_season), Welch t-test + bootstrap CI, 유의성 DataTable.
- TASK-031 DONE (coder): `web/pages/history.py` 완전 구현. 최근 100 run 로드, 전략/기간 필터, STALE 강조, multi-select equity overlay, metrics pivot.
- TASK-033 DONE (tester): `tests/test_ingestion_e2e.py` 6 시나리오 PASS (실패→복구, 부분→복구, 멱등, RateLimit, multi-asset 부분실패, close=0 REJECTED). 관찰: REJECTED 재수집은 MAX(time)+1 전략으로 커버 불가 — 후속 갭 스캐너 태스크에서 처리 필요.

## Round 11 (2026-04-14T17:20) — 최종

- TASK-034 DONE (coder): `README.md` 10개 섹션(소개/아키텍처/설치/수집/백테스트/전략 추가법/웹/테스트/디렉토리/면책) 작성. 실제 CLI flag/코드 확인 후 인용.

## Round 12 (2026-04-14T18:00) — TASK-014 [사용자 실행]

- TASK-014 DONE (tester, Execution=user): 초기 백필 + 품질 검증.
  - US 56자산 261,047행 SUCCESS, KR ETF 20 + CRYPTO 2 PARTIAL(상장일 미설정으로 기대치 과대, 실데이터 정상), KR 인덱스 3 FAILED.
  - close=0/NULL 이상치 0건.
  - Bug 발견: pykrx 인덱스 fetch `KeyError: '지수명'` (API 호환성) → TASK-039 등록.
  - Observation: PARTIAL 판정 로직이 자산 상장일을 반영하지 않음 → retrospective 이관.

## Round 13 (2026-04-14T18:30) — TASK-039

- TASK-039 DONE (coder): pykrx 1.2.4 상류 버그(`KeyError: '지수명'`) 확인 — 업그레이드/숫자ticker로 해결 불가.
  해결: `PykrxSource.fetch_ohlcv` 진입부에 KR 인덱스 심볼 yfinance fallback 분기 추가
  (KS11/KQ11/KS200 → ^KS11/^KQ11/^KS200). 파이프라인 계약 유지.
  검증: DB에 KS11=4921, KQ11=4921, KS200=4877 rows (2006-04-19~2026-04-14) 적재.
  트레이드오프: pykrx_source가 yfinance_source를 지연 import하는 경계 흐림 — 상류 수정 시 롤백 가능한 형태로 주석 처리.

## Round 14 (2026-04-14T19:00) — TASK-040

- TASK-040 DONE (coder): 이평선 전략 첫 세트.
  신규 디렉토리 `strategies/dynamic/moving_average/` + 4 파일.
  - `_common.py`: rolling_mean, crossover_signal(NaN→0), seasonal_mask(halloween/sell_in_may/presidential_term/custom_months), combine_signals(and/weighted).
  - `crossover.py`: `MovingAverageCrossover` (registry name: `moving_average_crossover`).
  - `seasonal.py`: `SeasonalMovingAverage` (registry name: `seasonal_moving_average`).
  base 인터페이스 제약상 `election_dates` 는 params 필드(ISO string list)로 노출 — 웹/엔진 레이어에서 `market_events` 로 조회 후 주입 필요.
  골든 크로스 2020-10-08 / 데드 크로스 2021-04-16 스팟체크 통과. registry 자동 스캔 확인.

## Round 15 (2026-04-14T19:30) — TASK-041 웹 UX 보완

- TASK-041 DONE (coder):
  (a) `web/pages/home.py` 신규 + navbar "홈" 링크 추가. `/` 404 해결.
  (b) `backtest.py` 에서 선택 전략의 ClassVar description 을 폼 상단 회색 이탤릭 박스로 렌더.
  (c) Universe Textarea 아래 도움말 caption (`@시장` 문법, required_universe fallback).
  (d) MovingAverageCrossover/SeasonalMovingAverage 의 Field description 한글화 + 전략 description 2~4문장 확장.
  (e) 라벨(굵은 필드명) + description(회색 작은 글씨) 별도 줄 렌더.
  `ctl restart stock-backtest-web` 후 `/`, `/backtest` HTTP 200 확인.

---

# V2 Reset (2026-04-15~)

## Round V2-1 (2026-04-15) — Phase 1 착수

- TASK-101 DONE (coder): 웹 레이어 전면 삭제.
  `src/stock_backtest/web/` 디렉토리 제거 (app.py, db_session.py, components/, pages/ 전부).
  `/home/jai/.a_service_control/services.yaml` 의 `stock-backtest-web:` 블록 제거 (사용자 확인 lint 반영 완료).
  완료조건 중 README.md (line 145, 147) 와 `scripts/run_web.sh` 의 web 언급은 TASK-103 범위로 명시적 보존.
  검증: `ls web/` not found, services.yaml grep 0 hit, `.venv/bin/python -c "import stock_backtest"` PASS.

- TASK-102 DONE (coder): 불필요 전략 + 테스트 삭제.
  전략 9개(momentum, dual_momentum, risk_parity, vaa, moving_average/{crossover,multi_crossover,seasonal,_common}, permanent) + 테스트 4개(test_momentum, test_vaa_riskparity, test_static_strategies, test_strategy_integration) 제거.
  `simple.py` 에서 `_common.rolling_mean` 의존을 내부 인라인으로 전환(_common.py 삭제 대응).
  `__init__.py` 3개의 docstring 을 V2 범위로 정리.
  검증: pytest --collect-only 118 수집 통과, list_strategies() 가 ['fixed_weight', 'simple_moving_average'] 2개 정확.
  메모: Tester 발견 — venv 에 pytest 미설치 상태였음 → TASK-103 dev 의존성 정비 범위로 자연히 흡수.

- TASK-103 DONE (coder): CLI/문서/의존성 정리.
  `scripts/run_web.sh` 삭제. README.md 전면 재작성(Dash/웹 섹션 제거, web/ 디렉토리 트리 제거, V2 Reset 안내 추가).
  requirements.txt 에서 dash/plotly 제거(plotly 코드 사용 0건 grep 확인).
  requirements-dev.txt 에 pytest-asyncio 추가(TASK-102 Tester 지적 반영).
  docs/cron.md / pyproject.toml 에는 기존 관련 언급 없음 확인, 변경 없음.
  검증: pip install --dry-run PASS, import stock_backtest PASS, grep 잔존 1건은 V2 Reset 진행 안내로 의도된 허용.

## Phase 1 완료 (2026-04-15)

V1 잔재 정리 완료. Phase 2 재구축 진입 가능. 다음은 TASK-111(Cash 타입 도입) — 의존성 없음, 독립 실행 가능.
