# Task Board

V3 Phase 1 MVP 범위. 모든 태스크는 `signal/stock-backtest/architecture.md` V3 섹션 (L484~) 과 `projects/stock-backtest/CLAUDE.md` (Quant Lab 5대 원칙 + UI/UX 6대 원칙) 을 근거로 한다.

## Phase 1 MVP

### 인프라 / 스캐폴드

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-001 | 프로젝트 스캐폴드 (backend/frontend 디렉토리, requirements.txt, package.json, .env.example, README, Docker Compose Postgres+TimescaleDB). architecture.md V3 § "Quant Lab 디렉토리 구조" 준수. **완료 검증**: `pip install -r backend/requirements.txt` 성공 + `python -c 'import app'` (backend/app 패키지) 성공 + `cd frontend && npm install` 성공 + `npm run build` 성공. 4개 모두 통과해야 DONE. | coder | agent | DONE | HIGH | - | 2026-04-29T01:50 | 2026-04-29T07:55 |
| TASK-002 | SQLAlchemy + Alembic 초기 설정. DB 연결은 `.env` 주입. 의존성 설치 및 import 검증 (alembic init / python -m app 실행 점검). | coder | agent | DONE | HIGH | TASK-001 | 2026-04-29T01:50 | 2026-04-29T08:05 |
| TASK-003 | 자산 카탈로그 시드 데이터 (KR/US/CRYPTO 50~100개 ticker JSON 또는 SQL). 한국 KOSPI/KODEX 주요 ETF, US SPY/QQQ/TLT/GLD/DBC 등 핵심 ETF, BTC/ETH 등. asset_type/currency/name 컬럼 모두 채움. | coder | agent | DONE | HIGH | TASK-010 | 2026-04-29T01:50 | 2026-04-29T08:50 |

### DB 스키마

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-010 | 마스터 테이블 alembic 마이그레이션: assets (V3 자산 도메인 풍부 컬럼 - asset_id/symbol/market/asset_type/currency/name/meta JSONB/active/start_date/last_ingested_at, UNIQUE(symbol,market)), ingestion_log. **market_events 는 Phase 2 로 이월 (architecture.md L732)** — Phase 1 에서는 생성하지 않음. | coder | agent | DONE | HIGH | TASK-002 | 2026-04-29T01:50 | 2026-04-29T08:25 |
| TASK-011 | 시계열 테이블 마이그레이션: ohlcv (hypertable, PRIMARY KEY(asset_id, time)), fx_rates (PRIMARY KEY(base_ccy, quote_ccy, time)), corporate_actions. TimescaleDB hypertable 변환 포함. | coder | agent | DONE | HIGH | TASK-010 | 2026-04-29T01:50 | 2026-04-29T08:50 |
| TASK-012 | 백테스트 테이블 마이그레이션: backtest_runs (run_hash UNIQUE, status, progress, error_json, code_commit_hash, data_hash, base_currency 등 V2 살림 항목 포함), backtest_equity (hypertable), backtest_trades (side ∈ BUY/SELL only), backtest_metrics. | coder | agent | DONE | HIGH | TASK-010 | 2026-04-29T01:50 | 2026-04-29T09:15 |

### 데이터 수집

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-020 | DataSource 추상 인터페이스 (base.py) + yfinance 어댑터 (US 주식/ETF, Crypto, FX). rate limit 1~2 req/sec 준수. | coder | agent | DONE | HIGH | TASK-011 | 2026-04-29T01:50 | 2026-04-29T09:15 |
| TASK-021 | pykrx 어댑터 (KR 주식/ETF). 세션당 100ms sleep. | coder | agent | DONE | HIGH | TASK-020 | 2026-04-29T01:50 | 2026-04-29T09:35 |
| TASK-022 | 증분 파이프라인: assets active 자산별 MAX(time) 조회 → 다음 날부터 백필. 갭 자동 감지(거래일 캘린더 vs ohlcv 커버리지 비교) + 멱등 UPSERT (ON CONFLICT(asset_id,time) DO UPDATE) + 비거래일 다층 방어 4단계 중 **수집/캘린더 레이어** (close=0/null/NaN 거부 + 캘린더 외 날짜 수집 제외). 조회 레이어는 TASK-030, 엔진 레이어는 TASK-041/043 에서. 자산 단위 3회 재시도 (1s→2s→4s). 실패 시 ingestion_log FAILED 기록. | coder | agent | DONE | HIGH | TASK-021 | 2026-04-29T01:50 | 2026-04-29T09:55 |
| TASK-023 | APScheduler cron 잡: KR 18:00 KST / US 07:00 KST(다음날) / Crypto 09:00 KST. 시장별 독립 처리. | coder | agent | DONE | MEDIUM | TASK-022 | 2026-04-29T01:50 | 2026-04-29T10:45 |

