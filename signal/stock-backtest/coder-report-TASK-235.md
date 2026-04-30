---
agent: coder
task_id: TASK-235
status: DONE
timestamp: 2026-04-30T15:30:00
---

## 결과 요약

`api/assets.py:85-86` 의 `PykrxSource() if market == "KR" else YfinanceSource()` 와 `scheduler/cron_jobs.py:48-52` 의 `sources_by_market` dict 가 동일한 라우팅 로직을 두 곳에 중복 보유하던 문제를 단일 factory 함수 `get_source_for_market` 로 통합했다. 신규 시장 추가 시 `app/data/sources/__init__.py` 의 함수 한 곳만 수정하면 양쪽이 동시에 반영된다.

## 변경 사항

### 1) Factory 함수 신규 추가
`backend/app/data/sources/__init__.py` (신규 함수, 기존 28줄 짧은 파일이라 별도 `factory.py` 신설 대신 `__init__.py` 에 추가):

```python
def get_source_for_market(
    market: str,
    *,
    yfinance: YfinanceSource,
    pykrx: PykrxSource,
) -> DataSource:
    """KR → pykrx, US/CRYPTO → yfinance. 알 수 없는 market 은 ValueError."""
    if market == "KR":
        return pykrx
    if market in ("US", "CRYPTO"):
        return yfinance
    raise ValueError(f"unknown market: {market!r}")
```

키워드 인자로 source 인스턴스를 주입받아 lifecycle 정책 (per-call vs 싱글톤) 은 호출자가 결정하도록 했다. 테스트 mock 주입에도 친화적.

`__all__` 에 `get_source_for_market` 추가, `app/data/__init__.py` 의 re-export 에도 추가.

### 2) `api/assets.py` 호출부 교체
`_RoutingValidator.__init__` 내부 인라인 if-else 를 factory 호출로 교체. 매번 인스턴스 생성하던 패턴은 그대로 유지 (Manager 지시: 별도 리팩토링 안 함):

```python
def __init__(self, market: str):
    self._source = get_source_for_market(
        market,
        yfinance=YfinanceSource(),
        pykrx=PykrxSource(),
    )
```

### 3) `cron_jobs._run_market_backfill` 호출부 교체
`sources_by_market` dict + 미지 market 체크 로직을 factory 호출 + `try/except ValueError` 로 교체. 미지 market 처리 동작 유지 (logger.error 후 return):

```python
try:
    source = get_source_for_market(
        market,
        yfinance=YfinanceSource(),
        pykrx=PykrxSource(),
    )
except ValueError:
    logger.error("cron: unknown market=%s, skip", market)
    return
filtered_sources: dict[str, DataSource] = {market: source}
```

## 변경된 파일

- `projects/stock-backtest/backend/app/data/sources/__init__.py` (수정 — factory 함수 신규 추가, `__all__` 갱신)
- `projects/stock-backtest/backend/app/data/__init__.py` (수정 — re-export 추가)
- `projects/stock-backtest/backend/app/api/assets.py` (수정 — `_RoutingValidator.__init__` factory 호출로 교체, import 추가)
- `projects/stock-backtest/backend/app/scheduler/cron_jobs.py` (수정 — `_run_market_backfill` factory 호출로 교체, import 추가)

## 추가/변경된 public 메서드 시그니처
- 신규: `app.data.sources.get_source_for_market(market: str, *, yfinance: YfinanceSource, pykrx: PykrxSource) -> DataSource`

(public 함수이며 `app.data.sources` 와 `app.data` 양쪽 `__all__` 에 등록.)

## DoD 검증

1. 신규 시장 추가 시 한 군데 (factory 함수) 만 수정해도 양쪽 호출자 동작: 충족. 양쪽 모두 factory 를 호출하므로 분기 로직이 한 곳에 응집.
2. `pytest tests/ --ignore=tests/api/test_api_contract.py --ignore=tests/e2e -x` PASS: **123 passed, 2 warnings in 5.52s**. Phase 1 baseline = 123 passed 와 정확히 일치 (회귀 0).
3. ruff/black: 프로젝트 root, backend/ 어디에도 `pyproject.toml`, `ruff.toml`, `.ruff.toml` 부재. 적용 대상 없음.
4. backend venv 로 테스트 통과 확인 (`/home/jai/pa/stock-backtest/projects/stock-backtest/.venv/bin/python -m pytest`).

추가로 factory 함수 자체를 smoke test:
```
KR  → PykrxSource    : OK (identity 일치)
US  → YfinanceSource : OK
CRYPTO → YfinanceSource : OK
XX  → ValueError    : OK (market 코드 메시지 포함)
```

## 행동 변화 검증 (no behavior regression)

- `_RoutingValidator` 호출 경로: `AssetCreate.market` 은 Pydantic `Market = Literal["KR","US","CRYPTO"]` 로 사전 검증되므로 미지 market 이 도달하지 않는다 (`backend/app/domain/asset/entity.py:15`). 따라서 factory 의 `ValueError` 는 HTTP 경로에서 트리거 불가 — 사실상 동작 동일. 단 fail-fast 로 더 안전.
- `_run_market_backfill` 호출 경로: 기존 `if market not in sources_by_market: logger.error; return` 시멘틱을 `try/except ValueError → logger.error; return` 으로 보존.

## 만지지 않은 파일 (지시 준수)
- `backend/app/data/sources/{yfinance_source.py, pykrx_source.py, _helpers.py, base.py}`: 동시 진행 중인 다른 Coder 영역이라 미터치.
- `frontend/`: TASK-237 영역, 미터치.
- `backend/tests/`: Tester 전용 디렉토리, 미터치.

## 이슈/블로커
없음.

## 다음 제안
- `_RoutingValidator.__init__` 가 호출마다 `YfinanceSource()` + `PykrxSource()` 를 새로 생성한다 (assets.py L88-93). 이는 기존 패턴을 그대로 유지한 것 (Manager 지시: 별도 리팩토링 안 함). 향후 source 인스턴스 lifecycle 을 개선한다면 `app.state` 싱글톤 + FastAPI `Depends` 로 주입하도록 별도 태스크로 분리하길 권장한다 (factory 시그니처는 이미 이를 지원).
- cron_jobs 도 동일하게 잡 발화마다 source 인스턴스를 생성한다. APScheduler lifespan 내 싱글톤 보관이 가능하면 동일하게 분리 가능.
- 단위 테스트 신규 추가는 본 태스크 범위 외 (Tester 영역). 필요 시 Manager 가 후속 Tester 태스크로 등록할 것.
