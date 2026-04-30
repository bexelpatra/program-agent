# Architecture

## 개요

**프로젝트 목적**: 글로벌 자산(지수/ETF/채권/원자재/암호화폐)을 대상으로 시계열 데이터 파이프라인을 구축하고, 계절성 분석·정적 자산배분·동적 자산배분·신규 전략 실험을 수행하는 백테스팅 플랫폼. 결과는 Dash 웹 앱으로 시각화·반복 실험.

**기술 스택**:
- 언어: Python 3.11+
- DB: PostgreSQL + TimescaleDB (Docker Compose)
- 데이터 소스: `yfinance` (US/원자재/암호화폐/FX), `pykrx` (KR)
- 거래일 캘린더: `exchange_calendars`
- 수치: `pandas`, `numpy`
- 웹: `dash` + `plotly`
- 설정: `.env` + `config/defaults.yaml`

**주요 제약사항**:
- 단일 사용자, 로컬 실행 (인증 없음; `user_id` 컬럼만 미리 확보하여 추후 멀티유저 이관 대비)
- 일봉 데이터만 (주/월봉은 런타임 resample)
- 개별 주식 제외 (ETF/지수 중심)
- 장기 확장 가능성: ClickHouse 이관, Supabase/AWS 배포, 분봉 확장, 개별주식 추가

---

## 구조

### 디렉토리

```
projects/stock-backtest/
├── src/stock_backtest/
│   ├── data/
│   │   ├── models.py           # SQLAlchemy ORM
│   │   ├── db.py               # 연결, 세션 관리
│   │   └── repository.py       # 쿼리 레이어 (자산 타입 추상화)
│   ├── ingestion/
│   │   ├── base.py             # DataSource 추상 인터페이스
│   │   ├── yfinance_source.py
│   │   ├── pykrx_source.py
│   │   ├── pipeline.py         # 증분 수집, 갭 감지, 재시도
│   │   └── cli.py              # `python -m stock_backtest.ingestion.cli`
│   ├── analysis/
│   │   ├── seasonality.py      # 월/요일/월말/할로윈/Sell-in-May
│   │   └── political_cycle.py  # 미국 대선/중간선거/FOMC/실적시즌, 한국 대선/총선
│   ├── strategies/
│   │   ├── base.py             # Strategy 추상 + params_schema
│   │   ├── static/
│   │   │   ├── fixed_weight.py # 60/40, 올웨더 등 파라미터화
│   │   │   └── permanent.py
│   │   ├── dynamic/
│   │   │   ├── momentum.py
│   │   │   ├── dual_momentum.py
│   │   │   ├── vaa.py
│   │   │   └── risk_parity.py
│   │   └── registry.py         # 파일 자동 스캔 + 등록
│   ├── backtest/
│   │   ├── engine.py           # 벡터화 백테스트
│   │   ├── portfolio.py        # 포지션, 현금, 환전
│   │   ├── calendar.py         # KR/US/Crypto 거래일 + 공통 기간 계산
│   │   ├── fx.py               # 통화 환산
│   │   └── cache.py            # (run 해시 기반 재사용)
│   ├── metrics/
│   │   └── performance.py      # CAGR, Vol, Sharpe, Sortino, MDD, Calmar, Turnover
│   └── web/
│       ├── app.py              # Dash entry
│       ├── pages/
│       │   ├── backtest.py     # MVP 1순위
│       │   ├── seasonality.py  # MVP 2순위
│       │   ├── data_explorer.py
│       │   └── history.py
│       └── components/
├── tests/
├── config/
│   └── defaults.yaml           # 수수료/슬리피지/환전비용/리밸런싱/캘린더/base_ccy
├── docker-compose.yml          # Postgres + TimescaleDB
├── migrations/                 # Alembic 또는 raw SQL
├── requirements.txt
├── .env.example
└── README.md
```

---

## 설계 결정

### 1. 데이터 저장 - PostgreSQL + TimescaleDB

- **결정**: `ohlcv`, `backtest_equity`를 hypertable로. `fx_rates`, `assets`, `market_events`, `corporate_actions`, `ingestion_log`, `backtest_runs`, `backtest_trades`, `backtest_metrics`는 일반 테이블.
- **이유**: 시계열 대량 데이터 압축·파티셔닝 이점. 일반 Postgres 쿼리/인덱스와 호환.
- **대안**: SQLite+Parquet(단순하나 멀티프로세스 취약), ClickHouse(과한 초기 비용). 추후 데이터량 폭증 시 ClickHouse 재검토.

### 2. 자산 타입 추상화

- **결정**: `assets.asset_type ∈ {EQUITY_INDEX, ETF, BOND, COMMODITY, CRYPTO}` + `assets.market` + `assets.currency`. FX는 별도 `fx_rates` 테이블.
- **이유**: 투자 자산과 환율 레퍼런스 분리. 자산 확장(섹터 ETF, 타국 지수) 시 스키마 변경 불필요.
- **대안**: 자산별 테이블 분리 — 쿼리 복잡도 증가로 기각.

### 3. 기준 통화 (base_currency)

- **결정**: 백테스트 런 파라미터로 `base_currency` 지정 (디폴트 USD). 체결/보유는 자산 native currency로 기록, 일별 포트폴리오 평가(equity)는 `fx_rates`로 환산해 base_currency로 저장.
- **이유**: 다중 통화 자산 합산은 단일 기준 통화에서만 의미 있음. 리밸런싱 비중 판단도 base_currency 필요.
- **대안**: 자산별 native 저장 후 매 조회 시 환산 — 리밸런싱 로직 복잡화로 기각.

### 4. 포트폴리오 환전 비용

- **결정**: 크로스-커런시 리밸런싱 시 해당일 fx_rate로 환전하며 `defaults.yaml`의 `fx_spread_bps`(기본 20bp) 차감.
- **이유**: 실제 환전 스프레드 반영. 현실적인 성과 추정.

### 5. 암호화폐 전용 모드

- **결정**: 백테스트 런은 `market_mode ∈ {STOCK, CRYPTO, MIXED}`. 암호화폐 일봉 기준시각은 **UTC 00:00 확정**.
  - STOCK: 주식 거래일 캘린더
  - CRYPTO: 365일 연속 캘린더 (UTC 00:00 종가)
  - MIXED: 주식 거래일 기준으로 리샘플링, 크립토는 해당 거래일의 UTC 00:00 종가를 forward-fill
- **이유**: 24/7 시장과 주식장 시간축 불일치 해결.
- **대안**: 항상 교집합 일자만 사용 — 주말 수익률 손실로 기각.

### 6. 공통 기간 자동 계산

- **결정**: 백테스트 런 시 universe 내 모든 자산의 `(start_date, end_date)` 교집합을 자동 산출. 명시적 기간을 넘어서면 경고.
- **이유**: 생존 편향 없이 일관된 백테스트 구간 확보. 암호화폐 등 신규 자산 포함 시 자동으로 짧아짐.

