# Coder Report - TASK-025

## Task
- Task ID: TASK-025
- Title: market_events seed + 이벤트 기반 계절성 분석
- Status: DONE

## 산출물

### 1. `projects/stock-backtest/scripts/seed_market_events.py` (신규)
- `scripts/` 디렉토리 생성 후 배치.
- 이벤트 빌더 함수: `us_presidential_elections`, `us_midterm_elections`,
  `fomc_events`, `earnings_season_peaks`, `kr_presidential_elections`,
  `kr_general_elections`.
- `EventRow` dataclass로 (country, type, event_date, meta) 구조화.
- 삽입 로직: `market_events` 테이블에 `(country, type, event_date)`
  UNIQUE 제약이 없기 때문에 **SELECT-then-INSERT dedup** 방식 사용
  (세션 시작 시 기존 튜플 집합을 로드해 신규 행만 add). 재실행 시 멱등.
- `if __name__ == "__main__":` 블록에서 `get_session()` 사용해 삽입 및
  카운트 요약 출력.

### 2. `projects/stock-backtest/src/stock_backtest/analysis/political_cycle.py` (신규)
- 공개 함수 4개:
  - `presidential_term_year_effect(returns, elections)` → term_year(1~4)
    × [mean_daily, annualized, count, win_rate]
  - `election_year_effect(returns, elections, midterms)` → year_type
    (presidential/midterm/non_election) × 동일 컬럼
  - `fomc_week_effect(returns, fomc_dates)` → week_type
    (fomc_week/other_week) × 컬럼 + Welch `t_stat`
  - `earnings_season_effect(returns, earnings_dates, window=5)` → bucket
    (in_window/out_window) × 컬럼 + Welch `t_stat`
- 모든 함수 DatetimeIndex 검증, NaN dropna, docstring 에 입출력 명시.
- `elections` 등 이벤트 인자는 DataFrame(`event_date` 컬럼) / DatetimeIndex /
  Iterable 을 모두 허용하도록 `_to_datetime_index()` 로 정규화.
- `seasonality.py` 는 수정하지 않음.

### 3. `projects/stock-backtest/src/stock_backtest/analysis/__init__.py` (수정)
- 신규 4개 함수 export 추가.

## 이벤트 개수 확인 (seed 빌더 호출 결과)

```
KR:general_election                        4
KR:presidential_election                   3
US:earnings_season                       104
US:fomc                                  124
US:midterm_election                       11
US:presidential_election                  12
TOTAL                                    258
```

- US 대선: 1980~2024 4년 간격 = 12개 (요구 "11개" 샘플 대비 실제 12개가
  맞음; 1980 포함 1984,1988,...,2024 = 12)
- US 중간선거: 1982~2022 4년 간격 = 11개 (요구 충족)
- FOMC: 2000~2020 근사 (21년×4) = 84, 2021~2025 실회의 40 → 총 124
  (요구: "최근 5년 ≥ 40회" 충족)
- 실적시즌: 2000~2025 × 4개월 = 104 (요구 "100+" 충족)
- KR 대선: 2012, 2017, 2022 = 3 (충족)
- KR 총선: 2012, 2016, 2020, 2024 = 4 (충족)

## Smoke test (합성 데이터, bdate 2000-01-01~2025-12-31)

```
=== presidential_term_year_effect ===
           mean_daily  annualized  count  win_rate
term_year                                         
1            0.000194    0.049983   1609  0.510255
2            0.000601    0.163467   1825  0.520548
3            0.000274    0.071477   1564  0.516624
4            0.000675    0.185323   1564  0.527494

=== election_year_effect ===
              mean_daily  annualized  count  win_rate
year_type                                            
presidential    0.000245    0.063676   1830  0.513661
midterm         0.000274    0.071477   1564  0.516624
non_election    0.000635    0.173503   3389  0.523753

=== fomc_week_effect ===
            mean_daily  annualized  count  win_rate    t_stat
week_type                                                    
fomc_week     0.001836    0.587576     50  0.600000  1.023144
other_week    0.000436    0.116185   6733  0.518788  1.023144

=== earnings_season_effect ===
            mean_daily  annualized  count  win_rate    t_stat
bucket                                                       
in_window     0.000250    0.064912   1144  0.525350 -0.752258
out_window    0.000487    0.130411   5639  0.518177  -0.752258
```

모든 함수가 정상 import 및 실행됨.

## 비고
- DB 실제 INSERT는 smoke test에 포함하지 않음 (DB 연결 불필요 환경에서
  import/로직만 검증). seed 스크립트는 `.env`에 `DATABASE_URL` 설정 후
  `python projects/stock-backtest/scripts/seed_market_events.py` 로 실행.
- FOMC 2000~2020 구간은 분기별 근사 (meta.approx=true), 2021~2025는 실
  회의일 (meta.approx=false). docstring 에 명시.

## 이슈/블로커
없음.
