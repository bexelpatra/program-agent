# Coder Report - TASK-024

- Task: 기본 계절성 분석 (월/요일/월말/Sell-in-May/Halloween)
- Status: DONE
- Date: 2026-04-14

## 구현 내용

`projects/stock-backtest/src/stock_backtest/analysis/seasonality.py` 신규 구현.
`projects/stock-backtest/src/stock_backtest/analysis/__init__.py` 에 퍼블릭 API 노출.

### 함수 목록 및 시그니처

| 함수 | 입력 | 반환 |
|------|------|------|
| `daily_returns(prices)` | `pd.Series` (DatetimeIndex, adj_close) | `pd.Series` (일별 단순수익률, 첫날 제거, name="return") |
| `monthly_effect(returns)` | `pd.Series` (DatetimeIndex, 일별 수익률) | `pd.DataFrame` index=1..12, cols=[mean, median, std, count, win_rate] |
| `day_of_week_effect(returns)` | 동상 | `pd.DataFrame` index=[Mon..Fri], cols=[mean, median, std, count, win_rate] |
| `month_edge_effect(returns, window=3)` | 동상 | `pd.DataFrame` index=[month_start, middle, month_end], cols=[mean, count, t_stat_vs_middle, t_stat_end_vs_start] |
| `sell_in_may(returns)` | 동상 | `pd.DataFrame` index=[may_oct, nov_apr], cols=[mean_daily, annualized, std_daily, count, win_rate] |
| `halloween_indicator(returns)` | 동상 | `pd.DataFrame` index=season_end_year, cols=[nov_apr_return, may_oct_return, halloween_return, buy_hold_return, excess_return] |

### 주요 설계 메모
- 모든 함수는 `pandas`/`numpy` 만 사용.
- 공용 내부 유틸 `_ensure_datetime_index` 로 DatetimeIndex 검증 (실패 시 `ValueError`).
- NaN 은 공통적으로 `dropna()` 후 집계. 월/요일별 win_rate = `(x > 0).mean()`.
- `month_edge_effect`: 거래일 기준 앞/뒤 window 일 구분. 작은 달에서 start/end 가 겹치면 end 우선. Welch t-통계 자체 구현 (scipy 미사용).
- `sell_in_may`: 연환산은 `(1+mean_daily)^252 - 1` 일별 복리 가정.
- `halloween_indicator`: Bouman & Jacobsen (2002) 정의에 맞춰 시즌 종료 연도(`season_end_year`) 기준 그룹핑. 11~12월은 다음 해로 이월. `halloween_return = nov_apr_return` (may_oct 현금=0), `buy_hold_return = (1+nov_apr)(1+may_oct)-1`, `excess_return = halloween - buy_hold`. 결측 시즌은 NaN 전파.

### 완료 조건 체크
- [x] seasonality.py 작성, `from stock_backtest.analysis import seasonality` import 성공
- [x] 각 함수가 DataFrame/Series 반환, 컬럼명 docstring 명시
- [x] DatetimeIndex 아님 → ValueError
- [x] `__init__.py` 퍼블릭 export
- [x] 모든 함수 docstring (입력·출력 스키마·계산 방식) 완비
- [x] 금지 영역(`tests/`, `ingestion/`, `strategies/`, task-board.md, architecture.md) 미수정

## 검증
합성 일별 가격 시계열(2018-01-01~2023-12-31, 영업일, seed=0)로 smoke test 수행.
- `daily_returns` 길이 1564
- `monthly_effect`/`day_of_week_effect` 정상 테이블
- `month_edge_effect` middle count=1132, start=end=216
- `sell_in_may` may_oct count=788, nov_apr count=776
- `halloween_indicator` season_end_year 별 5개 컬럼 정상
- `pd.Series([1,2,3])` 입력 시 ValueError 발생

## 블로커
없음.