### 자산 도메인

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-030 | Asset / Universe 도메인 모델 + Repository (자산 카탈로그 조회/검색, market 필터, 한글명 prefix). **비거래일 방어 — 조회 레이어** 포함: 사용자/전략이 비거래일을 넘기면 예외 또는 직전 거래일로 자동 정렬 (옵션). | coder | agent | DONE | HIGH | TASK-010 | 2026-04-29T01:50 | 2026-04-29T08:50 |
| TASK-031 | 자산 자유 추가 워크플로우. **레이어 분리**: ① domain 서비스 (`backend/app/domain/asset/registration.py`) 가 비즈니스 로직 담당, data 어댑터 (TASK-020/021) 를 의존성 주입으로 호출 (직접 import 금지) ② 즉시 검증 (yfinance/pykrx ticker 존재 + 최소 1년치 데이터 유무, 3초 이내) ③ 백필 큐잉은 scheduler 모듈 (`backend/app/scheduler/backfill_queue.py`) 에 위임 ④ 부분 백필 중 사용 가능. 검증 실패 시 한국어 에러 메시지 (UI/UX 원칙 2). | coder | agent | DONE | HIGH | TASK-030, TASK-022 | 2026-04-29T01:50 | 2026-04-29T10:20 |
| TASK-032 | universe 시작일 교집합 자동 산출. 사용자 명시 기간이 교집합 벗어나면 조정 결과를 응답에 포함하여 UI 통지 가능하게 함. | coder | agent | DONE | HIGH | TASK-030 | 2026-04-29T01:50 | 2026-04-29T09:15 |

### 백테스트 엔진 코어

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-040 | **파일: `backend/app/domain/portfolio.py`** — Portfolio 클래스 + cash_by_ccy[ccy] 잔고 모델 + 환전 엔진. 환전 정책: 단계 분리(C) + 같은 native currency 내 잔고 우선(B). fx_spread_bps 20bp 차감. FX 는 trade 미기록, 잔고 이동만. (architecture.md V3 § "백엔드 모듈 분할") | coder | agent | DONE | HIGH | TASK-012 | 2026-04-29T01:50 | 2026-04-29T09:35 |
| TASK-041 | **파일: `backend/app/domain/trade.py`** — 거래 실행 엔진: long-only, 음수 잔고 금지, 1주 단위 정수, 부족 시 가능한 만큼만 체결, 잔여 cash 는 base_currency 잔고 누적. 수수료 (KR 0.015% / US 0.005% / Crypto 0.1%) + 슬리피지 0.1% 시장별 자동 적용. **비거래일 방어 — 엔진 레이어**: 데이터 로드 직후 universe 전체에 is_trading_day 검증, 결측 시 명시적 에러 (silent 0 금지). Portfolio 를 import (TASK-040). | coder | agent | DONE | HIGH | TASK-040 | 2026-04-29T01:50 | 2026-04-29T09:55 |
| TASK-042 | **파일: `backend/app/domain/calendar.py`** — 캘린더 정렬: base_currency 의 시장 캘린더 (KRW→XKRX, USD→NYSE) 기준. 비base 시장 자산은 직전 자기 시장 거래일 종가 forward-fill. 암호화폐는 base 캘린더 D 일의 UTC 00:00 종가. exchange_calendars 사용. (architecture.md V3 § "백엔드 모듈 분할") | coder | agent | DONE | HIGH | TASK-040 | 2026-04-29T01:50 | 2026-04-29T09:55 |
| TASK-043 | **파일: `backend/app/domain/strategy.py` + `backend/app/domain/engine.py`** — Strategy 인터페이스: allocator + signal_filters[] (AND) + rebalance_schedule (daily/weekly/monthly/quarterly/yearly/signal_event) 3요소 조합. 시그널/체결 모델 A 강제 - generate_signal(prices_until_D) 함수에 D+1 일 데이터를 절대 노출하지 않는 구조적 차단 (시그널 함수 시점에 prices.tail(D) 슬라이싱). engine.py 는 백테스트 메인 루프만 (시그널 호출 → 리밸런싱 → 거래 실행 호출 → equity 기록 → 진행률/취소 체크). 비거래일 방어 - 엔진 레이어 보강. | coder | agent | DONE | HIGH | TASK-042 | 2026-04-29T01:50 | 2026-04-29T10:20 |
| TASK-044 | **파일: `backend/app/domain/dividend.py` + `backend/app/domain/metrics.py`** — 배당 처리 (yfinance dividends → corporate_actions 기록 → cash_by_ccy 입금 → 다음 리밸런싱 편입) + 메트릭 계산 (CAGR/MDD/Sharpe/Sortino/Calmar/승률/연·월 수익률 테이블). | coder | agent | DONE | HIGH | TASK-041 | 2026-04-29T01:50 | 2026-04-29T10:20 |
| TASK-045 | **파일: `backend/app/domain/tax.py`** — Tax plugin 인터페이스 (`apply(realized_trades, dividends, year) -> tax_amount`) + NoTaxPlugin 빈 구현 (MVP 디폴트 OFF). 엔진은 plugin 호출 시점/방법만 명확히 정의 (TASK-043 engine.py 에서 import). | coder | agent | DONE | MEDIUM | TASK-044 | 2026-04-29T01:50 | 2026-04-29T10:45 |

