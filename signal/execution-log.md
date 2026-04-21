# Execution Log

## 2026-04-13T07:08:33
- command: `python -c "import pytest; print(pytest.__version__)" 2>&1`
- output:
```

```

## 2026-04-13T07:09:32
- command: `python -m pytest _test_memo.py -v 2>&1`
- output:
```

```

## 2026-04-13T07:10:27
- command: `python -m pytest _test_memo.py -v 2>&1 | tail -25`
- output:
```

```

## 2026-04-13T07:38:02
- command: `cd /home/jai/program-agent/projects/abc-english && pip list 2>/dev/null | grep -iE "pytest|requests|beautifulsoup|pydantic|tqdm" 2>/dev/null; echo "---"; python -c "import pytest; print(pytest.__version__)" 2>&1`
- output:
```

```

## 2026-04-13T07:41:21
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_collector.py -v 2>&1`
- output:
```

```

## 2026-04-13T11:48:51
- command: `pip list 2>/dev/null | grep -iE "spacy|pydantic|pytest|yaml"`
- output:
```

```

## 2026-04-13T11:50:33
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_transcriber.py -v 2>&1`
- output:
```

```

## 2026-04-13T11:50:34
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_comparator.py -v 2>&1`
- output:
```

```

## 2026-04-13T11:50:41
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_analyzer.py -v 2>&1`
- output:
```

```

## 2026-04-13T11:50:44
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_collector.py -v 2>&1 | tail -5`
- output:
```

```

## 2026-04-13T11:54:05
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_loader.py -v 2>&1`
- output:
```

```

## 2026-04-13T11:59:26
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_llm_analyzer.py -v 2>&1`
- output:
```

```

## 2026-04-13T12:02:21
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_cli.py -v 2>&1`
- output:
```

```

## 2026-04-13T12:03:19
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_integration.py -v 2>&1`
- output:
```

```

## 2026-04-13T12:46:25
- command: `cd /home/jai/program-agent/projects/abc-english && python -m pytest tests/test_llm_analyzer.py -v --tb=short 2>&1 | tail -30`
- output:
```

```

## 2026-04-13T12:47:12
- command: `python -m pytest tests/test_llm_analyzer.py -v --tb=short 2>&1 | tail -25`
- output:
```

```

## 2026-04-13T12:47:32
- command: `python -m pytest tests/test_llm_analyzer.py -v --tb=short 2>&1 | tail -15`
- output:
```

```

## 2026-04-14T01:59:04
- command: `cd /home/jai/program-agent/projects/abc-english && python -c "
from src import scheduler as s
from unittest.mock import patch
import datetime

settings = {'scheduler': {'enabled': True, 'time': '09:00', 'timezone': 'Asia/Seoul', 'weekdays_only': True, 'log_file': 'data/scheduler.log'}}