### 7. 백테스트 엔진 - 벡터화 직접 구현

- **결정**: pandas/numpy 기반 벡터화. 이벤트 루프 없음. 리밸런싱 시점에만 목표 비중 vs 현재 비중 차이를 계산해 거래 생성.
- **이유**: 장기 자산배분·계절성 분석에 충분. 개발 속도·디버깅·분석 유연성 최고.
- **대안**: vectorbt/backtrader — 추후 이벤트 기반 전략이 생기면 혼합 도입. Strategy 인터페이스는 엔진 독립적으로 설계해 교체 비용 최소화.
- **디폴트값 (config/defaults.yaml)**:
  - commission_buy_bps: 15, commission_sell_bps: 15 (market별 오버라이드 지원)
  - slippage_bps: 5
  - fx_spread_bps: 20
  - rebalance: 'ME' (월말)
  - base_currency: 'USD'

### 8. 전략 등록 시스템

- **결정**: `Strategy` 추상 베이스 + `params_schema` (pydantic 기반). `src/strategies/` 하위 파일을 `registry.py`가 자동 스캔해 등록. 웹은 `params_schema`로 자동 폼 생성.
- **이유**: 파일 드롭으로 전략 추가 → 즉시 UI 노출. Claude 경유 등록/직접 코딩 모두 자연스러움.
- **보안**: 웹에서 임의 Python 코드 업로드/실행 기능은 **구현하지 않는다**. 임의 코드 실행 위험.

### 9. 데이터 수집 - DB 기반 증분

- **결정**: Cron 잡은 `assets` 테이블의 active 자산을 매 실행마다 조회. 자산별 `MAX(time)` 조회 후 그 다음 날짜부터 현재까지 백필.
- **장점**: 신규 자산 등록(DB row 추가) 시 자동으로 다음 실행에서 백필.
- **Cron 구성**:
  - KR: 매일 18:00 KST
  - US: 매일 07:00 KST (다음날)
  - Crypto: 매일 09:00 KST
- **실패 처리**:
  - 자산 단위 3회 재시도 (지수백오프 1s→2s→4s)
  - 실패 자산은 `ingestion_log`에 FAILED 기록, 잡은 계속 진행
  - 매 실행 시작 시 `assets` × `거래일 캘린더` vs `ohlcv` 실제 커버리지 비교하여 **갭 자동 감지·재수집**
- **Rate limit**: yfinance 초당 1~2 req 이하, pykrx는 세션당 100ms sleep. 시장별로 독립 처리.
- **멱등성**: ohlcv UPSERT (`ON CONFLICT (asset_id, time) DO UPDATE`).

### 10. 재현성 및 과거 데이터 수정

- **결정**: `backtest_runs`에 `code_commit_hash`, `data_hash`(관련 자산의 max(updated_at)+row count 해시), `created_at` 저장. 같은 run 재실행 시 현재 data_hash와 다르면 STALE 표시.
- **배경 - 과거 가격이 바뀌는 이유**:
  1. 분할/배당 이벤트 발생 시 yfinance는 **과거 adj_close 전체를 재계산**하여 제공 → UPSERT로 반영 필수
  2. 소스 측 지연/정정 데이터
  3. 신규 배당 선언으로 배당락일 이전 adj_close 재조정
- **정책**: UPSERT가 정상 동작. 과거 수정은 수용하되 백테스트 재현성은 `data_hash`+STALE 플래그로 관리. 완전 스냅샷 저장은 비용 대비 효용 낮아 생략.

### 11. 캐싱

- **결정**: (strategy_name, params, universe, period, base_currency) 해시를 `backtest_runs.run_hash`로 저장. 같은 해시로 재요청 시 기존 run 반환.
- **이유**: 동일 조건 중복 실행 방지, UI 반응성.

### 12. 계절성 이벤트 카테고리

- 월/요일/월말-월초 효과
- Sell-in-May / Halloween
- **미국 정치 사이클**: 대선(4년), 중간선거(2년), 대통령 임기 1~4년차
- **미국 통화정책**: FOMC 주간
- **실적 시즌**: 1/4/7/10월
- **한국 정치**: 대선(5년)·총선(4년) — 데이터 포인트 적어 통계력 약함을 UI에 경고 표시
- `market_events(event_id, country, type, event_date, meta JSONB)` 테이블로 관리

### 13. 비거래일 방어

- **결정**: 다층 방어.
  1. **수집 레이어**: 소스에서 받은 레코드에 close=0/null/NaN이면 insert 거부 + `ingestion_log`에 REJECTED 기록
  2. **캘린더 레이어**: 거래일 캘린더(`exchange_calendars`)에 없는 날짜는 애초에 수집 대상에서 제외
  3. **조회 레이어 (repository)**: 사용자/전략이 비거래일을 넘기면 예외 발생 또는 직전 거래일로 자동 정렬 (옵션)
  4. **백테스트 엔진**: 데이터 로드 직후 universe 전체에 대해 `is_trading_day(market, date)` 검증, 비거래일·결측 구간은 명시적 에러로 중단 (silent 0 계산 금지)
- **이유**: 비거래일을 0으로 취급해 수익률이 거짓으로 계산되는 사고 방지.

### 14. 한국 거주자 세금 모듈 (KR-resident tax)

- **결정**: 한국 거주자 기준 세금을 `Tax` 모듈로 분리. 기본 활성화(`enabled: true`) 디폴트, 전략별 오버라이드 가능.
- **적용 규칙**:
  - **미국/해외 주식형 자산 양도소득세**: 실현 이익에 대해 **22%** (연 **250만원** 기본공제). 달러 실현익을 환전 시점 기준 KRW 환산하여 집계.
  - **배당소득세**: 해외 배당 **15.4%** 원천징수로 단순화 (외국납부세액공제/금융소득종합과세 고려 생략).
  - **국내 ETF 매매차익**: 주식형 ETF는 비과세 / 채권·혼합·해외형은 배당소득세 15.4% → `assets.meta`에 `kr_tax_class` 태그로 관리.
  - **암호화폐**: 2026년 기준 양도세 22% (250만원 공제) — 설정으로 on/off (법 시행 유예 변동 가능).
- **적용 시점**: 리밸런싱 시 매도 체결에서 실현 이익 산출 → 해당 회계연도 누적 이익에서 공제액 초과분에 세율 적용 → 현금 잔고 차감. 연말(12/31 UTC) 누적 초기화.
- **왜 중요한가**: 한국 거주자가 미국 자산 위주 포트폴리오 실행 시 세후 수익률이 세전 대비 현저히 낮아짐. 정적/동적 자산배분 비교에서 리밸런싱 빈도에 따른 세금 부담이 의사결정에 큰 영향.
- **구조**: `src/stock_backtest/backtest/tax.py` 모듈화. 추후 미국 거주자·홍콩 거주자 등 다른 세제 프로파일 추가 용이.
- **디폴트 (defaults.yaml)**:
  ```yaml
  tax:
    enabled: true
    profile: 'kr_resident'
    kr_resident:
      overseas_capital_gains_rate: 0.22
      overseas_annual_deduction_krw: 2_500_000
      overseas_dividend_rate: 0.154
      crypto_capital_gains_rate: 0.22
      crypto_annual_deduction_krw: 2_500_000
      crypto_enabled: true
  ```

