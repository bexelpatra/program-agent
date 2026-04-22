# Coder Report — TASK-029

- Task: 웹 페이지 (b) 계절성 분석
- Status: DONE
- Target file: `projects/stock-backtest/src/stock_backtest/web/pages/seasonality.py`

## 구현 요약

`web/pages/seasonality.py` 를 placeholder 에서 완전 구현으로 덮어썼다.

### 레이아웃
- 자산 Dropdown (단일, active assets, 페이지 로드 콜백으로 채움)
- 기간 `DatePickerRange` (default: 최근 10년)
- 분석 카테고리 `RadioItems` (7종: monthly / day_of_week / sell_in_may /
  halloween / presidential_term / fomc / earnings_season)
- "분석 실행" 버튼
- 결과 영역: 상태 배너 + Plotly 차트 + 유의성 `DataTable`
- `dcc.Loading` 으로 긴 쿼리 대기 표시

### 콜백
1. `_populate_asset_options` — 페이지 최초 렌더 시 `list_active_assets`
   로 Dropdown 채움. DB 실패 시 빈 리스트.
2. `_run_analysis` — "분석 실행" 클릭 → `_run_analysis_impl`:
   - `OhlcvRepository.get_range(asset_id, start, end)` 로 adj_close 시계열
     로드 (adj_close 없으면 close 사용).
   - `analysis.seasonality.daily_returns(prices)` 계산.
   - 선택된 카테고리에 대해 `CATEGORY_RUNNERS[category](returns)` 실행.

### 카테고리 러너 (`CATEGORY_RUNNERS`)
- `_run_monthly`        — `monthly_effect` 바차트 + 각 월 vs 그 외 월
                          `welch_t_test` → `annotate_significance`.
- `_run_day_of_week`    — `day_of_week_effect` 바차트 + 동일한 Welch 비교.
- `_run_sell_in_may`    — `sell_in_may` 연환산 바차트 + 전체 표본 Welch.
- `_run_halloween`      — `halloween_indicator` 연도별 halloween vs B&H
                          그룹드 바차트 + 초과수익 평균/승률 요약.
- `_run_presidential_term` — `market_events` 에서 `(US,
  presidential_election)` 로드 → `presidential_term_year_effect` +
  연차별 `bootstrap_ci` (n_resamples=2_000) 를 계산해 95% CI 에러바.
  이벤트 없으면 친화적 안내 메시지.
- `_run_fomc`           — `(US, fomc)` 로드 → `fomc_week_effect` + FOMC
                          주간 vs 그 외 Welch t-test.
- `_run_earnings_season` — `1/4/7/10월 15일` ±5 거래일을 피크로 사용한
                          `earnings_season_effect` + Welch.

### 데이터 부족 경고
- 대통령 임기 분석은 총 샘플이 ~4년치(1008일) 미만이면 "데이터 포인트가
  적어 통계력이 약합니다" 경고 표시 (한국 대선/총선 등에도 동일 패턴
  적용 가능). 이벤트 레코드 0건이면 안내 메시지와 함께 빈 차트 반환.

### 에러 처리
- DB 세션 실패, 빈 가격, 기간 역전 등은 모두 `ValueError/RuntimeError`
  로 던지고, 상위 콜백에서 친화 메시지 + traceback 블록으로 렌더.

## 검증
- `python -c "import ast; ast.parse(...)"` → 통과.
- import/런타임 실행은 DB 연결이 필요하므로 수행하지 않았다 (해당 태스크는
  페이지 모듈 구현만 담당).
- `backtest.py` 의 콜백 패턴 (`dcc.Loading`, 상태/결과 분리, 에러 박스)
  을 동일하게 따랐다.

## 타입/문서화
- 모든 공개/내부 헬퍼에 한국어 docstring + 타입힌트 부여.
- `from __future__ import annotations` 로 포스트포닝된 어노테이션 사용.

## 변경 파일
- `projects/stock-backtest/src/stock_backtest/web/pages/seasonality.py`
  (전체 재작성)

다른 파일은 수정하지 않았다.
