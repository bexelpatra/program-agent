---
agent: coder
task_id: TASK-040
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약

이동평균(Moving Average) 전략 첫 세트를 `strategies/dynamic/moving_average/`
디렉토리에 구현했다. 공통 헬퍼 모듈(`_common.py`)에 rolling_mean /
crossover_signal / seasonal_mask / combine_signals 를 응집했고,
두 전략(`MovingAverageCrossover`, `SeasonalMovingAverage`) 은 base
`Strategy` 인터페이스 + pydantic `StrategyParams` + `@register`
데코레이터 패턴을 기존 동적 전략(`dual_momentum.py`, `momentum.py`,
`vaa.py`) 과 동일하게 따랐다. registry `discover_strategies()` 가
`pkgutil.walk_packages` 로 하위 패키지를 자동 스캔함을 실측 확인했다.

## 변경된 파일

- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/__init__.py` (신규)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/_common.py` (신규)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/crossover.py` (신규)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/seasonal.py` (신규)

## 공개 API / params_schema

### `_common` 공개 함수

- `rolling_mean(prices: pd.Series, window: int) -> pd.Series`
- `crossover_signal(fast: pd.Series, slow: pd.Series) -> pd.Series[int]`
  (NaN→0, **호출 측에서 `.shift(1)` 적용 권장**)
- `seasonal_mask(index: pd.DatetimeIndex, mode: Literal["halloween","sell_in_may","presidential_term","custom_months"], custom_months: list[int] | None = None, election_dates: list[date] | None = None) -> pd.Series[int]`
- `combine_signals(ma: pd.Series, seasonal: pd.Series, mode: Literal["and","weighted"], alpha: float) -> pd.Series[float]`

### `MovingAverageCrossoverParams`

```
risky_symbol: str                # required
safe_symbol:  str                # required, must differ from risky
fast_window:  int = 50           # > 0
slow_window:  int = 200          # > fast_window
```

registry name: `"moving_average_crossover"`

### `SeasonalMovingAverageParams`

```
risky_symbol:      str
safe_symbol:       str
fast_window:       int = 50
slow_window:       int = 200
seasonality_mode:  Literal["halloween","sell_in_may","presidential_term","custom_months"]
combine_mode:      Literal["and","weighted"] = "and"
alpha:             float = 0.5       # [0, 1]
custom_months:     list[int] | None = None   # required when mode="custom_months"
election_dates:    list[str] | None = None   # ISO-date strings, required when mode="presidential_term"
```

registry name: `"seasonal_moving_average"`

**설계 결정 — election_dates 주입 방식**:
base `Strategy` 인터페이스는 DB repository 주입을 노출하지 않는다.
기존 전략 패턴을 답습하여 `election_dates` 를 params 필드(ISO 문자열
리스트)로 두었다. 웹/엔진 레이어가 `market_events`
(`country='US', type='presidential_election'`) 테이블에서 미리
로드해 파라미터 인스턴스화 시점에 주입하면 된다. 전략 내부에서는
`datetime.fromisoformat` 로 파싱하여 `_common.seasonal_mask` 에
`list[date]` 로 전달한다.

## 수행 단계

1. `architecture.md`, base `Strategy`, 기존 동적 전략
   (`dual_momentum.py`, `momentum.py`, `vaa.py`), `registry.py` 를
   읽어 인터페이스 규약·파라미터 주입·등록 패턴을 확인.
2. `moving_average/` 패키지 생성 + `__init__.py` 작성.
3. `_common.py` 에 4개 헬퍼 구현. `crossover_signal` 은 NaN→0
   보장, look-ahead 방지를 위한 `.shift(1)` 사용 규약을 docstring
   으로 문서화.
4. `crossover.py` — `MovingAverageCrossover` 구현. `model_validator`
   로 `fast < slow` 및 risky≠safe 검증. `generate_weights` 는
   리밸런싱일 이전 거래일의 signal 을 pad 조회.
5. `seasonal.py` — `SeasonalMovingAverage` 구현. `combine_signals`
   결과에서 `w` 산출 후 `{risky: w, safe: 1-w}` 배분.
6. 문법 검증 (`ast.parse`) → 통과.
7. `discover_strategies()` 호출 → `moving_average.*` 네 모듈 모두
   import 성공, registry 에 두 전략명 등재 확인.
