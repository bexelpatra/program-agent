# Task Board

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| TASK-001 | 프로젝트 초기화 (requirements, .env.example, README, .gitignore, 디렉토리 골격) | coder | DONE | HIGH | - | 2026-04-14T10:00 | 2026-04-14T10:30 |
| TASK-002 | docker-compose.yml 작성 (Postgres 16 + TimescaleDB) 및 로컬 기동 검증 | coder | DONE | HIGH | TASK-001 | 2026-04-14T10:00 | 2026-04-14T10:50 |
| TASK-003 | DB 스키마 마이그레이션 작성 (assets, ohlcv hypertable, fx_rates, market_events, corporate_actions, ingestion_log, backtest_runs, backtest_equity hypertable, backtest_trades, backtest_metrics) | coder | DONE | HIGH | TASK-002 | 2026-04-14T10:00 | 2026-04-14T11:30 |
| TASK-004 | SQLAlchemy ORM 모델 + db 세션/연결 레이어 + repository 골격 | coder | DONE | HIGH | TASK-003 | 2026-04-14T10:00 | 2026-04-14T11:55 |
| TASK-005 | config/defaults.yaml + 설정 로더 (commission, slippage, fx_spread, rebalance, base_currency, market별 오버라이드, **tax 프로파일**) | coder | DONE | HIGH | TASK-001 | 2026-04-14T10:00 | 2026-04-14T12:15 |
| TASK-006 | DataSource 추상 인터페이스 (fetch_ohlcv, fetch_fx, list_symbols) 정의 | coder | DONE | HIGH | TASK-004 | 2026-04-14T10:00 | 2026-04-14T12:45 |
| TASK-007 | yfinance 기반 DataSource 구현 (US/원자재/암호화폐/FX) + rate limit 준수 | coder | DONE | HIGH | TASK-006 | 2026-04-14T10:00 | 2026-04-14T13:05 |
| TASK-008 | pykrx 기반 DataSource 구현 (KR 지수/ETF) | coder | DONE | HIGH | TASK-006 | 2026-04-14T10:00 | 2026-04-14T13:05 |
| TASK-009 | 거래일 캘린더 모듈 (KRX, NYSE, Crypto 365일, 공통 기간 교집합 계산) - exchange_calendars 사용 | coder | DONE | HIGH | TASK-006 | 2026-04-14T10:00 | 2026-04-14T13:05 |
| TASK-010 | 수집 파이프라인 (DB 기반 증분, 갭 감지, 재시도 3회 지수백오프, ingestion_log 기록, UPSERT, **비거래일 필터 + close=0/null REJECTED 기록**) | coder | DONE | HIGH | TASK-007, TASK-008, TASK-009 | 2026-04-14T10:00 | 2026-04-14T13:25 |
| TASK-011 | 수집 CLI 엔트리포인트 (`python -m stock_backtest.ingestion.cli --market KR/US/CRYPTO`) + cron 예제 | coder | DONE | MEDIUM | TASK-010 | 2026-04-14T10:00 | 2026-04-14T13:50 |
| TASK-012 | 수집 파이프라인 단위/통합 테스트 (갭 복구, 재시도, 멱등성) | tester | DONE | HIGH | TASK-010 | 2026-04-14T10:00 | 2026-04-14T14:45 |
| TASK-013 | 초기 자산 universe 등록 스크립트 (KR 지수/대표 ETF 20~30, US 지수+S&P섹터+국가 ETF 40~50, 채권 ETF, 금/은/원자재 ETF, BTC/ETH, fx 페어) | coder | DONE | HIGH | TASK-010 | 2026-04-14T10:00 | 2026-04-14T14:15 |
| TASK-014 | 초기 백필 실행 및 데이터 품질 검증 (결측/이상치/커버리지 리포트) [Execution=user] | tester | DONE | HIGH | TASK-013 | 2026-04-14T10:00 | 2026-04-14T18:00 |
| TASK-039 | pykrx KR 인덱스(KS11/KQ11/KS200) fetch 시 `KeyError: '지수명'` 수정 — pykrx 업데이트 또는 yfinance fallback (`^KS11`, `^KQ11`) 고려 | coder | DONE | HIGH | TASK-014 | 2026-04-14T18:00 | 2026-04-14T18:30 |
| TASK-040 | 이평선 전략 첫 세트: `strategies/dynamic/moving_average/` 디렉토리 + `_common.py`(공통 헬퍼) + `crossover.py`(MovingAverageCrossover) + `seasonal.py`(SeasonalMovingAverage, halloween/sell_in_may/presidential_term/custom_months × and/weighted 결합) | coder | DONE | MEDIUM | TASK-015, TASK-016, TASK-025 | 2026-04-14T18:40 | 2026-04-14T19:00 |
| TASK-041 | 웹 UX 보완: (a) `/` 홈 페이지 추가, (b) 백테스트 페이지에 선택 전략의 ClassVar description 렌더, (c) Universe 입력에 도움말, (d) risky_symbol/safe_symbol/fast_window/slow_window 등 필드 description 을 초보자도 이해할 수 있도록 확장 | coder | DONE | MEDIUM | TASK-028, TASK-040 | 2026-04-14T19:10 | 2026-04-14T19:30 |
| TASK-015 | Strategy 추상 베이스 + pydantic params_schema + 파일 자동 스캔 registry | coder | DONE | HIGH | TASK-005 | 2026-04-14T10:00 | 2026-04-14T12:45 |
| TASK-016 | 백테스트 엔진 (벡터화, 리밸런싱, 수수료/슬리피지, FX 환전비용, base_currency equity 산출, market_mode STOCK/CRYPTO/MIXED, **비거래일 검증, 세금 모듈 연동**) | coder | DONE | HIGH | TASK-009, TASK-015, TASK-035, TASK-036 | 2026-04-14T10:00 | 2026-04-14T14:15 |
| TASK-017 | 성과 지표 계산 (CAGR, Vol, Sharpe, Sortino, MDD, Calmar, Turnover, Win rate) | coder | DONE | HIGH | TASK-016 | 2026-04-14T10:00 | 2026-04-14T14:45 |
| TASK-018 | Run 저장/캐싱 (run_hash, code_commit_hash, data_hash, STALE 판정) | coder | DONE | MEDIUM | TASK-016, TASK-017 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-019 | 백테스트 엔진 단위 테스트 + 단순 전략 회귀 테스트 (known-good 시나리오) | tester | DONE | HIGH | TASK-016, TASK-017 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-020 | 정적 전략 구현 (FixedWeight 일반화: 60/40, All Weather, Permanent Portfolio) | coder | DONE | HIGH | TASK-015, TASK-016 | 2026-04-14T10:00 | 2026-04-14T14:45 |
| TASK-021 | 동적 전략 구현 1: Momentum, Dual Momentum | coder | DONE | MEDIUM | TASK-020 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-022 | 동적 전략 구현 2: VAA (Vigilant Asset Allocation), Risk Parity | coder | DONE | MEDIUM | TASK-020 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-037 | Portfolio._ensure_cash FX-spread 부호 버그 수정 (역방향 환전에서도 스프레드가 equity를 악화시키도록) | coder | DONE | HIGH | TASK-019 | 2026-04-14T15:20 | 2026-04-14T15:50 |
| TASK-038 | engine `_build_rebalance_trades`의 50bps 하드코딩 현금 쿠션을 fx_spread+commission 기반 동적 쿠션으로 교체 | coder | DONE | HIGH | TASK-019 | 2026-04-14T15:20 | 2026-04-14T15:50 |
| TASK-023 | 전략 단위 테스트 (정적+동적) | tester | DONE | HIGH | TASK-020, TASK-021, TASK-022 | 2026-04-14T10:00 | 2026-04-14T15:50 |
| TASK-024 | 기본 계절성 분석 (월/요일/월말/Sell-in-May/Halloween) | coder | DONE | MEDIUM | TASK-004 | 2026-04-14T10:00 | 2026-04-14T12:45 |
| TASK-025 | market_events seed (미 대선/중간선거/FOMC/실적시즌, 한국 대선/총선) + 이벤트 기반 계절성 분석 (선거/임기년차/FOMC 주간) | coder | DONE | MEDIUM | TASK-024 | 2026-04-14T10:00 | 2026-04-14T13:50 |
| TASK-026 | 계절성 통계 유의성 검정 (t-test, 부트스트랩) + 분석 모듈 테스트 | tester | DONE | MEDIUM | TASK-024, TASK-025 | 2026-04-14T10:00 | 2026-04-14T16:25 |
| TASK-027 | Dash 앱 스켈레톤 (라우팅, 공통 레이아웃, DB 연결) | coder | DONE | MEDIUM | TASK-018 | 2026-04-14T10:00 | 2026-04-14T15:50 |
| TASK-028 | 웹 페이지 (c): 전략 백테스트 (전략 선택 → 파라미터 폼 자동생성 → universe/기간 → 실행 → equity/drawdown/지표) | coder | DONE | MEDIUM | TASK-027, TASK-020 | 2026-04-14T10:00 | 2026-04-14T16:25 |
| TASK-029 | 웹 페이지 (b): 계절성 분석 (자산 선택 → 이벤트 카테고리 → 히트맵/박스플롯/유의성 표시) | coder | DONE | MEDIUM | TASK-027, TASK-026 | 2026-04-14T10:00 | 2026-04-14T17:00 |
| TASK-030 | 웹 페이지 (a): 데이터 탐색 (가격/수익률/상관관계) | coder | DONE | LOW | TASK-027 | 2026-04-14T10:00 | 2026-04-14T16:25 |
| TASK-031 | 웹 페이지 (d): 백테스트 이력 비교 (여러 run 겹쳐 그리기, STALE 플래그 노출) | coder | DONE | LOW | TASK-028 | 2026-04-14T10:00 | 2026-04-14T17:00 |
| TASK-032 | Cron 스케줄 설치 가이드 + 샘플 crontab (KR 18:00, US +1일 07:00, Crypto 09:00 KST) | coder | DONE | LOW | TASK-011 | 2026-04-14T10:00 | 2026-04-14T16:25 |
| TASK-033 | 수집 복구 시나리오 엔드투엔드 테스트 (실패 주입 → 다음 실행에서 갭 자동 복구 검증) | tester | DONE | MEDIUM | TASK-011, TASK-012 | 2026-04-14T10:00 | 2026-04-14T17:00 |
| TASK-034 | README / 사용자 매뉴얼 (설치, 수집, 전략 추가법, 웹 사용법) | coder | DONE | LOW | TASK-028, TASK-029, TASK-032 | 2026-04-14T10:00 | 2026-04-14T17:20 |
| TASK-035 | 비거래일 방어 모듈 (repository/엔진에서 거래일 캘린더 검증, 비거래일·결측 구간 명시적 에러, 직전 거래일 정렬 옵션) | coder | DONE | HIGH | TASK-009 | 2026-04-14T10:00 | 2026-04-14T13:50 |
| TASK-036 | 한국 거주자 세금 모듈 (해외 자산 양도세 22%/연 250만원 공제, 해외 배당세 15.4%, 국내 ETF 과세 분류, 암호화폐 토글, 회계연도 누적/초기화) + 엔진 연동 + 단위 테스트 | coder | DONE | HIGH | TASK-005, TASK-015 | 2026-04-14T10:00 | 2026-04-14T13:25 |
| TASK-042 | 전략 파라미터 폼 렌더러 dispatch 리팩터 + `asset_symbol` 위젯 메타데이터(pydantic `json_schema_extra`) 도입 → 검색 가능한 자산 Dropdown 렌더 + MovingAverageCrossover.risky_symbol/safe_symbol 적용 | coder | DONE | HIGH | TASK-041 | 2026-04-14T19:40 | 2026-04-14T19:50 |
| TASK-043 | `SimpleMovingAverage` 전략 구현 (price_{t-1} > MA(window)_{t-1} → risky, else safe) + asset_symbol 위젯 적용 | coder | DONE | MEDIUM | TASK-040, TASK-042 | 2026-04-14T19:40 | 2026-04-14T20:00 |
| TASK-044 | `MultiMovingAverageCrossover` 전략 구현 (`windows: list[int]`, 정배열 판정 `price > MA(w1) > … > MA(wN)` with `include_price: bool = True`) + `list[int]` 폼 코어션 | coder | DONE | MEDIUM | TASK-040, TASK-042 | 2026-04-14T19:40 | 2026-04-14T20:00 |
| TASK-045 | 백테스트 폼 UX 개선: 파라미터 라벨 한글화, Universe 입력을 Details 접기 + 자동결정 안내, 기간 입력을 텍스트 Input(YYYY-MM-DD) + 프리셋(1Y/3Y/5Y/10Y/20Y/전체) 버튼으로 교체 | coder | DONE | MEDIUM | TASK-042 | 2026-04-14T19:40 | 2026-04-14T20:10 |
| TASK-046 | USD 합성 자산 등록 (symbol=USD, market=CASH, asset_type=CASH, currency=USD, adj_close=1.0 고정) + assets 테이블 seed + OHLCV 백필 스크립트 (2000-01-01 ~ today 일별 1.0) | coder | DONE | HIGH | TASK-013 | 2026-04-14T20:20 | 2026-04-14T20:30 |
| TASK-047 | `asset_symbol_list` 위젯 추가 (`dcc.Dropdown(multi=True)` 자산 검색 다중 선택) + `_coerce_field_value` 처리 + Momentum/DualMomentum/VAA 등 기존 `list[str]` universe 필드 전수 전환 | coder | DONE | HIGH | TASK-042 | 2026-04-14T20:20 | 2026-04-14T20:30 |
| TASK-048 | `asset_weight_map` 위젯 추가 (자산 Dropdown + 비중 Input 페어의 동적 행 추가/삭제 UI, 합계 실시간 표시) + FixedWeight/RiskParity 등 `dict[str, float]` 필드 전환 | coder | DONE | HIGH | TASK-047 | 2026-04-14T20:20 | 2026-04-14T20:45 |
| TASK-051 | 엔진/Portfolio 에 `_CASH_` 예약 심볼 1급 지원 — `generate_weights` 의 `_CASH_` 컬럼 비중을 `cash_by_ccy[base_currency]` 잔고로 해석, prices 조회 시 제외, trade 기록 없음 | coder | DONE | HIGH | TASK-016, TASK-046 | 2026-04-14T21:00 | 2026-04-14T21:40 |
| TASK-053 | 새 DSL 구현 + MA 전략 3종(crossover/simple/multi) 마이그레이션 — `risky_symbol`/`safe_symbol` 제거, `target_symbol`/`exit_action`(cash|rotate)/`rotate_symbol` 도입. 기본 exit_action="cash" → `_CASH_` 비중 반환 | coder | DONE | HIGH | TASK-051 | 2026-04-14T21:00 | 2026-04-14T22:00 |
| TASK-054 | `_load_asset_options()` 에 `_CASH_` 가상 옵션 prepend (라벨: "현금 대기 · \_CASH\_") + FixedWeightParams.weights validator 에 `_CASH_` 키 허용 + Momentum/DualMomentum/VAA 의 universe/assets 필드 validator 에 `_CASH_` 허용 | coder | DONE | HIGH | TASK-051 | 2026-04-14T21:00 | 2026-04-14T22:00 |
| TASK-056 | SeasonalMovingAverage 전략을 새 DSL(target_symbol/exit_action/rotate_symbol)로 마이그레이션 + _FIELD_LABEL_KO 라벨 보강 + tests/ 내 옛 DSL 참조 확인 | coder | DONE | MEDIUM | TASK-053 | 2026-04-14T22:00 | 2026-04-14T22:10 |
| TASK-052 | FX TradeRecord 스키마 확장 — `backtest_trades.side` CHECK 에 `"FX"` 추가, `asset_id` nullable, `currency_from`/`currency_to`/`fx_rate`/`spread_bps` 컬럼 추가 (alembic migration) + `_ensure_cash` 에서 FX trade 생성 + run_store 저장 로직 반영 | coder | DONE | HIGH | TASK-016 | 2026-04-14T21:00 | 2026-04-14T21:20 |
| TASK-055 | 새 DSL 및 `_CASH_` 회귀 검증 — 기존 DB 저장 run 과의 결과 비교(동일 조건), `_CASH_` 비중 있는 백테스트의 equity/잔고 일치 확인, FX trade 기록 검증 | tester | CANCELLED | HIGH | TASK-053, TASK-054 | 2026-04-14T21:00 | 2026-04-15 |