### 전략

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-050 | Allocator base 클래스 (params_schema pydantic) + FixedWeight 구현. 비중 합 검증, _CASH_ 슬리브 허용. | coder | agent | DONE | HIGH | TASK-043 | 2026-04-29T01:50 | 2026-04-29T10:45 |
| TASK-051 | AllWeather Allocator 구현. 표준 비중 (주식 30 / 장기채 40 / 중기채 15 / 금 7.5 / 원자재 7.5) 또는 사용자 조정 가능. universe 내 해당 자산 부재 시 명시적 에러. | coder | agent | DONE | HIGH | TASK-050 | 2026-04-29T01:50 | 2026-04-29T11:00 |
| TASK-052 | EqualWeight Allocator 구현. universe 모든 자산에 1/N 비중 자동 배분. | coder | agent | DONE | HIGH | TASK-050 | 2026-04-29T01:50 | 2026-04-29T11:00 |
| TASK-053 | SignalFilter base 클래스 + MovingAverage 필터. 자산별 가격 > MA(window) 면 PASS. 멀티 자산 universe 에서 자산별 독립 적용. | coder | agent | DONE | HIGH | TASK-043 | 2026-04-29T01:50 | 2026-04-29T10:45 |
| TASK-054 | Momentum 필터. lookback 기간 수익률 > 0 (또는 사용자 임계값) 면 PASS. | coder | agent | DONE | HIGH | TASK-053 | 2026-04-29T01:50 | 2026-04-29T11:00 |

### API

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-060 | docs/openapi.yaml 초안 작성 + FastAPI 스캐폴드 + 전역 예외 핸들러 (모든 4xx/5xx 응답 에러 계약: stage/type/message/request_ctx/trace_id). 서버 로그 trace_id stage ctx 접두사. GET /api/health 포함. **`backend/app/schemas/` 공통 base 스키마**: ErrorResponse, PaginatedResponse, TimestampedModel 등 cross-endpoint base. | coder | agent | DONE | HIGH | TASK-001 | 2026-04-29T01:50 | 2026-04-29T08:05 |
| TASK-061 | 자산 API: GET /api/assets (q/market/asset_type 필터), POST /api/assets (자유 추가 - TASK-031 비동기 백필 트리거), GET /api/assets/{id}, GET /api/assets/{id}/ohlcv (start/end). GET /api/strategies (전략 목록 + pydantic JSON Schema). **스키마 모듈**: `backend/app/schemas/asset.py` (AssetCreate/AssetRead/AssetSearchQuery/OhlcvPoint), `backend/app/schemas/strategy.py` (StrategyDescriptor with JSON Schema). | coder | agent | DONE | HIGH | TASK-031, TASK-060 | 2026-04-29T01:50 | 2026-04-29T11:00 |
| TASK-062 | 백테스트 job API: POST /api/backtests (status=pending row 삽입 후 즉시 반환), GET /api/backtests/{run_id} (status/progress 0~1), GET /api/backtests/{run_id}/result (equity/trades/metrics), DELETE /api/backtests/{run_id} (running 취소 / 완료 삭제), GET /api/backtests (이력). FastAPI BackgroundTasks 또는 asyncio queue. 진행률은 리밸런싱 date 진행 기준. 취소는 DB 플래그 폴링. **스키마 모듈**: `backend/app/schemas/backtest.py` (BacktestCreate/BacktestStatus/BacktestResult/EquityPoint/TradeRecord/MetricsPayload). | coder | agent | DONE | HIGH | TASK-044, TASK-050, TASK-051, TASK-052, TASK-053, TASK-054, TASK-060 | 2026-04-29T01:50 | 2026-04-29T11:20 |

