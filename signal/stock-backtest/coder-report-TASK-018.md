# Coder Report — TASK-018

- Task ID: TASK-018
- Title: Run 저장/캐싱 (run_hash, code_commit_hash, data_hash, STALE 판정)
- Status: DONE

## 작업 요약

backtest_runs 영속화 + 캐시 판정 로직을 구현했다. 엔진 코어는 손대지 않고
외부 래핑 레이어만 추가했으며, `repository.py`는 기존 메서드 시그니처 변경 없이
추가(additive)만 했다.

## 변경 파일

- `projects/stock-backtest/src/stock_backtest/backtest/cache.py` (확장)
  - `compute_run_hash` 유지
  - `compute_code_commit_hash(cwd=None) -> str` 신규
    - `git rev-parse HEAD` 서브프로세스. 실패/미설치/비-레포 모두 `"unknown"`.
    - `FileNotFoundError`, `OSError`, `SubprocessError`, 비-zero returncode, 빈 stdout 전부 방어.
  - `compute_data_hash(session, asset_ids) -> str` 신규
    - 각 asset의 `MAX(ohlcv.time)` + `COUNT(*)`를 asset_id 오름차순 정렬 후 sha256.
    - ORM 쿼리 경로 우선, 실패 시 raw SQL(`ANY(:ids)`) 폴백.
    - 빈 universe면 DB 접근 없이 빈 payload 해시 반환.
    - ohlcv에 `updated_at`이 없으므로 `MAX(time)`을 프록시로 사용 (UPSERT로 time이 전진).
  - `is_stale(run_row, session) -> bool` 신규
    - 저장된 `data_hash`가 NULL이면 무조건 STALE.
    - `run_row.universe` JSONB에서 asset_id 추출 (int 또는 `{asset_id: ...}` 모두 허용).

- `projects/stock-backtest/src/stock_backtest/backtest/run_store.py` (신규)
  - `save_run(session, config, result, strategy_name, data_hash, code_hash) -> int`
    - `insert_run` → `bulk_insert_equity` → `bulk_insert_trades` → `insert_metrics` 순.
    - `metrics.performance.compute_all(equity, trades)` 호출 후 metric 테이블 기록.
    - equity row마다 running-max 기반 drawdown 계산해 함께 저장.
    - `result.run_hash`가 None이면 `compute_run_hash`로 재계산.
    - universe JSONB는 `[{asset_id, symbol, market, currency}, ...]` 형태로 저장.
  - `find_cached_run(session, run_hash) -> BacktestRun | None`
  - `load_run(session, run_id) -> (BacktestRun, pd.Series equity, list[trade dicts], dict metrics)`

- `projects/stock-backtest/src/stock_backtest/data/repository.py` (additive)
  - import에 `BacktestRun/Equity/Trade/Metric` 추가.
  - `insert_run(session, **fields) -> int`
  - `bulk_insert_equity(session, run_id, rows) -> int`
  - `bulk_insert_trades(session, run_id, rows) -> int`
  - `insert_metrics(session, run_id, metrics_dict) -> int`
    - NaN/inf 값은 자동 스킵(Postgres double precision 컬럼 보호).
  - `get_run_by_hash(session, run_hash) -> BacktestRun | None`

- `projects/stock-backtest/tests/test_run_store.py` (신규, 16 테스트)

## 엔진 수정 여부

엔진(`engine.py`)에 `run_with_cache` 등 추가 엔트리 함수는 **추가하지 않았다**.
동일 프로젝트 내 다른 Coder가 `engine.py`를 수정 중일 수 있어 충돌을 피했다.
사용자는 외부에서 다음 흐름을 구성하면 된다:

```python
from stock_backtest.backtest.cache import compute_run_hash, compute_data_hash, compute_code_commit_hash, is_stale
from stock_backtest.backtest.run_store import find_cached_run, save_run, load_run

run_hash = compute_run_hash(strategy_name, params, [s.symbol for s in universe],
                            (start, end), base_ccy)
cached = find_cached_run(session, run_hash)
if cached and not is_stale(cached, session):
    run_row, equity, trades, metrics = load_run(session, cached.run_id)
else:
    result = engine.run(config, strategy)
    data_hash = compute_data_hash(session, [s.asset_id for s in universe])
    code_hash = compute_code_commit_hash()
    run_id = save_run(session, config, result, strategy_name, data_hash, code_hash)
```

## 테스트 결과

`pytest tests/test_run_store.py -v` → 16/16 PASS
- compute_run_hash 결정론/입력변경시 변화 (2건)
- compute_code_commit_hash: 실제 git, FileNotFoundError, non-zero returncode (3건)
- compute_data_hash: max_time 변경, count 변경, 입력 순서 불변, 빈 universe (4건)
- is_stale: 해시 다름/같음/NULL/dict universe (4건)
- save_run: 모든 repository insert 호출 검증 (1건)
- find_cached_run: hit/miss (2건)

프로젝트 전체 `pytest -q` → 101 passed.

## 이슈/블로커

없음.
