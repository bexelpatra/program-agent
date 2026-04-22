---
agent: coder
task_id: TASK-052
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약

`backtest_trades` 테이블을 FX 1급 레코드로 확장하고, `Portfolio._ensure_cash` 가
통화 변환을 수행할 때마다 `side="FX"` TradeRecord 를 엔진 trade 이력에
추가하도록 구현했다. alembic 0003 마이그레이션을 작성·적용했고, ORM·run_store·
repository 를 새 스키마에 맞춰 갱신했다.

## 변경된 파일

- `projects/stock-backtest/migrations/versions/0003_fx_trade_support.py` (신규)
  - `ck_backtest_trades_side` 를 `('BUY','SELL','FX')` 로 확장
  - `backtest_trades.asset_id` FK → nullable
  - 신규 nullable 컬럼 4개: `currency_from VARCHAR(8)`, `currency_to VARCHAR(8)`,
    `fx_rate NUMERIC(20,10)`, `spread_bps INTEGER`
  - downgrade: 컬럼 drop + FX 행 DELETE + asset_id NOT NULL 복원 + CHECK 축소
- `projects/stock-backtest/src/stock_backtest/data/models.py` (수정)
  - `BacktestTrade.asset_id` → `Optional[int]`, `nullable=True`
  - 4개 컬럼 매핑 추가 (`currency_from/to`, `fx_rate`, `spread_bps`)
  - `ck_backtest_trades_side` 제약 문자열 `'BUY','SELL','FX'` 로 갱신
  - `Numeric`, `String` import 추가
- `projects/stock-backtest/src/stock_backtest/backtest/portfolio.py` (수정)
  - 신규 dataclass `FXTradeEvent(date, currency_from, currency_to, qty, fx_rate, spread_bps)`
  - `Portfolio.fx_trades: list[FXTradeEvent]` 필드 추가 (`__all__` 반영)
  - `_ensure_cash`: 변환이 발생할 때마다 mid-rate + portfolio `fx_spread_bps`
    를 기록하는 `FXTradeEvent` 를 `self.fx_trades` 에 append
    (full-drain 케이스와 partial-drain 케이스 둘 다)
- `projects/stock-backtest/src/stock_backtest/backtest/engine.py` (수정)
  - `TradeRecord`: `asset_id` → `int | None`, FX 전용 필드
    `currency_from / currency_to / fx_rate / spread_bps` 옵셔널 추가
  - `run()` 루프: 각 `apply_trade` 호출 전후 `portfolio.fx_trades` 스냅샷을
    떠서 새로 추가된 FX 이벤트를 `TradeRecord(side="FX", ...)` 로 변환해
    BUY/SELL 레코드보다 **먼저** `trade_records` 에 넣는다.
- `projects/stock-backtest/src/stock_backtest/backtest/run_store.py` (수정)
  - `save_run`: trade payload 에 `currency_from/to/fx_rate/spread_bps` 전달
  - `load_run`: 반환 dict 에 동일 컬럼 포함
- `projects/stock-backtest/src/stock_backtest/data/repository.py` (수정)
  - `bulk_insert_trades`: `asset_id` None 허용 + 신규 4개 컬럼 전달
- `projects/stock-backtest/src/stock_backtest/metrics/performance.py` (수정)
  - `turnover`: `side == "FX"` 행은 스킵 (FX qty*price 는 자산 notional 이 아님)
- `projects/stock-backtest/scripts/smoke_fx_trade.py` (신규, 검증용 스크립트)

## 공개 API 변경

- `stock_backtest.backtest.portfolio`
  - 신규 dataclass `FXTradeEvent(date, currency_from, currency_to, qty, fx_rate, spread_bps)`
  - `Portfolio` 필드 추가: `fx_trades: list[FXTradeEvent]`
- `stock_backtest.backtest.engine.TradeRecord`
  - 시그니처 확장: `asset_id: int | None`,
    신규 옵셔널 필드 `currency_from`, `currency_to`, `fx_rate`, `spread_bps`
- `stock_backtest.data.repository.bulk_insert_trades(session, run_id, rows)`
  - rows 스키마에 신규 키 `currency_from, currency_to, fx_rate, spread_bps`
    (모두 옵셔널, 기존 BUY/SELL 행은 `asset_id` 만 int 유지하고 나머지 생략 가능)
- `stock_backtest.backtest.run_store.load_run(...)` 반환 trade dict 에
  `currency_from, currency_to, fx_rate, spread_bps` 키 추가

## Smoke 검증

1. `alembic upgrade head` → `0002 -> 0003` 정상 적용 (로그 확인 완료).
2. `python -c "from stock_backtest.data.models import BacktestTrade; print(list(BacktestTrade.__table__.c.keys()))"`
   결과:
   ```
   ['id', 'run_id', 'time', 'asset_id', 'side', 'qty', 'price', 'commission',
    'currency', 'currency_from', 'currency_to', 'fx_rate', 'spread_bps']
   asset_id nullable= True
   ```
3. `scripts/smoke_fx_trade.py`: KRW 10_000_000 로 시작한 포트폴리오가
   USD@500 의 자산 10주 매수 시 KRW→USD FX 이벤트 1건을 남긴다.
   ```
   FX event: {'from_': 'KRW', 'to': 'USD', 'qty': '6770268.57...',
              'fx_rate': '0.00074074...', 'spread_bps': '20'}
   cash_by_ccy after: {'KRW': '3229731.43...', 'USD': '0'}
   ```
   → FX record 생성 + 이후 USD 로 매수 완료 확인.

## 이슈/블로커

- pytest 전체 실행은 환경 레벨에서 `dash._jupyter` 임포트 시
  `comm.create_comm` 가 `NotImplementedError("Cannot")` 을 던져 수집
  단계에서 실패한다. 본 태스크와 무관한 기존 환경 이슈이며, 구현 경로는
  smoke 스크립트로 검증됨. 필요 시 tester 세션에서 별도 점검 권장.
- FX 행을 DB 에 저장할 때 `fx_rate` 는 `NUMERIC(20,10)` 로 저장하기 위해
  `run_store.save_run` 에서 `float(t.fx_rate)` 로 캐스팅한다. SQLAlchemy
  드라이버가 float→Numeric 변환을 수행하므로 정밀도 손실 가능성 있음
  — 향후 정밀도 민감한 집계가 필요하면 `str(Decimal)` 바인딩으로 교체 고려.

## 다음 제안

- Tester: BUY 가 실제로 `_ensure_cash` 를 트리거하는 시나리오(기본 KRW / USD
  자산)에서 engine 실행 결과 `result.trades` 에 BUY 앞에 FX 행이 나타나는지
  회귀 테스트 추가.
- 웹 UI 상세 거래 테이블(별도 태스크)에서 FX 행을 다른 스타일(hash fill 등)
  로 구분 렌더링 고려.
