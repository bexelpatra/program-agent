---
task_id: TASK-046
agent: coder
status: DONE
date: 2026-04-14
---

# TASK-046: USD 합성 자산 등록

## 결과

- USD 합성 자산을 DB에 적재 완료.
  - asset_id=84, symbol=USD, market=CASH, asset_type=CASH, currency=USD,
    name="US Dollar Cash", start_date=2000-01-01, active=True.
- OHLCV 9601행 적재 (2000-01-01 ~ 2026-04-14, 매 캘린더일 1행).
  - open/high/low/close/adj_close=1.0, volume=0.
- 멱등성 확인: 두 번째 실행 시 `rows_inserted=0`.

## 변경 파일

- `projects/stock-backtest/scripts/seed_usd_cash.py` (신규)
- `projects/stock-backtest/migrations/versions/0002_add_cash_market_type.py` (신규 마이그레이션)
- `projects/stock-backtest/src/stock_backtest/data/models.py`
  (`ck_assets_market`, `ck_assets_asset_type` 에 `'CASH'` 추가)

## 마이그레이션 노트

기존 `ck_assets_market` / `ck_assets_asset_type` CHECK 제약이
`('KR','US','GLOBAL','CRYPTO')` / `('EQUITY_INDEX','ETF','BOND','COMMODITY','CRYPTO')`
로 한정되어 있어 `market='CASH'`, `asset_type='CASH'` 적재가 불가능했다.
- Alembic revision `0002_add_cash_market_type` 를 추가하여 두 제약에
  `'CASH'` 를 포함하도록 재정의.
- `alembic upgrade head` 적용 완료. 모델 측 `CheckConstraint` 도
  동일하게 갱신.

## 검증

```text
asset: US Dollar Cash market=CASH type=CASH currency=USD
ohlcv count/min/max: (9601,
  datetime.datetime(2000, 1, 1, 0, 0, tzinfo=UTC),
  datetime.datetime(2026, 4, 14, 0, 0, tzinfo=UTC))
sample close/volume: (1.0, 0.0)
```

`AssetRepository(s).list_active()` 에서 USD 가 정상적으로 노출되며,
`OhlcvRepository.upsert_bulk` (1000행 batch) 로 적재.

## 이슈/블로커

없음.

### Observation (severity: observation)

- `market='CASH'` 에 대한 거래일 캘린더 매핑은 본 태스크에서 검증하지
  않음 (스펙상 다음 태스크의 엔진/테스트에서 자연 노출 예정).
- USD 는 currency=USD 이므로 환율 모듈에서 base 일치 시 추가 변환 없이
  통과될 것으로 예상.
