---
task_id: TASK-304
agent: coder
status: DONE
date: 2026-05-12
---

# TASK-304 — 정규화 도메인 (normalization.py — rebase=100, equal weighting)

## 산출물

### 신규 파일
- `projects/stock-backtest/backend/app/domain/themes/normalization.py` (155 줄)
- `projects/stock-backtest/backend/tests/domain/themes/test_normalization.py` (8 테스트)

### 수정 파일
- `projects/stock-backtest/backend/app/domain/themes/__init__.py` — normalization 4 함수 re-export 추가 (`aggregate_equal_weighted`, `compute_theme_aggregate`, `rebase_multi_series`, `rebase_series`).
  - 주의: 파일 상단 line 1 의 `from app.domain.engine import dummy  # TEMP-TASK-309-VIOLATION-PROBE` 는 TASK-309 (도메인 격리 테스트) 의 의도적 violation probe 로, 본 태스크에서 건드리지 않음.

## 함수 시그니처

```python
def rebase_series(prices: pd.Series, base_value: Decimal = Decimal("100")) -> pd.Series
def rebase_multi_series(prices_df: pd.DataFrame, base_value: Decimal = Decimal("100")) -> pd.DataFrame
def aggregate_equal_weighted(prices_df: pd.DataFrame) -> pd.Series
def compute_theme_aggregate(
    prices_df: pd.DataFrame,
    weighting: Literal["equal", "market_cap"] = "equal",
    market_cap_df: pd.DataFrame | None = None,
) -> pd.Series
```

## Coder 결정 사항

### 1) 첫 유효값이 0 인 경우 → ValueError
- 태스크 본문: "ValueError 또는 NaN 시리즈 반환 (Coder 결정 + report 명시)"
- **선택: ValueError**
- 이유: rebase=100 의 수학적 의미상 0 으로 나눌 수 없음. NaN 시리즈로 강등하면 호출자가 "데이터 없음 (all NaN)" 과 "0 가격 결함" 을 구별하지 못함. 0 가격 자산은 입력 데이터 결함이므로 호출자 (API 레이어, TASK-305) 가 사전 필터해야 한다는 명확한 신호를 fast-fail 로 전달한다.

### 2) Decimal vs float
- 태스크 본문: "pandas 시리즈는 float 으로 처리하되 base_value 만 Decimal 받아서 float 으로 변환. 정밀도 손실 우려 시 Decimal 시리즈 유지 (메모리 비용 ↑). Coder 결정 + report 명시."
- **선택: base_value 는 Decimal 인자, 내부 연산은 float64**
- 이유:
  1. pandas Series.dtype=object(Decimal) 산술은 Python 루프로 떨어져 100~1000x 느림. NaN 처리/`.mean(skipna=True)` 호환성도 떨어짐.
  2. 정규화 차트는 표시용 (소수점 둘째자리 % 단위). float64 의 ~15 유효숫자 정밀도면 차트 정확도 충분.
  3. 백테스트 회계 (`engine.py`) 의 Decimal 정밀도는 **불변** — 본 모듈은 백테스트 트랙과 도메인 격리되어 있어 회계에 영향 없음.

### 3) market_cap weighting 실제 구현 추가
- 태스크 본문: "weighting='market_cap' and market_cap_df is not None → 실제 시가총액 가중 평균 구현 (Phase 2.2 에서 활성화)"
- 본 함수에 가중 평균 본체를 구현해 두었다. 인덱스/컬럼 정렬 (`reindex`) 후 일자별 분자/분모 합산. 분모 0 또는 NaN 행은 NaN. Phase 2.2 에서 API 가 market_cap_df 를 넘기면 즉시 활성화됨.
- 단, 단위 테스트는 placeholder 동작 (NotImplementedError) 만 검증 (태스크 요구 8건의 마지막). 실제 구현 검증은 Phase 2.2 통합 시점에 추가 예정.

## DoD 검증

| DoD | 결과 | 명령 |
|-----|------|------|
| (a) 단위 테스트 8건 PASS | **PASS** 8/8 | `../.venv/bin/python -m pytest tests/domain/themes/test_normalization.py -q` → `8 passed, 1 warning in 0.31s` |
| (b) 수학적 성질 | **PASS** | rebase 첫 유효값 == base_value (test 1·2·4), equal aggregate[i] == mean(dropna()) (test 5·6) |
| (c) 도메인 순수성 | **PASS** | `grep -nE "^(from\|import) (sqlalchemy\|fastapi\|requests\|httpx\|yfinance\|pykrx\|app\.data\|app\.api\|app\.services)" app/domain/themes/normalization.py` → exit=1 (0 hit). 허용 import 만: `decimal`, `typing`, `pandas` |
| (d) import 무결성 | **PASS** | `../.venv/bin/python -c "from app.domain.themes.normalization import rebase_series, rebase_multi_series, aggregate_equal_weighted, compute_theme_aggregate"` → `import OK` |
| (e) 회귀 0 | **PASS** | `pytest tests/domain/ -q --ignore=tests/domain/themes/test_normalization.py` → `50 passed, 1 warning in 0.48s` |

## 단위 테스트 8건 (요약)

1. `test_rebase_series_basic` — [100, 110, 121] → [100, 110, 121]
2. `test_rebase_series_with_leading_nan` — [NaN, NaN, 50, 60, 75] → [NaN, NaN, 100, 120, 150]
3. `test_rebase_series_all_nan` — all NaN → all NaN (예외 없음)
4. `test_rebase_multi_series_independent_columns` — 2 컬럼 각각 독립 rebase
5. `test_aggregate_equal_weighted_basic` — [100, 200, 300] 행 → 200
6. `test_aggregate_equal_weighted_skipna` — 일부 NaN 행 평균, 전체 NaN 행 NaN
7. `test_aggregate_empty_df` — 빈 DataFrame → 빈 Series
8. `test_compute_theme_aggregate_market_cap_not_implemented` — market_cap + market_cap_df=None → NotImplementedError

## 후속 의존

- **TASK-305** (정규화 차트 API) 는 본 모듈의 `rebase_multi_series` + `compute_theme_aggregate(weighting="equal")` 를 직접 호출.
- **Phase 2.2** 진입 시: 시가총액 데이터 어댑터 (data 레이어) 추가 후 `compute_theme_aggregate(weighting="market_cap", market_cap_df=...)` 활성화. 본 함수의 가중 평균 본체는 이미 구현되어 있음.

## 이슈/블로커

없음.