### 15. 재현/테스트

- 모든 DB 연결은 `.env`로 주입. 테스트는 Docker Compose로 별도 테스트 DB 기동.
- 백테스트 결과에 `code_commit_hash` + `data_hash`.

---

## DB 스키마 (요약)

```sql
-- 마스터
assets(asset_id PK, symbol UNIQUE(symbol,market), market, asset_type, name,
       currency, active, start_date, last_ingested_at, meta JSONB)

-- 시계열 (hypertable)
ohlcv(time, asset_id FK, open, high, low, close, adj_close, volume,
      PRIMARY KEY(asset_id, time))
corporate_actions(time, asset_id, type, value, meta JSONB)

-- FX
fx_rates(time, base_ccy, quote_ccy, rate, PRIMARY KEY(base_ccy, quote_ccy, time))

-- 이벤트
market_events(event_id PK, country, type, event_date, meta JSONB)

-- 수집 로그
ingestion_log(log_id PK, asset_id FK, requested_start, requested_end,
              status, rows_inserted, error_message, attempted_at)

-- 백테스트
backtest_runs(run_id PK, run_hash UNIQUE, user_id DEFAULT 'local',
              strategy_name, params JSONB, universe JSONB,
              period_start, period_end, base_currency, market_mode,
              code_commit_hash, data_hash, created_at)
backtest_equity(run_id FK, time, equity, cash, drawdown,
                PRIMARY KEY(run_id, time))  -- hypertable
backtest_trades(run_id FK, time, asset_id FK, side, qty, price,
                commission, currency)
backtest_metrics(run_id FK, metric_name, value)
```

---

## 웹 MVP 순서

1. **(c) 전략 백테스트 페이지**: 전략 선택 → 파라미터 폼 → universe 선택 → 기간 → 실행 → 결과(equity curve, drawdown, 주요 지표 테이블)
2. **(b) 계절성 분석 페이지**: 자산 선택 → 이벤트 카테고리 선택 → 히트맵/박스플롯/통계검정
3. **(a) 데이터 탐색**: 자산 가격·수익률·상관관계 조회
4. **(d) 이력 비교**: 여러 run 겹쳐 그리기

---

## 현재 상태

- 설계 완료. 태스크 분해 진행 예정.
- 아직 구현 착수 전.

---

## 전략 DSL 및 현금 1급 처리 (2026-04-14 확정)

### 원칙
1. **자산 입력 필드는 반드시 자산 위젯으로 렌더**. 원시 `str`/`list[str]`/`dict[str,float]` 텍스트/JSON 입력 UI 영구 금지. 위젯: `asset_symbol`, `asset_symbol_list`, `asset_weight_map`.
2. **현금(`_CASH_`)은 1급 포지션**. 합성 자산/OHLCV 없이 엔진의 `cash_by_ccy[base_currency]` 잔고로 직접 표현. 매수/매도 trade 기록 없음.
3. **FX 변환은 trade 레코드로 취급하지 않는다** *(2026-04-22 개정, V2 단순화)*. 자산 매매만 `backtest_trades` 에 기록. 통화 이동은 엔진 내부 잔고 변화(스프레드 차감 포함)로만 처리. → 상세는 V2 §"V2 FX 처리 모델" 참조.

### 롱 전용 전략 DSL
단일 자산 스위칭 전략(MA Crossover/Simple/Multi 등):
```python
target_symbol: str                                  # 신호 ON 시 롱 대상
exit_action:   Literal["cash", "rotate"] = "cash"   # 신호 OFF 시 동작
rotate_symbol: str | None = None                    # exit_action="rotate"일 때만 필수
```
- `exit_action="cash"` → `generate_weights` 가 `_CASH_` 컬럼에 100% 배분
- `exit_action="rotate"` → `rotate_symbol` 에 100% 배분

### 다중 자산 전략의 현금 슬리브
- `FixedWeight.weights` 에 `"_CASH_"` 키 허용: 예 `{"SPY": 0.6, "AGG": 0.3, "_CASH_": 0.1}`
- `Momentum/DualMomentum/VAA/RiskParity` 의 `universe`/`offensive_assets`/`defensive_assets` 에 `"_CASH_"` 포함 허용. `_CASH_` 의 수익률은 base_currency 기준 0 (가격 1.0 상수).

### 엔진 `_CASH_` 처리 규약
- `generate_weights` 가 반환하는 DataFrame 에 `_CASH_` 컬럼이 있으면:
  - prices DataFrame 에서는 `_CASH_` 를 조회하지 않음 (`required_universe()` 는 포함 허용, 엔진이 필터링)
  - 목표 비중 = `target_cash_value = equity * weight_cash` (base_currency)
  - 리밸런싱 후 `cash_by_ccy[base_currency]` 가 `target_cash_value` 에 근접하도록 조정 (실제로는 타 자산 매수/매도 후 남은 잔고로 자연 충족)
- trade 레코드는 실제 자산 매매만 기록. `_CASH_` 단독 이동은 기록하지 않음 (잔고 변화로 추적).

### FX TradeRecord 스키마 확장 *(2026-04-22 폐기)*

~~V1 DSL 확정 시점(2026-04-14)에는 `backtest_trades.side` CHECK 에 `"FX"` 추가, `currency_from/currency_to/fx_rate/spread_bps` 컬럼 추가, `asset_id` nullable 로 설계했음.~~
**V2 에서 폐기.** 일반 사용자 관점에서 FX trade 노출은 노이즈이며, 세금 계산도 매도 시점 환율로 충분히 단순화 가능. V2 §"V2 FX 처리 모델" 참조. TASK-052(이미 완료)는 되돌림 migration 필요.

### 마이그레이션 방침
- 기존 `risky_symbol`/`safe_symbol` DSL **제거**. 병행 운영 안 함. 기존 백테스트 이력은 DB 에 보존되나 신규 실행은 새 DSL로만.

---

## 리스크 / 향후 재검토

- yfinance/pykrx 비공식성 → DataSource 추상화로 교체 가능하게 설계
- 데이터량 폭증 시 ClickHouse 이관
- 분봉 확장 시 엔진 재설계 필요
- 개별 주식 편입 시 생존 편향 처리 (point-in-time 구성 이력) 필요

---

# V2 Reset (2026-04-15~)