<!--
결번 메모:
- TASK-049, TASK-050: 등록된 적 없음 (할당 단계에서 누락 추정, 추적 불가).
- TASK-053, TASK-054: 한때 DONE/TODO 두 행이 중복 등록되어 있었음. 2026-04-15 정리 시 TODO 중복 행을 제거하고 DONE 행만 유지.
- TASK-055: V2 Reset 결정(2026-04-15)으로 V1 DSL 회귀 검증은 무의미해져 CANCELLED. V2 에서 golden snapshot + API 통합테스트로 재설계.
-->

---

# V2 Reset — 태스크 보드 (2026-04-15~)

V2 방향은 `architecture.md` 의 `# V2 Reset` 섹션 참조. 번호는 TASK-101 부터 신규 할당.

## Phase 1 — 삭제/정리

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| TASK-101 | 웹 레이어 전면 삭제 — `src/stock_backtest/web/` 디렉토리 완전 제거, `/home/jai/.a_service_control/services.yaml` 에서 `stock-backtest-web:` 블록(line 51~) 제거. 완료 조건: (1) `ls projects/stock-backtest/src/stock_backtest/web` 가 not found, (2) `grep -r "stock_backtest.web\|from .web\|stock-backtest-web" projects/stock-backtest /home/jai/.a_service_control/services.yaml` 0 hit, (3) `python -c "import stock_backtest"` 성공 | coder | DONE | HIGH | - | 2026-04-15 | 2026-04-15 |
| TASK-102 | 불필요 전략 + 테스트 삭제 — 전략 파일: `src/stock_backtest/strategies/dynamic/{momentum.py, dual_momentum.py, risk_parity.py, vaa.py}`, `dynamic/moving_average/{crossover.py, multi_crossover.py, seasonal.py, _common.py}`, `static/permanent.py`. 테스트 파일: `tests/test_momentum.py`, `tests/test_vaa_riskparity.py`, `tests/test_static_strategies.py`, `tests/test_strategy_integration.py` (통합 테스트는 V2 에서 재설계), `tests/test_seasonality_*` (seasonal 전략 연동 부분만). 완료 조건: (1) 위 파일 모두 부재, (2) `pytest --collect-only` 에러 없음, (3) `python -c "from stock_backtest.strategies import list_strategies; print(list_strategies())"` 가 `simple_moving_average`, `fixed_weight` 2개만 반환 | coder | DONE | HIGH | - | 2026-04-15 | 2026-04-15 |
| TASK-103 | CLI/문서/의존성 정리 — (a) `projects/stock-backtest/scripts/run_web.sh` 삭제, (b) `README.md` 에서 웹/대시보드/`/backtest` URL 언급 제거, (c) `docs/cron.md` 에서 웹 관련 언급 제거, (d) `requirements.txt`/`pyproject.toml` 에서 `dash`, `dash-*`, `plotly`(다른 곳에서 쓰이지 않으면) 의존성 제거. 완료 조건: (1) `grep -ri "dash\|plotly\|/backtest\|run_web" projects/stock-backtest/{README.md,docs,requirements.txt,pyproject.toml}` 0 hit, (2) `pip install -r requirements.txt` dry-run 성공 | coder | DONE | MEDIUM | TASK-101 | 2026-04-15 | 2026-04-15 |