8. 합성 SPY 가격 픽스처로 스팟체크 수행 (아래 로그).

## registry 등록 로그

```
imported(ma): ['stock_backtest.strategies.dynamic.moving_average',
               'stock_backtest.strategies.dynamic.moving_average._common',
               'stock_backtest.strategies.dynamic.moving_average.crossover',
               'stock_backtest.strategies.dynamic.moving_average.seasonal']
list: ['dual_momentum', 'fixed_weight', 'momentum', 'moving_average_crossover',
       'permanent', 'risk_parity', 'seasonal_moving_average', 'vaa']
get_strategy('moving_average_crossover') = MovingAverageCrossover
get_strategy('seasonal_moving_average')  = SeasonalMovingAverage
```

`pkgutil.walk_packages` 가 하위 패키지를 자동 스캔함을 실증. registry
쪽은 전혀 건드리지 않았다.

## 스팟체크 결과

### 1) 이평선 골든/데드 크로스 (합성 SPY)

합성 가격: 50일 하락 100→60 → 200일 상승 60→200 → 150일 하락 200→120.
fast=50, slow=200 SMA 와 `.shift(1)` 적용 시:

- **골든크로스 최초 체결일**: `2020-10-08`
  - fast(50) = 148.29, slow(200) = 104.64 → fast > slow.
  - slow MA 워밍업 종료(200 거래일 이후) 직후 상승 구간 한가운데에서
    교차 발생 — 구성 의도와 일치.
- **데드크로스**: `2021-04-16` 에 signal 이 1→0 전환.
  - 상승 구간 끝의 피크(2021-04) 이후 하락 시작점과 일관.
- 월간 리밸런싱(21거래일마다) 기준 risky(SPY=1) 편입 6회, safe(BIL=1)
  편입 14회 — 워밍업 + 하락 구간에서 safe 로 회피하는 패턴 확인.

### 2) seasonal halloween 모드 (2023년 월초)

```
01 1, 02 1, 03 1, 04 1, 05 0, 06 0, 07 0, 08 0, 09 0, 10 0, 11 1, 12 1
```

→ 11/12/1/2/3/4 월만 1 반환 확인.

### 3) sell_in_may

halloween 과 **동일 월 집합**(11~4)으로 반환됨을 assert 로 확인.
(관점상 "5~10월 회피" 와 동치; docstring 명시.)

### 4) custom_months=[1,7]

1월 / 7월 시작일만 1, 나머지 0 확인.

### 5) presidential_term (election_dates=[2016-11-08, 2020-11-03, 2024-11-05])

6월 1일 기준 연도별 스팟체크:

| 연도 | 기대 | 실측 |
|------|------|------|
| 2017 (1년차) | 0 | 0 |
| 2018 (2년차) | 0 | 0 |
| 2019 (3년차 = pre-election) | **1** | **1** |
| 2020 (4년차/election year) | 0 | 0 |
| 2021 (1년차) | 0 | 0 |
| 2022 (2년차) | 0 | 0 |
| 2023 (3년차) | **1** | **1** |
| 2024 (4년차) | 0 | 0 |

### 6) combine_signals

- and:         `[1, 0, 0, 0]` (ma=[1,1,0,0], se=[1,0,1,0]) ✓
- weighted α=0.5: `[1.0, 0.5, 0.5, 0.0]` ✓

### 7) SeasonalMovingAverage (halloween + and)

crossover signal 이 1 인 `2021-03-18` 리밸런싱 행에서 SPY=1.0
(3월=halloween 시즌). 이후 2021-04-16 부터 dead cross 로 SPY=0,
BIL=1.0 — 두 신호의 AND 결합이 의도대로 동작.

## 이슈/블로커

없음.

## 다음 제안

- `market_events` 테이블에서 `presidential_election` 이벤트를 조회해
  `election_dates` 를 params 에 주입하는 헬퍼를 웹/엔진 레이어에
  추가하는 후속 태스크 필요.
- 파생(`triple.py`, `adaptive.py`, `slope.py`) 구현 시 `_common` 의
  `rolling_mean` 을 재사용하고, slope/adaptive 전용 헬퍼를 동일
  모듈에 누적할 것.
- 단위 테스트(tester) 에 NaN 워밍업 경계, fast==slow 검증 에러,
  weighted 모드 α 범위, presidential_term 의 첫 대선 이전 구간
  0 처리 등을 포함 권장.