V1의 Dash 웹 레이어와 과잉 구현된 전략들은 검증이 누락된 채 복잡도만 커져 사용성이 떨어진다. 아래 V2 섹션이 이후 설계의 **유일한 진실**이며, 상충 시 V2를 우선 적용한다. (V1 내용은 히스토리 보존 목적.)

## V2 목표

1. **Backend-first**: 웹 전부 제거. FastAPI HTTP 서버가 유일한 외부 인터페이스.
2. **검증된 전략 2개만**: `SimpleMovingAverage`, `FixedWeight`. 나머지 전부 삭제.
3. **확장성**: 전략 조합(AND 합성)을 인터페이스 수준에서 허용. 실제 composer 구현은 Phase 3.
4. **추적성**: 모든 에러에 stage/ctx/trace_id 를 부여해 응답과 로그에서 교차 조회 가능.
5. **비동기 실행**: 백테스트는 job 모델(POST → run_id → 폴링). 진행률/취소 가능.

## V2 전략 인터페이스 (슬림화)

전략은 순수 로직만 담당. UI 힌트(드롭다운, 라벨)는 전략 밖의 별도 레이어가 책임.

```python
class Strategy(Protocol):
    params_schema: ClassVar[type[BaseModel]]   # 입력 파라미터 pydantic
    def __init__(self, params: BaseModel): ...
    def required_universe(self) -> list[AssetRef]: ...
    def generate_signal(self, prices: pd.DataFrame) -> Signal: ...
```

- `Signal` = **자산별 타깃 비중 시계열** (index=거래일, columns=`AssetRef | Cash`). 기존 weights 와 다른 점: cash 가 타입으로 구분.
- 전략 클래스에서 웹 위젯 메타/라벨 한글화 등은 **제거**. API 레이어가 pydantic schema 를 그대로 OpenAPI로 노출.

### V2 유지 전략 목록

| name                     | params                                                                 | semantics                                                                |
|--------------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------|
| `simple_moving_average` | `target: AssetRef`, `window: int`                                      | `price_{t-1} > MA(window)_{t-1}` → 100% target, else 100% cash           |
| `fixed_weight`          | `weights: dict[AssetRef, float]`, `rebalance: "annual"\|"quarterly"\|"monthly"` | 목표 비중을 유지, 주기 도래 시 리밸런싱                        |

둘 다 cash 참조를 허용한다 (`Cash`는 `AssetRef` 의 한 종류).

## V2 Cash 타입화

V1 에서 `"_CASH_"` 문자열이 레이어마다 누락되는 문제를 구조적으로 차단한다.

```python
class Cash(NamedTuple):
    currency: str   # "USD", "KRW", ...

AssetRef = Asset | Cash   # 태그된 유니온

# Signal 의 column 타입이 AssetRef 이므로, cash 를 전략이 반환하면
# 엔진/레포/저장소는 항상 분기 처리가 강제됨 (빼먹을 수 없음).
```

- 엔진 prices 조회: `AssetRef` 가 `Cash` 면 자동 스킵 (price=1.0, 거래 없음, base_currency 환산만).
- API 응답: cash 는 `{"type":"cash","currency":"USD"}`, 자산은 `{"type":"asset","symbol":"SPY","market":"US"}`.
- DB `backtest_trades` 는 **자산 매매만 기록**. FX 관련 컬럼/CHECK 확장은 폐기(아래 §"V2 FX 처리 모델" 참조).

## V2 FX 처리 모델 (2026-04-22)

일반 사용자 관점에 맞춘 단순 모델. "자산은 market 의 native currency 로 거래, 포트폴리오 총액만 기축통화(base_currency)로 환산" 멘탈 모델.

### 원칙
1. **자산은 native currency 로만 체결·보유**. SPY=USD, KODEX200=KRW, BTC=USD 등 `assets.currency` 를 그대로 사용.
2. **현금도 currency 별로 분리 보유**: `cash_by_ccy[USD]`, `cash_by_ccy[KRW]` 등.
3. **FX 는 trade 로 기록하지 않는다**. 리밸런싱 과정에서 통화 이동이 필요하면 엔진 내부에서 `cash_by_ccy` 잔고 이동 + 스프레드 차감만 수행. `backtest_trades` 에는 **자산 매매만** 기록.
4. **equity 는 매일 base_currency 로 환산해 저장**. 각 자산 native value × 당일 `fx_rates` → base_currency 합산.
5. **세금은 매도 시점 환율로 실현익 환산**. "환전 시점 환율 추적" 로직은 제거(한국 세법 엄밀 적용은 실제 세무 신고용이며, 백테스팅 의사결정 비교에는 불필요한 정밀도).

### 엔진 동작
- 리밸런싱 시 목표 자산이 A 통화, 현재 잔고가 B 통화면: `cash_by_ccy[B]` 에서 fx_rate 로 환산해 `cash_by_ccy[A]` 로 이동하며 `fx_spread_bps` 차감. 이 이동은 DB 에 기록되지 않음. equity 저하로만 반영됨.
- `fx_spread_bps` (defaults.yaml) 유지. 기본 20bp.

### DB 스키마 (V1 원본 유지)
- `backtest_trades.side ∈ {"BUY","SELL"}` 만 유지. `"FX"` 추가 **안 함**.
- `asset_id` NOT NULL 유지. `currency_from/currency_to/fx_rate/spread_bps` 컬럼 **추가 안 함**.
- 이미 TASK-052 로 migration 이 적용되어 있다면 Phase 2 에서 되돌림 migration 추가(TASK-115 범위 또는 신규 태스크).

### 영향
- 세금 모듈(`tax.py`): 환전 시점 추적 로직 제거. `RealizedTrade.fx_rate_at_realize` 는 매도일 fx_rate 그대로 사용.
- Portfolio `_ensure_cash`: FX TradeRecord 생성 제거. 잔고 이동 함수로 단순화.
- run_store: FX trade 저장 경로 제거.

## V2 전략 조합 (Composer) — Phase 3 예정, Phase 2 는 인터페이스만

AND 기반 합성. 자산별 ON/OFF 필터가 기본형.

```python
Signal = DataFrame[date, AssetRef → weight]

def compose_and(base: Signal, *filters: SignalMask) -> Signal:
    """base 의 자산별 비중에 filter mask 를 AND 적용.
    mask 가 OFF 인 자산의 비중은 Cash(base_currency) 로 이동."""
```

예: `FixedWeight({SPY:0.6, AGG:0.4}) AND MAFilter(window=200)` →
- SPY 의 MA 가 OFF 이면 0.6 → Cash 로 이동
- AGG 의 MA 가 OFF 이면 0.4 → Cash 로 이동
- 양쪽 다 OFF 면 100% Cash

Phase 2 에서는 `Signal` 타입과 `SignalMask` 프로토콜만 정의. composer 구현·API 노출은 Phase 3.

## V2 API (FastAPI)

OpenAPI-first. `docs/openapi.yaml` 을 먼저 확정하고 라우트 구현.

### 엔드포인트 (초안)

