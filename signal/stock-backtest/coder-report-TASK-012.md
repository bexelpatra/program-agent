---
agent: coder
task_id: TASK-012
status: DONE
timestamp: 2026-04-29T00:00:00
---

## 결과 요약

architecture.md V3 § "DB 스키마" L242-251 (V1 살림) + § "비동기 job 모델" L437-446 + § "에러 응답 계약" L450 (V2 살림) 정의에 따라 백테스트 결과 도메인 4 테이블 (`backtest_runs` / `backtest_equity` / `backtest_trades` / `backtest_metrics`) 의 SQLAlchemy 2.0 ORM 모델과 alembic revision `0003_backtest_tables` 를 추가했다. 4개 모델은 응집도(모두 run_id 기반 관계, Run import 순환 방지)를 위해 `backtest.py` 한 파일에 묶었다. `backtest_equity` 는 TimescaleDB hypertable 변환을 포함하며 0002 와 동일하게 `try/except` + 경고 로그로 일반 PostgreSQL 환경 호환. `backtest_trades.side` 는 DB 레벨 `CHECK (side IN ('BUY', 'SELL'))` 으로 V3 § FX trade 미기록 정책 (architecture.md L389) 을 강제. DoD 5 항목 모두 통과.

## 변경된 파일

- `projects/stock-backtest/backend/app/models/backtest.py` (신규 — BacktestRun, BacktestEquity, BacktestTrade, BacktestMetric 4개 ORM)
- `projects/stock-backtest/backend/app/models/__init__.py` (수정 — 4개 re-export 추가, 알파벳순 정렬, `__all__` 9개)
- `projects/stock-backtest/backend/alembic/versions/0003_backtest_tables.py` (신규 — down_revision="0002_timeseries_tables")

## DoD 결과

| # | 항목 | 명령 | 기대 | 실측 | 결과 |
|---|------|------|------|------|------|
| 1 | 4개 모델 import 스모크 | `python -c "from app.models import BacktestRun, BacktestEquity, BacktestTrade, BacktestMetric; print(...)"` | `backtest_runs backtest_equity backtest_trades backtest_metrics` | `backtest_runs backtest_equity backtest_trades backtest_metrics` | PASS |
| 2 | metadata 9개 테이블 | `python -c "from app.core.db import Base; import app.models; print(sorted(Base.metadata.tables.keys()))"` | 9개 (assets, backtest_equity, backtest_metrics, backtest_runs, backtest_trades, corporate_actions, fx_rates, ingestion_log, ohlcv) | `['assets', 'backtest_equity', 'backtest_metrics', 'backtest_runs', 'backtest_trades', 'corporate_actions', 'fx_rates', 'ingestion_log', 'ohlcv']` | PASS |
| 3 | CHECK constraint 존재 | `python -c "... print(BacktestTrade.__table__.constraints)"` 후 sqltext 추출 | `side IN ('BUY', 'SELL')` 포함 | `CHECK: ck_backtest_trades_side -> side IN ('BUY', 'SELL')` | PASS |
| 4 | alembic dry-run | `alembic upgrade head --sql` | 0003 의 CREATE TABLE 4건 + UNIQUE + CHECK + hypertable 출력 | `CREATE TABLE backtest_runs` / `CREATE TABLE backtest_equity` / `CREATE TABLE backtest_trades` (`CONSTRAINT ck_backtest_trades_side CHECK (side IN ('BUY', 'SELL'))` 포함) / `CREATE TABLE backtest_metrics` (`CONSTRAINT uq_backtest_metrics_run_name UNIQUE (run_id, metric_name)` 포함) / `CREATE UNIQUE INDEX ix_backtest_runs_run_hash` / `SELECT create_hypertable('backtest_equity', 'time', if_not_exists => TRUE);` 모두 확인 | PASS |
| 5 | revision 그래프 | `alembic history` | `0001 → 0002 → 0003 (head)` | `0002_timeseries_tables -> 0003_backtest_tables (head), ...` / `0001_v3_baseline -> 0002_timeseries_tables, ...` / `<base> -> 0001_v3_baseline, ...` | PASS |

## 주요 설계 결정

