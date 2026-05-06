# Backtest Engine Validation Report

Plan C 검증 (Layer 1~4) — 2026-05-06 실행.

## 요약

| Layer | 케이스 수 | PASS | FAIL | 정밀도 |
|-------|-----------|------|------|--------|
| L1 | 5 | 5 | 0 | 1e-9 (닫힌식 한 줄 수식) |
| L2 | 3 | 3 | 0 | 1e-6 (손계산 박제) |
| L3 | 1 | 1 | 0 | invariant (engine 무관 명제) |
| L4 | 2 | 2 | 0 | qualitative (Opus sanity) |

**Total: 11/11 PASS, runtime ≈ 2.1s**

## ⚠️ 발견된 결함 — TASK-244 BUG 등록 (2026-05-06)

L4 Opus 4.7 의 S1 sanity 응답이 짚은 의심점이 사용자 검토 후 **BUG 등급** 으로 확정:

> 엔진의 D iteration 안에서 ① 시그널 (D 종가까지) → ② settlement_d=D+1 → ③ `execute_rebalance` *즉시* 실행 → ④ 같은 D iteration 안에서 EOD equity 기록 (D 가격으로 *post-rebalance* 평가).

**사용자 멘탈 모델 (정확)**:
- 매도 시그널의 D EOD: 아직 매도 전 → 주식 시가 평가 그대로
- 매수 시그널의 D EOD: 아직 매수 전 → cash 그대로

**현 엔진 동작 (어긋남)**:
- D EOD 평가에 "D+1 가격으로 산 새 포지션을 D 가격으로 평가" + "D+1 settlement 직후 cash" 가 D 가격으로 기록됨.

**영향 (사용자 지적)**: 종가↔시가 갭이 큰 자산 (BTC 등) + 장기 백테스트 (수년) 에서 일별 회계 편향이 누적 — *스노우볼*. MDD/Sharpe 지표에 의미 있는 편향 가능.

**수정 방향**: `pending_rebalance` 큐잉 패턴. D 시그널 → 다음 iteration (D+1) 시작 시점에 settlement → D+1 EOD equity 기록.

**전체 11/11 PASS 의 의미 재해석**: 검증은 "엔진이 *현 명세대로* 동작함" 을 확인했지 "현 명세가 *사용자 의도와 정합함*" 을 확인한 게 아님. 이번 발견은 *명세 자체의 결함* 이며 L4 Opus 의 정성 평가가 잡아낸 영역. 수정 후 골든 9 + L1~L3 11 + 관련 회귀 모두 baseline 재생성 필요.

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
  PASS initial_equity: actual=9989.604505 expected=9989.604505 diff=-1.82e-12 (0.0000%)
  PASS mdd: actual=0.000000 expected=0.000000 diff=+0.00e+00 (0.0000%)
  PASS peak_equity: actual=9989.604505 expected=9989.604505 diff=-1.82e-12 (0.0000%)
  notes:
    - qty=99.0
    - cash_after=89.6045
    - equity=9989.6045

### C2 — KODEX BH KRW 선형 +20% (L1) — ✅ PASS
  PASS num_fills: actual=1 expected=1
  PASS final_qty: actual=284.000000 expected=284.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_after_buy_KRW: actual=15396.067363 expected=15396.067363 diff=-7.28e-10 (0.0000%)
  PASS final_equity: actual=11943396.067363 expected=11943396.067363 diff=+0.00e+00 (0.0000%)
  PASS initial_equity: actual=9955396.067363 expected=9955396.067363 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=0.000000 expected=0.000000 diff=+0.00e+00 (0.0000%)
  notes:
    - p_settle(D+1)=35116.6667, p_final=42000.0000
    - qty=284.0, cash_after=15396.07