# Simulate saturday
class FakeDT(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime.datetime(2026, 4, 18, 9, 0, tzinfo=tz)  # Saturday

with patch('src.scheduler.datetime', FakeDT):
    out = s.run_job(settings, force_check_weekend=False)
    print('Saturday ->', out)
"`
- output:
```

```

## 2026-04-14T02:08:10
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_tax.py -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:12:12
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_calendar_guard.py -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:12:25
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_calendar_guard.py -v 2>&1 | tail -30`
- output:
```

```

## 2026-04-14T02:19:37
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_smoke.py -x -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:19:47
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_smoke.py -x -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:20:02
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_smoke.py -x -v 2>&1 | tail -30`
- output:
```

```

## 2026-04-14T02:23:45
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -c "import pytest, pandas, sqlalchemy; print('OK')" 2>&1`
- output:
```

```

## 2026-04-14T02:23:56
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_static_strategies.py -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:23:58
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_performance.py -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:24:10
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_static_strategies.py -v 2>&1 | tail -30`
- output:
```

```

## 2026-04-14T02:24:29
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_performance.py -v 2>&1 | tail -30`
- output:
```

```

## 2026-04-14T02:24:39
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_performance.py 2>&1 | tail -5`
- output:
```

```

## 2026-04-14T02:25:34
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_ingestion_pipeline.py -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:26:02
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_ingestion_pipeline.py -v 2>&1 | tail -40`
- output:
```

```

## 2026-04-14T02:30:24
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_momentum.py -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:30:32
- command: `cd /home/jai/program-agent/projects/stock-backtest && PYTHONPATH=src python -c "from stock_backtest.strategies.registry import discover_strategies, list_strategies; discover_strategies(); print(list_strategies())" && python -m pytest tests/ 2>&1 | tail -15`
- output:
```

```

## 2026-04-14T02:31:02
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_run_store.py -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:31:06
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest -q 2>&1 | tail -20`
- output:
```

```

## 2026-04-14T02:31:10
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_vaa_riskparity.py -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:31:49
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py -v 2>&1 | tail -100`
- output:
```

```

## 2026-04-14T02:32:13
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:33:35
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py -v 2>&1 | tail -30`
- output:
```

```

## 2026-04-14T02:33:52
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py -v 2>&1 | tail -40`
- output:
```

```

## 2026-04-14T02:34:58
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py -v 2>&1 | tail -25`
- output:
```

```

## 2026-04-14T02:36:05
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py tests/test_engine_smoke.py 2>&1 | tail -8`
- output:
```

```

## 2026-04-14T02:38:46
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py -v 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:39:13
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_regression.py tests/test_engine_smoke.py -v 2>&1 | tail -50`
- output:
```

```

## 2026-04-14T02:39:26
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_portfolio_fx.py tests/test_engine_regression.py -v 2>&1 | tail -40`
- output:
```

```

## 2026-04-14T02:39:50
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_engine_cushion.py tests/test_engine_regression.py tests/test_engine_smoke.py -v 2>&1 | tail -40`
- output:
```

```

## 2026-04-14T02:39:55
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/ 2>&1 | tail -15`
- output:
```

```

## 2026-04-14T02:40:16
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_strategy_integration.py -v 2>&1 | tail -100`
- output:
```

```

## 2026-04-14T02:40:23
- command: `cd /home/jai/program-agent/projects/stock-backtest && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_strategy_integration.py -v -p no:cacheprovider 2>&1 | tail -100`
- output:
```

```

## 2026-04-14T02:40:34
- command: `cd /home/jai/program-agent/projects/stock-backtest && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_strategy_integration.py -v -p no:cacheprovider 2>&1 | tail -60`
- output:
```

```

## 2026-04-14T02:43:13
- command: `ls /home/jai/program-agent/projects/stock-backtest/{pyproject.toml,setup.py,setup.cfg,conftest.py,pytest.ini} 2>&1 | head -10 && cat /home/jai/program-agent/projects/stock-backtest/pyproject.toml 2>/dev/null | head -50`
- output:
```

```

## 2026-04-14T02:44:44
- command: `cd /home/jai/program-agent/projects/stock-backtest && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_seasonality_stats.py -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:50:40
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_ingestion_e2e.py -v 2>&1 | tail -80`
- output:
```

```

## 2026-04-14T02:50:47
- command: `cd /home/jai/program-agent/projects/stock-backtest && python -m pytest tests/test_ingestion_e2e.py -v -p no:cacheprovider -p no:dash 2>&1 | tail -40`
- output:
```

```

## 2026-04-14T09:00:11
- command: `PYTHONPATH=src python -m pytest tests/ -x -q 2>&1 | tail -40`
- output:
```

```

## 2026-04-14T09:00:16
- command: `PYTHONPATH=src python -m pytest tests/ -x -q --ignore=tests/web 2>&1 | tail -30`
- output:
```

```

## 2026-04-14T09:00:19
- command: `PYTHONPATH=src python -m pytest tests/backtest -x -q 2>&1 | tail -25`
- output:
```

```

## 2026-04-14T09:00:23
- command: `PYTHONPATH=src python -m pytest tests/backtest/test_portfolio.py -x -q -p no:cacheprovider 2>&1 | tail -25`
- output:
```

```

## 2026-04-14T09:04:12
- command: `PYTHONPATH=src python -m pytest tests/test_engine_smoke.py tests/test_engine_regression.py tests/test_engine_cushion.py -x -q 2>&1 | tail -20`
- output:
```

```

## 2026-04-14T09:04:16
- command: `PYTHONPATH=src python -m pytest tests/test_engine_smoke.py tests/test_engine_regression.py tests/test_engine_cushion.py -x -q -p no:cacheprovider --no-header 2>&1 | grep -E "passed|failed|error" | tail -5`
- output:
```

```

## 2026-04-14T09:04:20
- command: `PYTHONPATH=src python -m pytest tests/test_engine_smoke.py -x -q --no-header -p no:cacheprovider 2>&1 | tail -10`
- output:
```

```

## 2026-04-15T06:20:38
- command: `cd /home/jai/program-agent/projects/stock-backtest && .venv/bin/python -m pytest --collect-only 2>&1 | tail -40`
- output:
```

```

## 2026-04-15T06:20:43
- command: `cd /home/jai/program-agent/projects/stock-backtest && ls .venv/bin/ | grep -i pytest; .venv/bin/pip list 2>/dev/null | grep -i pytest`
- output:
```

```

## 2026-04-15T06:20:51
- command: `cd /home/jai/program-agent/projects/stock-backtest && .venv/bin/pip list 2>&1 | grep -i pytest; which pytest; python3 -c "import pytest; print(pytest.__version__)" 2>&1`
- output:
```

```

## 2026-04-15T06:20:54
- command: `cd /home/jai/program-agent/projects/stock-backtest && PYTHONPATH=src .venv/bin/python -m pip install pytest 2>&1 | tail -5`
- output:
```

```

## 2026-04-15T06:20:59
- command: `cd /home/jai/program-agent/projects/stock-backtest && .venv/bin/python -m pytest --collect-only 2>&1 | tail -50`
- output:
```

```

## 2026-04-15T06:21:58
- command: `cat >> /home/jai/program-agent/signal/stock-backtest/done-log.md <<'EOF'

- TASK-102 DONE (coder): 불필요 전략 + 테스트 삭제.
  전략 9개(momentum, dual_momentum, risk_parity, vaa, moving_average/{crossover,multi_crossover,seasonal,_common}, permanent) + 테스트 4개(test_momentum, test_vaa_riskparity, test_static_strategies, test_strategy_integration) 제거.
  `simple.py` 에서 `_common.rolling_mean` 의존을 내부 인라인으로 전환(_common.py 삭제 대응).
  `__init__.py` 3개의 docstring 을 V2 범위로 정리.
  검증: pytest --collect-only 118 수집 통과, list_strategies() 가 ['fixed_weight', 'simple_moving_average'] 2개 정확.
  메모: Tester 발견 — venv 에 pytest 미설치 상태였음 → TASK-103 dev 의존성 정비 범위로 자연히 흡수.
EOF`
- output:
```

```

## 2026-04-15T06:24:47
- command: `cat >> /home/jai/program-agent/signal/stock-backtest/done-log.md <<'EOF'

- TASK-103 DONE (coder): CLI/문서/의존성 정리.
  `scripts/run_web.sh` 삭제. README.md 전면 재작성(Dash/웹 섹션 제거, web/ 디렉토리 트리 제거, V2 Reset 안내 추가).
  requirements.txt 에서 dash/plotly 제거(plotly 코드 사용 0건 grep 확인).
  requirements-dev.txt 에 pytest-asyncio 추가(TASK-102 Tester 지적 반영).
  docs/cron.md / pyproject.toml 에는 기존 관련 언급 없음 확인, 변경 없음.
  검증: pip install --dry-run PASS, import stock_backtest PASS, grep 잔존 1건은 V2 Reset 진행 안내로 의도된 허용.

## Phase 1 완료 (2026-04-15)

V1 잔재 정리 완료. Phase 2 재구축 진입 가능. 다음은 TASK-111(Cash 타입 도입) — 의존성 없음, 독립 실행 가능.
EOF`
- output:
```

```