| Method | Path                                   | 용도                                                        |
|--------|----------------------------------------|-------------------------------------------------------------|
| GET    | `/api/health`                          | liveness                                                    |
| GET    | `/api/strategies`                      | 전략 목록 + 각 전략의 JSON Schema (pydantic 변환)         |
| GET    | `/api/assets?q=&market=&asset_type=`   | 자산 검색 (symbol/name prefix, 시장/타입 필터)             |
| GET    | `/api/assets/{asset_id}`               | 단일 자산 상세                                              |
| GET    | `/api/assets/{asset_id}/ohlcv`         | 기간 OHLCV (start/end)                                      |
| POST   | `/api/backtests`                       | 백테스트 job 생성 → `{run_id, status:"pending"}` 즉시 반환 |
| GET    | `/api/backtests/{run_id}`              | job 상태 (pending/running/done/failed) + 진행률            |
| GET    | `/api/backtests/{run_id}/result`       | 완료 시 equity/trades/metrics                              |
| DELETE | `/api/backtests/{run_id}`              | 취소 (running 만) / 삭제 (완료 run)                        |
| GET    | `/api/backtests?strategy=&limit=`      | 과거 run 이력                                               |

### 비동기 job 실행 모델

- `POST /api/backtests` → DB `backtest_runs` 에 `status='pending'` row 삽입 후 즉시 반환
- 백그라운드 워커(FastAPI `BackgroundTasks` or 별도 `asyncio` task queue)가 실제 엔진 실행
- 진행률: 리밸런싱 date 진행 기준 `progress: 0.0~1.0` 을 `backtest_runs` row 에 업데이트
- 취소: DB 플래그 확인 → 엔진 루프가 주기적으로 체크 후 abort
- 실패 시 `backtest_runs.error_json` 에 stage/ctx/trace_id 기록
- **검증 포인트** (사용자 요구: "구현이 복잡한 만큼 잘 동작하게 검증"):
  - 동시 job 2개 실행 → 결과 독립성
  - 취소 시 DB 트랜잭션 정리
  - 워커 크래시 시 `pending/running` row 복구 정책

### 에러 응답 계약

모든 4xx/5xx 응답은 아래 형태로 통일:

```json
{
  "error": {
    "stage": "resolve_universe",
    "type": "ValueError",
    "message": "...",
    "request_ctx": {"strategy":"...", "universe":[...], "period":[...], "run_hash":"..."},
    "trace_id": "uuid-v4"
  }
}
```

- FastAPI 전역 예외 핸들러 1개로 구현
- 서버 로그에는 `trace_id=<uuid> stage=<X> <ctx>` 접두사로 stacktrace 출력
- 클라이언트가 `trace_id` 를 복사해 지원 요청 → 로그 grep 으로 즉시 재현 가능

## V2 테스트 전략

- **Golden snapshot**: 2 전략 × 3 시나리오 = 6 케이스. 현재 엔진 결과를 `tests/golden/<scenario>.json` 에 스냅샷. 이후 엔진/레포 로직 변경 시 `pytest` 가 diff 로 회귀를 즉시 감지. (기대값의 수학적 독립 검증은 사용자가 별도 수행.)
- **API 계약 테스트**: OpenAPI spec 대비 schemathesis 로 자동 fuzz
- **통합 스모크**: `POST /backtests` → 폴링 → `/result` 까지의 end-to-end 1 케이스

## V2 삭제 범위

- `src/stock_backtest/web/` 전체 + 관련 pycache
- service_control `stock-backtest-web` 엔트리
- 삭제 전략: `dynamic/momentum.py`, `dynamic/dual_momentum.py`, `dynamic/risk_parity.py`, `dynamic/vaa.py`, `dynamic/moving_average/{crossover,multi_crossover,seasonal}.py`, `dynamic/moving_average/_common.py`, `static/permanent.py`
- 관련 테스트: `tests/test_*web*`, 삭제 전략 단위/통합 테스트
- `data/`, `ohlcv`, `assets`, `fx_rates`, `market_events`, `backtest_runs` 등 **DB 데이터는 전부 보존**

---

# V3 Reset (2026-04-29~)

V1 (Dash 웹, 사용성 부족) 과 V2 (FastAPI-only, UI 부재) 의 양 극단 실패를 교훈 삼아, V3 는 **비개발자 친화 풀스택 (FastAPI 백엔드 + Next.js 프런트)** 으로 재출발한다. 이 V3 섹션이 이후 설계의 **유일한 진실**이며, 상충 시 V3 를 우선 적용한다. V1/V2 섹션은 히스토리 보존 목적.

## V3 미션 (Quant Lab)

`projects/stock-backtest/CLAUDE.md` 의 미션을 그대로 인용:

> 비개발자 금융 사용자를 위한 퀀트 투자 웹앱. 핵심 기능은 **정적 자산 배분(SAA)**, **동적 자산 배분(DAA)**, **백테스팅** 세 가지이며 이 세 가지는 어떤 변경에도 항상 동작해야 한다.

V3 의 5개 절대 원칙 (CLAUDE.md L6-26):
1. JSON/코드를 사용자에게 노출하지 않는다 (모든 전략 구성은 UI 폼)
2. 모든 전략은 3요소 조합: `allocator` + `signal_filters[]` (AND) + `rebalance_schedule`
3. 백테스팅 실거래 반영도 최소 70% (수수료/슬리피지/look-ahead/배당/환율)
4. 결과 지표: CAGR, MDD, Sharpe, Sortino, Calmar, 승률, 연/월 수익률
5. MVP 프리셋 — Allocator 3종 (FixedWeight/AllWeather/EqualWeight) + Filter 2종 (MovingAverage/Momentum)

## V3 클린 코드 / 유지보수 원칙

V1/V2 에서 누적된 모순을 정리하고 다음 원칙을 강제한다:

1. **데이터 모델은 도메인 풍부도, UI 는 사용자 친화도 — 둘을 분리한다.** assets 테이블은 풍부한 분류(asset_type, currency, market, kr_tax_class) 보유. UI 노출은 사용자 지식 수준에 맞춰 점진 확장.
2. **UI/UX First**. 모든 신규 기능은 비개발자 사용자가 이해 가능한 UI 로 설계. 자세한 원칙은 § "V3 UI/UX 원칙" 참조.
3. **세금/수집/fx 등은 plugin 인터페이스로 시작**. MVP 가 빈 구현이거나 단일 구현이라도 추후 확장 가능한 추상화를 처음부터 도입.
4. **에이전트 위임 영역의 자율성**. Manager 와 사용자가 직접 결정한 영역(자산 도메인 + 현금/FX) 외는 V1/V2 결정 + V3 원칙 + Quant Lab CLAUDE.md 를 참조해 Coder/Tester/Reviewer 가 자체 결정. 차단 사유는 `signal/stock-backtest/blockers.md` 에 HARD/SOFT 구분으로 기록.

---