### C3 — BTC fractional BH USD 선형 +50% (L1) — ✅ PASS
  PASS num_fills: actual=1 expected=1
  PASS final_qty_btc: actual=0.197951 expected=0.197951 diff=+0.00e+00 (0.0000%)
  PASS cash_after_buy_USD: actual=0.000377 expected=0.000377 diff=-1.05e-12 (0.0000%)
  PASS final_equity: actual=14846.325377 expected=14846.325377 diff=+0.00e+00 (0.0000%)
  PASS mdd: actual=0.000000 expected=0.000000 diff=+0.00e+00 (0.0000%)
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
  PASS mdd: actual=0.000000 expected=0.000000 diff=+0.00e+00 (0.0000%)
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
  PASS mdd: actual=0.000000 expected=0.000000 diff=+0.00e+00 (0.0000%)
  notes:
    - qtys={1: 75.0, 2: 444.0, 3: 157.0, 4: 41.0, 5: 340.0}
    - cash_after=160.27

### Layer L2

### C6 — 60/40 monthly 5-day Jan-Feb 경계 (path-dependent) (L2) — ✅ PASS
  PASS num_fills: actual=4 expected=4
  PASS qty_spy_final: actual=57.000000 expected=57.000000 diff=+0.00e+00 (0.0000%)
  PASS qty_tlt_final: actual=42.000000 expected=42.000000 diff=+0.00e+00 (0.0000%)
  PASS cash_USD_final: actual=118.943006 expected=118.942997 diff=+1.00e-05 (0.0000%)
  PASS final_equity: actual=10588.943006 expected=10588.942996 diff=+1.00e-05 (0.0000%)
  PASS peak_equity: actual=10589.604505 expected=10589.604500 diff=+5.00e-06 (0.0000%)
  PASS mdd: actual=-0.000062 expected=-0.000062 diff=+4.72e-10 (0.0008%)
  PASS num_equity_points: actual=5 expected=5
  notes:
    - 수동 계산: docstring trace 참조
    - 기대 equity_curve = [9989.6045, 9989.6045, 10589.6045, 10588.9430, 10588.9430]

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
  PASS calmar_identity: actual=3.399285 expected=3.399285 diff=+0.00e+00 (0.0000%)
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

### Layer L4

### S1 — Opus sanity: 폭락-회복 (L4) — ✅ PASS
  PASS opus_verdict: actual=PLAUSIBLE expected=PLAUSIBLE
  notes:
    - reasoning: 엔진 출력은 입력 가격 곡선에 정합한다: peak/trough 일자가 가격 극값 idx와 일치하고, 97주 보유 × 각 일자 가격 + 현금 $47.06 으로 equity 시계열이 닫힌식 검증된다. CAGR 203%와 MDD -59.8%는 짧은 86일 윈도우(연환산)와 $150→$60 -60% drawdown 입력에 비례해 합리적이며, 부호·자릿수 오류 없음. 회계 항등식 통과, qty/cash 비음수 조건 충족.
    - suspicions: ['init buy가 idx 1의 settlement price($102.5)로 체결됐는데 포지션 qty=97이 idx 0(price=$100)부터 equity_curve에 반영된 점은 형식상 D+1 가격을 D에 사용한 모양새지만, 초기 매수에 대한 흔한 시뮬 관용(slippage·fee·price gap을 Day 0 mark에 한 번에 흡수)으로 해석 가능. 다만 일반 리밸런싱에도 같은 관행이 적용되는지(즉 정기 리밸런싱 fill price를 D close mark에 즉시 반영하는지) 별도 시나리오로 확인 권장 — 본 시나리오는 init only라 분리 검증 불가.']

### S2 — Opus sanity: 60/40 monthly (L4) — ✅ PASS
  PASS opus_verdict: actual=PLAUSIBLE expected=PLAUSIBLE
  notes:
    - reasoning: 최종 수익률 +5.89% 는 SPY 60% 가중치 × +10% 가격 상승 ≈ +6% 에서 슬리피지·수수료·TLT 1주 미달분을 차감한 값과 정합. 부호·자릿수·look-ahead 의심점 없음. Day 3 rebalance 가 Day 2(Jan 31) close 시그널을 Day 3(Feb 1) open 에 체결하는 자연스러운 흐름으로 해석되며, equity curve 의 0.66 USD drop 은 cost only 변화로 설명 가능.
    - suspicions: none