1. **4개 모델 = 한 파일 (`backtest.py`)**: 모두 `backtest_runs.run_id` 기반 FK 관계. Run/Equity/Trade/Metric 분리 시 모두 Run 을 import 하면서 SQLAlchemy 모듈 import 순서 의존성 발생 (Mapped relationship 미사용 단계라도 동일 metadata 보장이 우선). 응집도 ↑ + 순환 위험 ↓.
2. **status / market_mode / side / metric_name 모두 String + 애플리케이션 검증**: Postgres ENUM 마이그레이션 부담 회피 (assets.asset_type, ingestion_log.status 와 동일 패턴). 단 `side` 만은 V3 § FX trade 미기록 정책 (L389) 의 강제력 확보를 위해 DB 레벨 `CHECK` 추가 — 다른 컬럼은 값 집합 변경 가능성이 있어 ENUM/CHECK 모두 회피, side 는 BUY/SELL 외 확장 의도 없음.
3. **error_json JSONB**: V2 § "에러 응답 계약" L450 의 `{stage, type, message, request_ctx, trace_id}` 구조 그대로 적재. Pydantic schema 는 TASK-062 에서 정의 예정. 본 태스크에서는 구조 미정 가능성 + 부분 인덱싱 여지 확보를 위해 JSONB nullable 로 둠.
4. **universe JSONB (FK 없음)**: `[{"asset_id": int, ...}]` 형식. assets FK 미지정 — universe 는 실행 시점 스냅샷 성격이라 자산이 후일 deactivate/delete 되어도 run 이력은 보존되어야 함. asset_id 로 join 은 가능하지만 DB 레벨 강제 안 함.
5. **trades.asset_id ON DELETE RESTRICT**: 실제 거래된 자산은 카탈로그에서 강제 삭제 불가 (감사성). universe JSONB 와 의도적으로 다른 정책.
6. **progress = Float (0.0~1.0)**: 정밀도 요구 없음 (UI 표시는 % 반올림). Numeric 회피로 직렬화/연산 비용 절약.
7. **drawdown = Numeric(10, 6)**: -99.999999% 까지 표현. equity 와 다른 scale 인 이유는 비율 표현이라 8자리까지 불필요 + 컬럼 크기 절약.
8. **hypertable try/except**: 0002 ohlcv 와 동일 패턴 — `DatabaseError` catch + 경고 로그. CI/test 의 일반 PostgreSQL 환경에서도 마이그레이션 통과.
9. **인덱스 3종 on backtest_runs**: `status` (job 큐 폴링), `run_hash UNIQUE` (캐시 hit 판정), `created_at` (최근 run 이력 페이징) — 모두 명시적 사용 시나리오 존재.
10. **`__all__` 알파벳순**: 0002 에서 도입한 컨벤션 유지 (Asset → BacktestEquity → BacktestMetric → BacktestRun → BacktestTrade → CorporateAction → FxRate → IngestionLog → Ohlcv).

## 클린 코드 점검

- 4개 모델 한 파일 = 명시적 응집도 결정 (TASK 명세 § "클린 코드 점검" 의 근거 그대로 적용).
- 모든 모델이 `app.core.db.Base` 단일 metadata 사용.
- TimestampedModel mixin 미적용 — 백테스트 row 는 created/started/finished_at 으로 의미 분리(updated_at 의미 없음). Run 만 created_at 보유, Equity/Trade/Metric 은 시점 자체가 키.
- 주석은 "왜" (정책 근거, architecture.md 라인 참조) 만. "무엇" 주석은 컬럼 이름/타입으로 충분.
- Single Responsibility: 본 파일은 백테스트 결과 영속화 모델 정의만 담당. domain 로직 없음 (engine.py 책임).

## 이슈/블로커

없음. 병렬 안전성도 확보 (TASK-020 backend/app/data/, TASK-032 backend/app/domain/ 와 파일 충돌 없음).

## 다음 제안

- **TASK-013 (Repository 레이어)**: 본 모델들에 대한 `backtest_repository.py` (insert_run / update_status / append_equity / bulk_insert_trades / list_recent_runs 등) 권장. ORM 직접 사용을 서비스 레이어에 노출하지 않도록.
- **TASK-062 (에러 응답 Pydantic)**: `error_json` JSONB 의 정합성을 위해 `BacktestRunError(BaseModel)` (stage / type / message / request_ctx / trace_id) Pydantic schema 정의 권장. Repository 의 `mark_failed(run_id, error: BacktestRunError)` 와 직결.
- **TimescaleDB extension 활성화 (BLOCKER-001 연관)**: 0002/0003 어느 쪽에도 `CREATE EXTENSION IF NOT EXISTS timescaledb;` 가 포함되어 있지 않음. production DB 에서 hypertable 변환이 try/except 로 silent fail 하면 backtest_equity 시계열 성능이 저하됨. 별도 인프라 작업 또는 0001 baseline 보강 검토 권장.
- **(향후) backtest_runs.user_id FK 승격**: 멀티유저 도입 시 `users` 테이블 생성 + FK + 기본값 'local' 폐기 마이그레이션 필요.