## V3 자산 도메인 모델

### 자산 분류 체계 (DB 풍부 / UI 단순)

DB `assets` 컬럼:
- `asset_id` PK
- `symbol` (yfinance/pykrx ticker), `(symbol, market)` UNIQUE
- `market` ∈ {`KR`, `US`, `CRYPTO`} — UI 노출 기준
- `asset_type` ∈ {`EQUITY_INDEX`, `ETF`, `BOND`, `COMMODITY`, `CRYPTO`, ...} — 내부 분류, 추후 UI 세분화 시 활용
- `currency` ∈ {`KRW`, `USD`, ...} — native currency, 환전 계산 기준
- `name` — 한글 표시명
- `meta` JSONB — `kr_tax_class` 등 미래 확장 (한국 상장 해외 ETF 세금 분류 등)
- `active` — 카탈로그 노출 여부
- `start_date`, `last_ingested_at`

UI 분류 (MVP):
- 시장(한국/미국/암호화폐) 단위로만 노출
- ETF/지수/채권 등 자산 타입 세분화는 Phase 2 이후 사용자 지식 성장 시 노출 검토

### 자산 카탈로그 + 사용자 자유 추가 (하이브리드)

- **카탈로그 (큐레이션)**: KR 주요 ETF (KODEX 200/KODEX 미국 S&P500 등), US 핵심 ETF (SPY/QQQ/TLT/GLD/DBC 등), 주요 암호화폐 (BTC/ETH 등) 50~100개 시드
- **사용자 자유 추가 워크플로우**:
  1. **즉시 검증** (3초 이내): yfinance/pykrx 에 ticker 존재 + 최소 1년치 일봉 데이터 유무 확인. 실패 시 즉시 에러 ("티커 'XYZ' 를 찾을 수 없습니다")
  2. **비동기 백필**: 검증 통과 시 `assets.active=true` 등록 + 백그라운드 백필 큐잉. UI 에는 "등록됨, 데이터 백필 중 (XX%)" 표시
  3. **부분 사용 가능**: 백필 진행 중에도 백필된 기간만큼 백테스트 가능 (자동 교집합)

### universe 정의

universe = 백테스트 1회에 사용할 자산 묶음. 백테스트 생성 폼에서 사용자가 자산 선택해 구성.

### universe 시작일 불일치 — 자동 교집합 + 통지

- universe 자산 시작일 다를 때 가장 늦은 시작일로 백테스트 기간 자동 조정
- 사용자에게 명시적 알림: "BTC 데이터 시작일이 2014-01-01 이라 백테스트 기간을 2014-01-01 ~ 로 조정했습니다"

### 멀티 마켓 캘린더 — base_currency 기준

- 백테스트 기준 캘린더 = `base_currency` 의 시장 캘린더
  - base=KRW → 한국 거래일 캘린더 (XKRX)
  - base=USD → 미국 거래일 캘린더 (NYSE)
- 비base 시장 자산은 base 캘린더 거래일 행에 **직전 자기 시장 거래일 종가 forward-fill**
  - 예: base=KRW 의 D 일 행에 표기되는 SPY 가격 = D-1 일 미국 종가 (한국 시간 D 일 새벽 발표)
- 암호화폐는 24/7 시장이므로 base 캘린더 D 일의 UTC 00:00 종가 사용

---

## V3 현금 / FX 모델

### B 모델 — Native currency 보유 + base_currency 환산

- 자산은 native currency 로만 체결·보유 (SPY=USD, KODEX200=KRW, BTC=USD)
- 현금은 currency 별 분리: `cash_by_ccy[KRW]`, `cash_by_ccy[USD]`, ...
- 매일 base_currency 로 equity 환산 저장 (각 자산 native value × 당일 fx_rate)

### base_currency 사용자 선택 (디폴트 없음)

백테스트 생성 시 사용자가 명시 (`KRW` / `USD` / 기타). 디폴트 강제 안 함. UI 에서 사용자별 마지막 선택값 기억해 다음 백테스트 시 프리셀렉트 가능.

### FX 거래는 trade 로 기록하지 않음 (잔고 이동 + 스프레드 차감)

- 리밸런싱 시 통화 이동 필요하면 엔진 내부에서 `cash_by_ccy` 잔고 이동 + `fx_spread_bps` 차감
- `backtest_trades` 테이블에는 자산 매매(BUY/SELL)만 기록
- equity 저하로만 환전 비용 반영

### 환전 정책 — 단계 분리 (C) + native 우선 (Q5-B)

리밸런싱 흐름:
1. 모든 매도 실행 → native currency 잔고로 입금
2. 같은 native currency 의 매수가 동일 리밸런싱에 있으면 **native 잔고 직접 활용** (환전 안 함)
3. native 잔고 부족 시 base_currency 로 환전 → 부족분만큼 다시 매수 native currency 로 환전 (환전 비용 양방향 발생)
4. 매수 실행

### fx_spread_bps = 20bp (defaults.yaml)

한국 증권사 환전 우대 평균 가정. 사용자가 변경 가능.

### 환율 시점 = 체결일 fx_rate 1개

- 일봉 fx_rate 만 사용 (시가/종가 구분 없음)
- 체결일 종가 fx_rate 로 환산

### fx 데이터 어댑터 (yfinance 디폴트, 교체 가능)

- MVP: yfinance "KRW=X" 등으로 일봉 환율 수집
- 갭 처리: 주말/공휴일 → 직전 영업일 환율 forward-fill
- 추후 한국은행 OpenAPI / FRED 어댑터 추가 가능 (어댑터 인터페이스 분리)

---

## V3 거래 정책

### Long-only, 음수 잔고 금지

- 매수 주문이 cash_by_ccy 잔고 초과 시 **가능한 만큼만 체결**, 나머지는 비중 미달로 결과에 노출
- 공매도/마진 미지원

### 1주 단위 정수, 잔여 cash 누적 (Q8, 2026-04-29 재결정 — 코인 한정 fractional)

- **주식/ETF/지수/채권/원자재 (KR/US market)**: 1주 단위 정수 매매
- **암호화폐 (CRYPTO market)**: 소수점 8자리까지 fractional 매매 (BTC 1코인 = $50k 같은 고가 자산이 작은 자본으로도 매수 가능)
- 분기 사유: BTC 1코인이 초기 자본보다 비싸면 정수 단위로는 0개 체결 → equity 평탄선. 사용자 첫 시도 사고 (run_id=56) 발견 후 결정. 일반 주식의 fractional shares 는 실거래에서 일부 증권사만 지원하므로 V3 는 코인만 허용.
- 구현: `Portfolio.buy(asset_id, currency, ...)` 가 자산의 market 또는 currency 가 CRYPTO 인지 분기. 정수 자산은 `int()` 강제, 코인은 `Decimal` 8자리 (또는 Position.qty 자체를 Decimal 로 통일).
- 비중 100% 정확히 못 채우는 잔액은 base_currency 잔고로 누적 (다음 리밸런싱에 활용)
- 암호화폐도 1코인 단위 — BTC 1개당 가격이 크면 작은 universe 비중에서 매수 안 될 수 있음을 UI 에 안내