## Opus 4.7 응답 원문 (L4)

### S1: Opus sanity: C9 폭락-회복 invariants

**verdict**: `PLAUSIBLE`

**reasoning**:

> 엔진 출력은 입력 가격 곡선에 정합한다: peak/trough 일자가 가격 극값 idx와 일치하고, 97주 보유 × 각 일자 가격 + 현금 $47.06 으로 equity 시계열이 닫힌식 검증된다. CAGR 203%와 MDD -59.8%는 짧은 86일 윈도우(연환산)와 $150→$60 -60% drawdown 입력에 비례해 합리적이며, 부호·자릿수 오류 없음. 회계 항등식 통과, qty/cash 비음수 조건 충족.

**suspicions**:
- init buy가 idx 1의 settlement price($102.5)로 체결됐는데 포지션 qty=97이 idx 0(price=$100)부터 equity_curve에 반영된 점은 형식상 D+1 가격을 D에 사용한 모양새지만, 초기 매수에 대한 흔한 시뮬 관용(slippage·fee·price gap을 Day 0 mark에 한 번에 흡수)으로 해석 가능. 다만 일반 리밸런싱에도 같은 관행이 적용되는지(즉 정기 리밸런싱 fill price를 D close mark에 즉시 반영하는지) 별도 시나리오로 확인 권장 — 본 시나리오는 init only라 분리 검증 불가.

<details><summary>raw response</summary>

```
```json
{
  "verdict": "PLAUSIBLE",
  "reasoning": "엔진 출력은 입력 가격 곡선에 정합한다: peak/trough 일자가 가격 극값 idx와 일치하고, 97주 보유 × 각 일자 가격 + 현금 $47.06 으로 equity 시계열이 닫힌식 검증된다. CAGR 203%와 MDD -59.8%는 짧은 86일 윈도우(연환산)와 $150→$60 -60% drawdown 입력에 비례해 합리적이며, 부호·자릿수 오류 없음. 회계 항등식 통과, qty/cash 비음수 조건 충족.",
  "suspicions": [
    "init buy가 idx 1의 settlement price($102.5)로 체결됐는데 포지션 qty=97이 idx 0(price=$100)부터 equity_curve에 반영된 점은 형식상 D+1 가격을 D에 사용한 모양새지만, 초기 매수에 대한 흔한 시뮬 관용(slippage·fee·price gap을 Day 0 mark에 한 번에 흡수)으로 해석 가능. 다만 일반 리밸런싱에도 같은 관행이 적용되는지(즉 정기 리밸런싱 fill price를 D close mark에 즉시 반영하는지) 별도 시나리오로 확인 권장 — 본 시나리오는 init only라 분리 검증 불가."
  ]
}
```
```

</details>

### S2: Opus sanity: C6 60/40 monthly mini

**verdict**: `PLAUSIBLE`

**reasoning**:

> 최종 수익률 +5.89% 는 SPY 60% 가중치 × +10% 가격 상승 ≈ +6% 에서 슬리피지·수수료·TLT 1주 미달분을 차감한 값과 정합. 부호·자릿수·look-ahead 의심점 없음. Day 3 rebalance 가 Day 2(Jan 31) close 시그널을 Day 3(Feb 1) open 에 체결하는 자연스러운 흐름으로 해석되며, equity curve 의 0.66 USD drop 은 cost only 변화로 설명 가능.

<details><summary>raw response</summary>

```
```json
{
  "verdict": "PLAUSIBLE",
  "reasoning": "최종 수익률 +5.89% 는 SPY 60% 가중치 × +10% 가격 상승 ≈ +6% 에서 슬리피지·수수료·TLT 1주 미달분을 차감한 값과 정합. 부호·자릿수·look-ahead 의심점 없음. Day 3 rebalance 가 Day 2(Jan 31) close 시그널을 Day 3(Feb 1) open 에 체결하는 자연스러운 흐름으로 해석되며, equity curve 의 0.66 USD drop 은 cost only 변화로 설명 가능.",
  "suspicions": []
}
```
```

</details>
