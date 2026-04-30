---
agent: coder
task_id: TASK-213
status: DONE
timestamp: 2026-04-30T10:30:00
---

## 결과 요약

신규 자산 백필 시작일을 고정 20년이 아니라 **소스가 알려주는 가장 오래된 데이터 날짜**로 사용하도록 정책 변경. `DataSource` Protocol 에 `earliest_available(symbol) -> date | None` 메서드 추가, `YfinanceSource`/`PykrxSource` 구현, `pipeline._resolve_start` 가 신규 자산일 때 이 메서드를 우선 호출하고 None 이면 기존 `DEFAULT_MAX_LOOKBACK_DAYS` fallback. `pipeline.backfill_asset` 호출부에서 source/symbol 전달.

## 변경된 파일

- `backend/app/data/sources/base.py` (수정) — `DataSource.earliest_available(symbol) -> date | None` Protocol 메서드 추가.
- `backend/app/data/sources/yfinance_source.py` (수정) — `YfinanceSource.earliest_available()` 구현 (period='max', 빈 결과/예외 → None + warning).
- `backend/app/data/sources/pykrx_source.py` (수정) — `PykrxSource.earliest_available()` 구현 (1995-01-01 ~ today 한 번 조회로 첫 행 추출).
- `backend/app/data/pipeline.py` (수정):
  - `_resolve_start` 시그니처 확장 — `*, source: DataSource | None = None, symbol: str | None = None` 키워드 전용 옵셔널.
  - 신규 자산 분기에서 `source.earliest_available(symbol)` 우선 시도, None/예외 시 `DEFAULT_MAX_LOOKBACK_DAYS` fallback.
  - `backfill_asset` 호출부 `_resolve_start(... source=source, symbol=asset.symbol)` 로 전달.
  - `DEFAULT_MAX_LOOKBACK_DAYS` 코멘트를 "fallback 상한" 으로 갱신.
- `backend/tests/data/__init__.py` (신규) — 빈 패키지 마커.
- `backend/tests/data/test_pipeline.py` (신규) — `_resolve_start` 단위 테스트 6 케이스:
  1. earliest_available 결과 있을 때 그 날짜 사용
  2. earliest_available None → DEFAULT_MAX_LOOKBACK_DAYS fallback
  3. earliest_available 예외 → 흡수 후 fallback
  4. source/symbol 미제공 시 역호환 fallback
  5. 기존 자산 (latest 있음) → latest+1, earliest_available 호출 안 함
  6. custom max_lookback_days 적용 확인

## 변경된 public API

`app.data.sources.base.DataSource` Protocol:
- `earliest_available(symbol: str) -> date | None` (신규)

`app.data.pipeline._resolve_start` (모듈 private 이지만 시그니처 변경):
- `_resolve_start(latest, end, max_lookback_days, *, source=None, symbol=None) -> date`
- 신규 인자는 키워드 전용 + 옵셔널 → 기존 호출자 영향 없음.

## 테스트 실행 결과

```
/home/jai/pa/stock-backtest/projects/stock-backtest/.venv/bin/python -m pytest tests/regression/ tests/golden/ tests/data/ -v
68 passed, 2 warnings in 3.10s
```

- 신규 6 테스트 모두 통과.
- 기존 회귀 (lookahead, calendar, cash_by_ccy) 49 테스트 통과 — 회귀 0.
- 골든 스냅샷 9 케이스 통과 — 엔진 결과 영향 없음 (예상대로 fixture 기반).

## 이슈/블로커

없음.

### 충돌 회피 메모

태스크 명세에 따라 **본 태스크는 earliest_available 메서드 추가만 담당**. 다음 항목은 **건드리지 않음** (TASK-214 범위):
- `yfinance_source.fetch_ohlcv` 의 `auto_adjust=False` (그대로 유지).
- `pykrx_source` L100-102 "MVP 비조정 종가" 코멘트 (그대로 유지).

`earliest_available` 내부에서 yfinance `period='max'` 호출 시 `auto_adjust=False` 를 명시 — fetch_ohlcv 와 동일 정책으로 통일했으나, 이 옵션은 `period='max'` 에서 첫 인덱스 추출에만 영향이 없으므로 (어차피 가격 값을 사용하지 않음) TASK-214 가 fetch_ohlcv 를 `auto_adjust=True` 로 바꿀 때 함께 정리 가능.

### Coder agents.md 규정 충돌 메모

agents/coder.md L198: "tests/ 디렉토리의 파일을 수정하지 않는다 (Tester 전용)" 규정과 본 태스크 명세 "테스트 추가" 가 충돌. **태스크 명세 (Manager 지시) 가 명시적으로 테스트 작성을 요구**했으므로 명세 우선으로 처리. 향후 동일 패턴이면 Manager 가 Tester 에 분리 위임할지 정책 확정 필요.

## 다음 제안

1. **운영 액션 (TASK-216 범위)**: BTC-USD 같은 기존 자산은 `latest_time` 이 이미 있어 earliest_available 호출이 발생하지 않음. 기존 자산을 새 정책으로 재백필하려면 사용자가 ohlcv 를 truncate 하거나, 별도 "재백필" 명령(예: `--force-from-earliest` 플래그)이 필요. 현 파이프라인에는 없음.
2. **earliest_available 캐싱**: 자산 등록 시 1회만 호출하고 `assets.start_date` 에 캐시하면 매 백필 잡 실행 시 외부 호출 부담 없음. 현 구조는 신규 자산일 때만 호출되므로 사실상 1회성이지만, retry 시 매번 호출되는 점은 향후 개선 여지.
3. **pykrx earliest 조회 비용**: 1995-01-01 부터 today 까지 한 번 조회는 KR 거래일 ~7800 행. 종목당 1회만 발생하므로 부담 적음. 다만 자산 100개 이상 신규 등록 시 (일괄 시드) 누적 시간 고려 필요 — 현재 _rate_limit 100ms × 100 = 10s 추가.

## 회귀 의도 commit msg

`TASK-213: 백필 시작일을 earliest_available 기반으로 — DataSource Protocol 확장`
