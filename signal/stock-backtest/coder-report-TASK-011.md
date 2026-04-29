---
agent: coder
task_id: TASK-011
status: DONE
timestamp: 2026-04-29T00:00:00
---

## 결과 요약

architecture.md V3 § "DB 스키마" L227-234 의 V1 살림 정의에 따라 시계열 3 테이블 (ohlcv / fx_rates / corporate_actions) 의 SQLAlchemy 2.0 ORM 모델과 alembic revision `0002_timeseries_tables` 를 추가했다. ohlcv 는 TimescaleDB hypertable 변환을 포함하며, 일반 PostgreSQL 환경에서도 fail 하지 않도록 try/except + 경고 로그 처리. DoD 5 항목 모두 통과.

## 변경된 파일

- `projects/stock-backtest/backend/app/models/ohlcv.py` (신규)
- `projects/stock-backtest/backend/app/models/fx_rates.py` (신규)
- `projects/stock-backtest/backend/app/models/corporate_actions.py` (신규)
- `projects/stock-backtest/backend/app/models/__init__.py` (수정 — Ohlcv/FxRate/CorporateAction re-export 추가, 알파벳순 정렬)
- `projects/stock-backtest/backend/alembic/versions/0002_timeseries_tables.py` (신규)

## DoD 결과

| # | 항목 | 명령 | 기대 | 실측 | 결과 |
|---|------|------|------|------|------|
| 1 | 모델 import 스모크 | `python -c "from app.models import Ohlcv, FxRate, CorporateAction; print(...)"` | `ohlcv fx_rates corporate_actions` | `ohlcv fx_rates corporate_actions` | PASS |
| 2 | metadata 테이블 목록 | `python -c "from app.core.db import Base; ..."` | `['assets', 'corporate_actions', 'fx_rates', 'ingestion_log', 'ohlcv']` | `['assets', 'corporate_actions', 'fx_rates', 'ingestion_log', 'ohlcv']` | PASS |
| 3 | CreateTable SQL 스모크 | `CreateTable + CreateIndex compile(postgresql)` | 각 테이블 PK / FK / 인덱스 정의 정상 | `ohlcv` PK(asset_id, time) + FK assets ON DELETE CASCADE / `fx_rates` PK(base_ccy, quote_ccy, time) / `corporate_actions` PK(action_id) + FK assets ON DELETE CASCADE + `ix_corporate_actions_asset_time` (asset_id, time) | PASS |
| 4 | alembic dry-run | `alembic upgrade head --sql` | `0002_timeseries_tables` CREATE TABLE 3건 + `SELECT create_hypertable(...)` 포함 | 출력에 `CREATE TABLE ohlcv` / `CREATE TABLE fx_rates` / `CREATE TABLE corporate_actions` / `CREATE INDEX ix_corporate_actions_asset_time` / `SELECT create_hypertable('ohlcv', 'time', if_not_exists => TRUE);` 모두 확인 | PASS |
| 5 | revision 그래프 | `alembic history` | `0001_v3_baseline → 0002_timeseries_tables` | `0001_v3_baseline -> 0002_timeseries_tables (head), 시계열 테이블 — ohlcv (hypertable) + fx_rates + corporate_actions.` `<base> -> 0001_v3_baseline, v3 baseline — assets + ingestion_log.` | PASS |

## 주요 설계 결정

1. **numeric precision/scale 일관**:
   - 가격 4종 (open/high/low/close/adj_close) + fx rate + corporate_action.value: `Numeric(20, 8)` — 암호화폐 8자리 소수 + 큰 정수 가격 모두 수용.
   - volume: `Numeric(20, 0)` — 정수형이지만 BigInteger 한계(2^63 ≈ 9.2e18) 초과 가능성 대비 Numeric(20, 0).
2. **timezone-aware datetime 강제**: 모든 `time` 컬럼 `DateTime(timezone=True)` — UTC 저장, 표시 계층에서 변환.
3. **close NOT NULL**: 비거래일/공휴일은 row 자체를 적재하지 않는 정책 (수집 레이어 책임). architecture.md "비거래일 방어" 정책 반영.
4. **hypertable try/except**: TimescaleDB extension 이 없는 일반 PostgreSQL CI/test 환경에서도 마이그레이션이 멈추지 않도록 `DatabaseError` catch + 경고 로그. production (TimescaleDB 가정) 에서는 정상 변환.
5. **corporate_actions surrogate PK + 보조 인덱스**: 동일 자산·동일 시점에 여러 종류의 권리 이벤트가 있을 수 있어 (asset_id, time) 복합 PK 대신 `action_id` surrogate PK + (asset_id, time) 인덱스로 시계열 조회 최적화.
6. **fx_rates 일반 테이블**: 데이터량이 ohlcv 대비 작아 hypertable 변환 안 함 (architecture.md 명시).
7. **JSONB default `{}`**: corporate_actions.meta 는 assets.meta 와 동일 패턴 — `server_default="'{}'::jsonb"` 으로 NOT NULL 회피하면서 코드 처리 단순화.

## 클린 코드 점검

- 한 파일 = 한 모델 (Ohlcv, FxRate, CorporateAction 분리).
- 모든 모델이 `app.core.db.Base` 단일 metadata 사용 (DeclarativeBase 통일).
- TimestampedModel mixin 미사용 — 시계열 row 는 created_at/updated_at 의미 없음 (시점 자체가 키).
- 주석은 "왜" (정책 근거, architecture.md 참조) 만 기재. "무엇" 주석 없음.

## 이슈/블로커

없음.

## 다음 제안

- **TASK-012 (백테스트 테이블)**: 다음 revision `0003_backtest_tables` 로 backtest_runs / backtest_equity (hypertable) / backtest_trades / backtest_metrics 추가. down_revision 은 `"0002_timeseries_tables"`.
- **DB 적용 (BLOCKER-001 해소 후)**: 사용자가 V1/V2 잔재 초기화 후 `alembic upgrade head` 적용. TimescaleDB extension 이 활성화되어야 hypertable 변환 성공 — `CREATE EXTENSION IF NOT EXISTS timescaledb;` 가 baseline 외부에서 1회 실행되어야 함 (현재 0001/0002 어느 쪽에도 포함되어 있지 않음 — 별도 인프라 작업으로 처리하거나 0002 에 추가하는 것을 검토 권장).
- **backtest_equity hypertable 변환 시**: TASK-012 도 동일한 try/except 패턴을 따르도록 권장.