### 시그널 / 체결 시점 — 모델 A (D 종가 시그널 → D+1 시가 체결)

V3 CLAUDE.md L20 원안 유지:
- D 일 종가까지의 데이터로 시그널 판정
- D+1 일 시가에 체결
- look-ahead 0 (시그널 결정 시점에 체결가는 모름)

엔진 규약:
- `generate_signal(prices_until_D)` 함수에 D+1 일 데이터를 절대 넘기지 않음 (구조적 차단)
- Tester 는 모든 전략에 대해 "D+1 데이터 노출 시 시그널 변화 없음" 회귀 테스트 필수

멀티 마켓 적용:
- 한국 자산 KODEX200: D 일 한국 종가 → D+1 한국 시가 체결
- 미국 자산 SPY: D 일 미국 종가 → D+1 미국 시가 체결 (base=KRW 캘린더 정렬 시 한 칸 어긋남이 자연스럽게 흡수됨)
- 단순화 표현: "각 자산은 자기 시장의 다음 거래일 시가에 체결"
- BTC: D 일 UTC 00:00 종가 → D+1 일 UTC 00:00 종가 (24/7 시장이라 시가/종가 구분 없음)

### 수수료 / 슬리피지 (V3 CLAUDE.md 디폴트)

- 수수료: 한국 0.015% / 미국 0.005% / 암호화폐 0.1% (market 별 자동 적용)
- 슬리피지: 0.1% (사용자 조정 가능)
- 둘 다 `defaults.yaml` 에서 시장별 오버라이드 가능

### 배당 처리

- 배당은 native currency 현금으로 수령 → `cash_by_ccy` 입금
- 다음 리밸런싱에 자동 편입
- yfinance dividends 사용. `corporate_actions` 테이블에 기록

### 분할/증자/감자 처리 (V3 MVP 임시처방)

- **yfinance**: `auto_adjust=True` 로 close 자체가 분할/배당 소급 보정된 가격.
  OhlcvBar.close 만 사용하면 분할 시 가짜 시그널 발동 방지.
- **pykrx**: 비조정가 한계 (한국 ETF 는 분할이 거의 없어 실전 영향 적음).
- **정공법 (Phase 2)**: corporate_actions SPLIT 이벤트를 엔진이 매일 EOD 시점에
  portfolio.position.qty 에 적용 + pykrx 별도 분할 데이터 수집. → BLOCKER-003.

---

## V3 백엔드 모듈 분할 (engine 분리 정책)

Quant Lab CLAUDE.md L39 의 `engine.py # 백테스팅 엔진 (단일 파일 유지)` 표현은 V3 에서 **"백테스트 메인 루프를 분산하지 마라"** 로 재해석한다 (V3 우선 원칙 L486 적용). 도메인 모델은 별도 파일로 분리해 책임을 단일화한다.

`backend/app/domain/` 모듈 분할:

| 파일 | 책임 | 담당 태스크 |
|------|------|-------------|
| `engine.py` | 백테스트 **메인 루프만** (시그널 호출 → 리밸런싱 → 거래 실행 → equity 기록 → 진행률/취소 체크). 도메인 모델 직접 정의 금지, 전부 import. | TASK-043 (Strategy 인터페이스를 호출하는 루프 골격) |
| `portfolio.py` | Portfolio 클래스 + `cash_by_ccy` 잔고 관리 + 환전 엔진 (단계 분리 C + native 우선 B + fx_spread 20bp). FX 는 잔고 이동, trade 미기록. | TASK-040 |
| `trade.py` | 거래 실행 로직 (long-only, 음수 잔고 금지, 정수 주, 부족 시 가능한 만큼만 체결, 잔여 cash 누적, 수수료·슬리피지 시장별 자동 적용). | TASK-041 |
| `calendar.py` | 멀티 마켓 캘린더 정렬 (base_currency 기준 + 비base 시장 forward-fill, exchange_calendars 사용, 비거래일 방어 — 엔진 레이어). | TASK-042 |
| `strategy.py` | Strategy 인터페이스 (allocator + filters AND + rebalance_schedule), Allocator base, Filter base. 시그널/체결 모델 A 구조적 차단 (`generate_signal(prices_until_D)` 슬라이싱 강제). | TASK-043 |
| `allocators/{fixed_weight,all_weather,equal_weight}.py` | Allocator 구현 3종. | TASK-050, 051, 052 |
| `filters/{moving_average,momentum}.py` | Filter 구현 2종. | TASK-053, 054 |
| `metrics.py` | 메트릭 계산 (CAGR/MDD/Sharpe/Sortino/Calmar/승률/연·월 수익률). | TASK-044 |
| `dividend.py` | 배당 처리 (corporate_actions 기록 → cash_by_ccy 입금 → 다음 리밸런싱 편입). | TASK-044 |
| `tax.py` | Tax plugin 인터페이스 + NoTaxPlugin. | TASK-045 |

**병렬 안전성**: 위 매핑으로 TASK-040~045 가 서로 다른 파일을 수정하므로 의존성 순서만 지키면 동시 충돌 없음. `engine.py` 는 TASK-043 가 만들지만 다른 모듈을 import 만 하므로 이후 태스크가 추가 import 만 하면 됨.

---

## V3 세금 모듈 (Plugin 인터페이스)

### MVP: 디폴트 OFF, 빈 구현

- `Tax` plugin 인터페이스 정의 (`apply(realized_trades, dividends, year) -> tax_amount`)
- MVP 디폴트 구현 = `NoTaxPlugin` (세금 0)
- UI 에서 "세후 수익률 계산" 토글 (디폴트 OFF)

### 추후 확장 가능 항목 (Phase 3+)

- **한국 거주자 세금**: 해외 양도세 22% (250만원 공제), 배당 15.4%, 한국 상장 해외 ETF (kr_tax_class 별 차등), 암호화폐 양도세 (시행 시점 확정 후)
- 사용자가 본인 세법 무지로 MVP 에서 제외했으나 의사결정 본질에 영향이 큰 영역. plugin 추가 시 즉시 활성 가능하도록 인터페이스만 선설계

---

## V3 UI / UX 원칙

V1 의 Dash 사용성 부족과 V2 의 UI 부재를 피하기 위한 명시적 원칙. **모든 화면 설계 시 이 6개 원칙을 통과해야 한다.**

### 1. JSON / 코드 노출 금지
- 전략 구성은 항상 폼 (드롭다운 + 슬라이더 + 체크박스)
- 자산 입력은 검색 위젯 (자동완성, 한글명 검색 지원, ticker 직접 입력은 "자유 추가" 버튼 분리)
- 비중 입력은 숫자 + 슬라이더 + 합 100% 자동 검증/정규화