### 테스트

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-080 | 백테스트 엔진 골든 스냅샷 테스트: 전략 3종(FixedWeight/AllWeather/EqualWeight) × 시나리오 3개 (단일통화 KRW universe / 멀티통화 KRW base 미국+한국 / 암호화폐 포함 멀티 마켓) = 9 케이스. tests/golden/<scenario>.json 스냅샷. 회귀 시 pytest diff. | tester | agent | DONE | HIGH | TASK-062 | 2026-04-29T01:50 | 2026-04-29T11:55 |
| TASK-081 | look-ahead 회귀 테스트: 모든 전략에 대해 generate_signal 함수에 D+1 일 데이터를 추가로 노출했을 때 시그널 결과가 변하지 않음을 검증 (구조적 차단 검증). + 비거래일 방어 4단계 (수집/캘린더/조회/엔진) + cash_by_ccy 환전 단위 (단계 분리 + native 우선 + fx_spread 적용) 테스트. | tester | agent | DONE | HIGH | TASK-080 | 2026-04-29T01:50 | 2026-04-29T11:42 |
| TASK-082 | API 계약 테스트 (schemathesis fuzz, OpenAPI spec 대비) + 비동기 job 통합 스모크 (POST /backtests → 폴링 → /result end-to-end 1 케이스). 동시 job 2개 독립성 + 취소 시 DB 트랜잭션 정리 + 워커 크래시 후 pending/running 복구 정책 검증. | tester | agent | DONE | HIGH | TASK-062 | 2026-04-29T01:50 | 2026-04-29T11:55 |

### 프런트 (Next.js)

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-090 | Next.js 14+ App Router 스캐폴드 + shadcn/ui 설치 + Zod 런타임 검증 + 한국어 i18n 기본 + API 클라이언트 (Zod schema 로 응답 검증). UI/UX 6대 원칙 강제 시작점. | coder | agent | DONE | HIGH | TASK-061 | 2026-04-29T01:50 | 2026-04-29T11:20 |
| TASK-091 | 자산 카탈로그 화면: 시장 필터 (한국/미국/암호화폐) + 한글명/심볼 검색 + "자산 추가" 다이얼로그 (ticker 입력 → 즉시 검증 → 등록 성공 시 백필 진행률 폴링 표시). UI/UX 원칙 1·2·3 적용. | coder | agent | DONE | HIGH | TASK-090 | 2026-04-29T01:50 | 2026-04-29T11:55 |
| TASK-092 | 백테스트 생성 화면: 전략 선택 (드롭다운) → 파라미터 폼 (pydantic schema → 자동 폼 생성, JSON 노출 없음) → universe 선택 (자산 카탈로그 검색 위젯, 다중 선택) → 기간 (시작/종료) → base_currency (드롭다운, 디폴트 없음) → 실행 버튼. UI/UX 원칙 1·5 강제. | coder | agent | DONE | HIGH | TASK-091 | 2026-04-29T01:50 | 2026-04-29T11:42 |
| TASK-093 | 백테스트 결과 화면: equity curve (선형, log 토글) + drawdown 차트 + 지표 테이블 (CAGR/MDD/Sharpe/Sortino/Calmar/승률) + 연·월 수익률 히트맵 + 거래 내역 테이블 (페이지네이션, 통화 그룹). UI/UX 원칙 4 적용. | coder | agent | DONE | HIGH | TASK-092 | 2026-04-29T01:50 | 2026-04-29T11:55 |
| TASK-094 | 진행률 폴링 + 데이터 갭 통지 토스트 ("BTC 시작일 때문에 기간 조정됨" 등) + 한국어 에러 메시지 액션 가이드 ("티커 'XYZ' 를 찾을 수 없습니다 ..." 형태) + 백테스트 취소 버튼. **화면 귀속**: TASK-092 (백테스트 생성) 화면 내에서 폼 제출 후 진행률 표시 (in-place 패널), 완료 시 TASK-093 결과 화면으로 라우팅. **별도 진행 화면 만들지 않음 (UI/UX 원칙 6 점진적 노출 — 화면 3개 한도 유지)**. UI/UX 원칙 2·3 강제. | coder | agent | DONE | MEDIUM | TASK-092 | 2026-04-29T01:50 | 2026-04-29T11:55 |

### 통합

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-100 | end-to-end 통합 검증 (자산 추가 → universe 구성 → 백테스트 생성 → 진행률 폴링 → 결과 표시 → 취소/재실행). README + 실행 가이드 (Docker Compose up → migrate → seed → backend/frontend 기동) 작성. | coder | agent | DONE | MEDIUM | TASK-082, TASK-094 | 2026-04-29T01:50 | 2026-04-29T12:10 |
