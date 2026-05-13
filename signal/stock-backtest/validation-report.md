# Backtest Engine Validation Report

Plan C 검증 (Layer 1~4) — 2026-05-06 실행.

## 요약

| Layer | 케이스 수 | PASS | FAIL | 정밀도 |
|-------|-----------|------|------|--------|
| L1 | 5 | 5 | 0 | 1e-9 (닫힌식 한 줄 수식) |
| L2 | 3 | 3 | 0 | 1e-6 (손계산 박제) |
| L3 | 1 | 1 | 0 | invariant (engine 무관 명제) |

**Total: 9/9 PASS, runtime ≈ 1.9s**

## 검증 방법론 (4-Layer)

- **L1 닫힌식**: 시뮬 0줄, 한 줄 수식 (BH 케이스). 엔진은 일별 시뮬 + Decimal,
  오라클은 float + math.floor 한 줄 — 알고리즘 패러다임 자체가 다름. 같은 버그 동시
  침투 가능성 무시 가능.
- **L2 손계산 박제**: pen+paper 로 5-day mini case 풀어 결과 숫자를 코드에 literal
  상수로 박제. 엔진 코드 import 안 함. 100% 독립.
- **L3 invariants**: engine 무관 수학 명제 (회계 항등식, peak monotone, MDD ≤ 0,
  Calmar = CAGR/|MDD|, equity peak idx == price peak idx for BH).
- **L4 Opus 4.7 sanity**: 시계열 요약 + 엔진 출력만 Opus 에 전달. JSON 응답으로
  PLAUSIBLE/SUSPECT 평가. 정량 비교 안 함 (LLM 산술 정밀도 부족 — 의심점 자유서술만).

## 케이스별 결과

### Layer L1

### C1 — SPY BH USD 평탄가 (yearly) (L1) — ✅ PASS
  PASS num_fills: actual=1 expected=1
  PASS final_qty: actual=99.000000 expected=99.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_after_buy_USD: actual=89.604505 expected=89.604505 diff=-1.15e-12 (0.0000%)
  PASS final_equity: actual=9989.604505 expected=9989.604505 diff=-1.82e-12 (0.0000%)
  PASS initial_equity: actual=10000.000000 expected=10000.000000 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.001040 expected=-0.001040 diff=-1.85e-16 (0.0000%)
  PASS peak_equity: actual=10000.000000 expected=10000.000000 diff=+0.00e+00 (0.0000%)
  notes:
    - qty=99.0
    - cash_after=89.6045
    - equity=9989.6045

### C2 — KODEX BH KRW 선형 +20% (L1) — ✅ PASS
  PASS num_fills: actual=1 expected=1
  PASS final_qty: actual=284.000000 expected=284.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_after_buy_KRW: actual=15396.067363 expected=15396.067363 diff=-7.28e-10 (0.0000%)
  PASS final_equity: actual=11943396.067363 expected=11943396.067363 diff=+0.00e+00 (0.0000%)
  PASS initial_equity: actual=10000000.000000 expected=10000000.000000 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.001147 expected=-0.001147 diff=+4.81e-17 (0.0000%)
  notes:
    - p_settle(Day 1)=35116.6667, p_final=42000.0000
    - qty=284.0, cash_after=15396.07
    - day0=10000000.00, day1=9988529.40

### C3 — BTC fractional BH USD 선형 +50% (L1) — ✅ PASS
  PASS num_fills: actual=1 expected=1
  PASS final_qty_btc: actual=0.197951 expected=0.197951 diff=+0.00e+00 (0.0000%)
  PASS cash_after_buy_USD: actual=0.000377 expected=0.000377 diff=-1.05e-12 (0.0000%)
  PASS final_equity: actual=14846.325377 expected=14846.325377 diff=+0.00e+00 (0.0000%)
  PASS initial_equity: actual=10000.000000 expected=10000.000000 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.001997 expected=-0.001997 diff=-2.19e-16 (0.0000%)
  notes:
    - qty=0.197951 (fractional 8자리)
    - p_settle=50416.67, p_final=75000.00
    - cash_after=0.0004

### C4 — 60/40 BH USD 평탄가 (yearly) (L1) — ✅ PASS
  PASS num_fills: actual=2 expected=2
  PASS qty_spy: actual=60.000000 expected=60.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_tlt: actual=41.000000 expected=41.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_after_USD: actual=94.609755 expected=94.609755 diff=-4.83e-13 (0.0000%)
  PASS final_equity: actual=9989.609755 expected=9989.609755 diff=+0.00e+00 (0.0000%)
  PASS initial_equity: actual=10000.000000 expected=10000.000000 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.001039 expected=-0.001039 diff=+3.25e-18 (0.0000%)
  notes:
    - qty_spy=60.0, qty_tlt=41.0
    - cash_after=94.6098, equity=9989.6098