### 2. 비개발자 한국어 우선
- 모든 라벨/에러 메시지/안내 한국어 기본
- 영어 전문 용어는 괄호 병기 ("샤프지수(Sharpe Ratio)")
- 에러는 액션 가능한 가이드 형태 ("티커 'XYZ' 를 찾을 수 없습니다. yfinance 검색에서 유효한 ticker 인지 확인하세요" 식)

### 3. 진행 상태 가시화
- 자산 백필 진행률 (XX%)
- 백테스트 실행 진행률 (V2 비동기 job 모델: POST → run_id → 폴링)
- 데이터 갭/조정 통지 (예: "BTC 시작일 때문에 기간 조정됨")

### 4. 결과 시각화 (V3 CLAUDE.md L24)
- equity curve (선형 차트, log 토글)
- drawdown (선형 차트)
- 지표 테이블: CAGR, MDD, Sharpe, Sortino, Calmar, 승률
- 연/월 수익률 히트맵
- 거래 내역 테이블 (페이지네이션, 통화별 그룹)

### 5. 폼 검증 (Zod 런타임)
- 프런트 Zod 스키마로 백엔드 Pydantic 과 동기 (V3 CLAUDE.md 코드 규칙)
- 입력 시점 즉시 피드백 (제출 후 아니라)

### 6. 점진적 노출
- MVP 화면 3개만: ① 백테스트 생성 ② 결과 보기 ③ 자산 카탈로그
- 사용자 지식 성장 시 추가 노출 (asset_type 세분화, 세금 토글, fx 어댑터 선택, 수수료 오버라이드 등)

---

## V3 에이전트 위임 영역

이번 대화에서 결정 안 한 영역은 다음 가이드에 따라 Manager / Coder / Tester / Reviewer 가 자체 진행. 차단 사유는 `signal/stock-backtest/blockers.md` 에 HARD/SOFT 구분 기록.

| 영역 | 가이드 |
|------|--------|
| DB 스키마 | V1 § "DB 스키마 (요약)" + 위 자산 도메인 모델 반영 |
| API | V2 § "V2 API (FastAPI)" 참조. OpenAPI-first. 비동기 job 모델. 에러 응답 계약 (stage/ctx/trace_id) |
| 데이터 수집 | V1 § 결정 9 (DB 기반 증분, cron, 갭 감지, 멱등 UPSERT) + 비거래일 다층 방어 (V1 결정 13) |
| 전략 인터페이스 | V3 CLAUDE.md 3요소 (allocator + filters AND + rebalance_schedule) + V2 § "V2 전략 조합" SignalMask |
| 프런트 | V3 CLAUDE.md 디렉토리 (Next.js App Router + shadcn/ui + Zod) + 위 UI/UX 원칙 6개 강제 |
| 테스트 | V3 CLAUDE.md "골든 테스트" + V2 schemathesis fuzz + look-ahead 회귀 테스트 |

### Blocker 정책

- `blockers.md` 형식 (append-only):
  ```markdown
  ## BLOCKER-001 [HARD|SOFT] (TASK-XXX)
  - 발견 시점: YYYY-MM-DD
  - 차단 영역: (DB 스키마 / API / 프런트 / ...)
  - 사유: (왜 사용자 판단이 필요한가)
  - 우회 방안: (SOFT 일 때만, mock/빈 구현으로 진행할 방법)
  - 처리 결과: TODO | RESOLVED (날짜)
  ```
- **HARD**: 선결되지 않으면 진행 불가능 → 즉시 멈추고 Manager 가 사용자에게 보고
- **SOFT**: mock/빈 구현으로 우회 가능 → 우회 + 해당 task-board 에 TODO 등록 + 계속 진행
- 모든 태스크 완료 후 Manager 가 blockers 재독 → 자체 처리 시도 → 잔여 blocker 만 사용자 보고

---

## V3 Phase 분리

| Phase | 범위 |
|-------|------|
| **Phase 1 (MVP)** | Allocator 3종 (FixedWeight, AllWeather, EqualWeight) + Filter 2종 (MovingAverage, Momentum) + 백엔드 (FastAPI + DB + 데이터 수집 cron + 백테스트 엔진) + 프런트 (Next.js + 화면 3개) + Tax plugin 인터페이스 (빈 구현) |
| **Phase 2** | 계절성 분석 (V1 결정 12 의 정치 사이클·FOMC·Sell-in-May·실적시즌·한국 정치) + market_events 테이블 + 분석 페이지 |
| **Phase 3+** | 한국 거주자 세금 plugin 구현, asset_type UI 세분화, 추가 allocator/filter, 한국은행 fx 어댑터, 다중 전략 합성 (composer) UI |

---

## V1 / V2 결정 — 폐기 / 살림 일람

### V1 폐기
- Dash 웹 (`src/stock_backtest/web/`) 전체
- `_CASH_` 문자열 컬럼 방식 (V2 폐기, V3 도 cash_by_ccy 잔고)
- FX TradeRecord 스키마 (V2 폐기, V3 도 trade 미기록)
- dynamic 전략 5종 (momentum/dual_momentum/vaa/risk_parity/moving_average 변형) — Phase 3 재검토

### V1 살림
- assets 풍부 분류 (asset_type, market, currency, kr_tax_class)
- ohlcv hypertable (TimescaleDB)
- 데이터 수집 cron (KR 18:00 / US 07:00 / Crypto 09:00 KST, 자산 단위 3회 재시도, 갭 자동 감지)
- 비거래일 다층 방어 (수집/캘린더/조회/엔진 4단계)
- exchange_calendars 사용
- 재현성 (code_commit_hash + data_hash + STALE 플래그)
- backtest_runs.run_hash 캐싱

### V2 폐기
- "FastAPI-only, 웹 제거" → V3 는 Next.js 프런트 부활
- Cash NamedTuple 타입화 → V3 는 cash_by_ccy[ccy] 딕셔너리로 단순화
- AND composer (SignalMask) 즉시 구현 → V3 Phase 1 은 단일 전략(allocator + filters AND) 만, 다중 전략 합성은 Phase 3+

### V2 살림
- 에러 응답 계약 (stage/ctx/trace_id, 전역 예외 핸들러)
- 비동기 job 모델 (POST → run_id → 폴링, 진행률, 취소)
- OpenAPI-first 개발 (docs/openapi.yaml 먼저 확정)
- Golden snapshot 테스트 + schemathesis fuzz
- 검증 포인트 (동시 job 독립성, 취소 시 트랜잭션 정리, 워커 크래시 복구)

---

## V3 현재 상태

- 사용자와 자산 도메인 + 현금/FX 핵심 결정 완료 (Q1~Q16)
- architecture.md V3 섹션 작성 완료 (2026-04-29)
- 다음 단계: task-board.md 분해 → Reviewer 검증 → Coder/Tester 위임 루프 시작
