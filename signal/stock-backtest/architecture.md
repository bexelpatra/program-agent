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
3. **FX 변환은 명시적 trade 레코드**. `_ensure_cash` 에서 통화 변환이 발생할 때마다 `side="FX"` TradeRecord 생성.

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

### FX TradeRecord 스키마 확장
- `backtest_trades.side` CHECK 제약에 `"FX"` 추가
- nullable 컬럼 추가: `currency_from`, `currency_to`, `fx_rate`, `spread_bps`
- `asset_id` FK nullable 허용 (FX 는 자산 없음)
- `_ensure_cash` 에서 통화 변환 시 `TradeRecord(side="FX", asset_id=NULL, currency_from=src, currency_to=dst, qty=amount, price=fx_rate, ...)` 생성

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
- DB `backtest_trades` 는 V1 그대로 (asset_id nullable + side 구분).

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