### C5 — AllWeather 5자산 BH USD (yearly) (L1) — ✅ PASS
  PASS num_fills: actual=5 expected=5
  PASS qty_spy: actual=75.000000 expected=75.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_tlt: actual=444.000000 expected=444.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_ief: actual=157.000000 expected=157.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_gld: actual=41.000000 expected=41.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_dbc: actual=340.000000 expected=340.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_after_USD: actual=160.273263 expected=160.273263 diff=-1.47e-11 (0.0000%)
  PASS final_equity: actual=99895.273263 expected=99895.273263 diff=-1.46e-11 (0.0000%)
  PASS initial_equity: actual=100000.000000 expected=100000.000000 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.001047 expected=-0.001047 diff=-1.68e-16 (0.0000%)
  notes:
    - qtys={1: 75.0, 2: 444.0, 3: 157.0, 4: 41.0, 5: 340.0}
    - cash_after=160.27

### Layer L2

### C6 — 60/40 monthly 5-day Jan-Feb 경계 (path-dependent) (L2) — ✅ PASS
  PASS num_fills: actual=4 expected=4
  PASS qty_spy_final: actual=57.000000 expected=57.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_tlt_final: actual=42.000000 expected=42.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_USD_final: actual=118.943006 expected=118.943006 diff=+0.00e+00 (0.0000%)
  PASS final_equity: actual=10588.943006 expected=10588.943006 diff=+0.00e+00 (0.0000%)
  PASS initial_equity: actual=10000.000000 expected=10000.000000 diff=+0.00e+00 (0.0000%)
  PASS peak_equity: actual=10589.604505 expected=10589.604505 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.001040 expected=-0.001040 diff=-3.47e-18 (0.0000%)
  PASS num_equity_points: actual=5 expected=5
  notes:
    - 수동 계산: docstring trace 참조 (TASK-244 큐잉 패턴)
    - 기대 equity_curve = [10000.0000, 9989.6045, 10589.6045, 10589.6045, 10588.9430]

### C7 — compute_metrics 직접: MDD 합성 시리즈 [100,110,120,100,80,90,110] (L2) — ✅ PASS
  PASS mdd: actual=-0.333333 expected=-0.333333 diff=-5.55e-17 (0.0000%)
  PASS win_rate: actual=0.666667 expected=0.666667 diff=+0.00e+00 (0.0000%)
  PASS cagr: actual=329.963202 expected=329.963202 diff=+0.00e+00 (0.0000%)
  notes:
    - 엔진 미경유 (compute_metrics 만)
    - hand-MDD = (80-120)/120 = -0.333333

### C8 — 폭락-회복 단일 SPY 5-day (peak/trough 명확) (L2) — ✅ PASS
  PASS num_fills: actual=1 expected=1
  PASS qty_spy: actual=99.000000 expected=99.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_USD: actual=89.604505 expected=89.604505 diff=+0.00e+00 (0.0000%)
  PASS final_equity: actual=8999.604505 expected=8999.604505 diff=+0.00e+00 (0.0000%)
  PASS peak_equity: actual=11969.604505 expected=11969.604505 diff=+0.00e+00 (0.0000%)
  PASS trough_after_peak: actual=8009.604505 expected=8009.604505 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=-0.330838 expected=-0.330838 diff=+0.00e+00 (0.0000%)
  notes:
    - prices = [100.0, 100.0, 120.0, 80.0, 90.0]
    - peak=11969.6045, trough=8009.6045, MDD=-0.330838

### Layer L3

### C9 — L3 invariants — 큰 폭락-회복 (peak idx=20, trough idx=40) (L3) — ✅ PASS
  PASS accounting_identity_final: actual=12657.059878 expected=12657.059878 diff=+0.00e+00 (0.0000%)
  PASS peak_monotone_non_decreasing: actual=True expected=True
  PASS mdd_le_zero: actual=True expected=True
  PASS calmar_identity: actual=2.876443 expected=2.876443 diff=+0.00e+00 (0.0000%)
  PASS all_cash_non_negative: actual=True expected=True
  PASS all_qty_non_negative: actual=True expected=True
  PASS first_equity_le_initial: actual=True expected=True
  PASS equity_peak_idx_matches_price_peak_idx: actual=20 expected=20
  PASS equity_trough_idx_matches_price_trough_idx: actual=40 expected=40
  PASS mdd_in_expected_range: actual=True expected=True
  notes:
    - price [start=100, peak=150 @ idx20, trough=60 @ idx40, end=130]
    - actual MDD=-0.598066, peak_value=14597.0599, trough_value=5867.0599
    - num_days=61, num_fills=1