## Phase 2 — Backend 재구축 (API-first)

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| TASK-111 | `Cash` 타입 + `AssetRef = Asset \| Cash` 태그 유니온 도입 — 데이터 모델/pydantic 스키마/직렬화 규칙 정의 (`{"type":"cash","currency":"USD"}` / `{"type":"asset","symbol":"SPY","market":"US"}`). 타입 정의 자체는 독립적이며, 엔진/저장소의 `"_CASH_"` 문자열 경로 치환은 TASK-115에서 수행 | coder | TODO | HIGH | - | 2026-04-15 | 2026-04-15 |
| TASK-112 | 슬림 전략 인터페이스 정의 — `Strategy` 프로토콜(params_schema, required_universe, generate_signal), `Signal` 타입(DataFrame[date, AssetRef → weight]), `SignalMask` 프로토콜(Phase 3 composer 대비) | coder | TODO | HIGH | TASK-111 | 2026-04-15 | 2026-04-15 |
| TASK-113 | `SimpleMovingAverage` 재구현 — 새 인터페이스 기반. `price_{t-1} > MA(window)_{t-1}` → target 100%, else Cash 100%. params: `target: AssetRef`, `window: int` | coder | TODO | HIGH | TASK-112 | 2026-04-15 | 2026-04-15 |
| TASK-114 | `FixedWeight` 재구현 — 새 인터페이스 기반. params: `weights: dict[AssetRef, float]`, `rebalance: "annual"\|"quarterly"\|"monthly"`. `AssetRef` 키에 Cash 허용 | coder | TODO | HIGH | TASK-112 | 2026-04-15 | 2026-04-15 |
| TASK-115 | 엔진 `_CASH_` 문자열 경로 전수 제거 + `AssetRef` 기반으로 재배선 — prices 조회, trade 기록, data_hash, run_store 저장 로직, 세금/FX 모듈 연동점 수정 | coder | TODO | HIGH | TASK-111, TASK-113, TASK-114 | 2026-04-15 | 2026-04-15 |
| TASK-116 | OpenAPI 초안 작성 — `projects/stock-backtest/docs/openapi.yaml`. 엔드포인트: `/health`, `/strategies`, `/assets*`, `/backtests*` (POST/GET/DELETE). 에러 응답 스키마 (`stage/type/message/request_ctx/trace_id`). 비동기 job 상태 스키마 | coder | TODO | HIGH | TASK-112 | 2026-04-15 | 2026-04-15 |
| TASK-117 | FastAPI 스켈레톤 — `src/stock_backtest/api/` 구조, 앱 팩토리, 전역 예외 핸들러(에러 계약 구현), trace_id 미들웨어, CORS 설정(`http://localhost:5173` Vue dev 기본 포트 + 환경변수 `STOCK_BACKTEST_CORS_ORIGINS` 로 추가 허용), **서버 포트 `8051` 고정** (기존 8050 웹은 삭제됨), `scripts/run_api.sh` 추가, `/home/jai/.a_service_control/services.yaml` 에 `stock-backtest-api` 엔트리 등록 (port: 8051, depends_on: [stock-backtest-db]) | coder | TODO | HIGH | TASK-116 | 2026-04-15 | 2026-04-15 |
| TASK-118 | 조회 엔드포인트 구현 — `GET /strategies` (pydantic→JSON Schema 자동 변환), `GET /assets` (q/market/asset_type 필터, pagination), `GET /assets/{id}`, `GET /assets/{id}/ohlcv` | coder | TODO | HIGH | TASK-117 | 2026-04-15 | 2026-04-15 |
| TASK-119 | 백테스트 job 모델 구현 — `POST /backtests` → pending row 삽입 + BackgroundTasks 트리거, 워커에서 엔진 실행(진행률 업데이트), `GET /backtests/{run_id}` 상태, `GET /backtests/{run_id}/result` 완료 결과, `DELETE /backtests/{run_id}` 취소/삭제 | coder | TODO | HIGH | TASK-115, TASK-117 | 2026-04-15 | 2026-04-15 |
| TASK-120 | 백테스트 job 동시성/취소/복구 검증 — 동시 2 job 독립성, 취소 시 DB 정리, 워커 크래시 시 pending/running 복구 정책 구현 및 테스트 | tester | TODO | HIGH | TASK-119 | 2026-04-15 | 2026-04-15 |
| TASK-121 | Golden snapshot 테스트 — 2 전략 × 3 시나리오 = 6 케이스. 현재 엔진 결과를 `tests/golden/<scenario>.json` 스냅샷으로 저장, pytest 에서 diff 검증. 스냅샷 생성용 pytest fixture 포함 | tester | TODO | HIGH | TASK-113, TASK-114, TASK-115 | 2026-04-15 | 2026-04-15 |
| TASK-122 | API 계약 테스트 — schemathesis 로 OpenAPI fuzz + 에러 응답 형태 확인 + end-to-end 스모크 (POST backtest → polling → result) | tester | TODO | HIGH | TASK-118, TASK-119 | 2026-04-15 | 2026-04-15 |
| TASK-123 | README/운영 문서 갱신 — V1 웹 언급 제거, V2 API 기동법(`ctl start stock-backtest-api`), 엔드포인트 요약, 에러 trace_id 활용법, golden 테스트 갱신 절차 | coder | TODO | MEDIUM | TASK-117, TASK-121 | 2026-04-15 | 2026-04-15 |

