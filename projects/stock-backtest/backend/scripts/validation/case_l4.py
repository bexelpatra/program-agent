"""Layer 4 — Opus 4.7 sanity 호출 (2 케이스).

L1/L2/L3 모두 통과한 시점에서 *설계 sanity* 만 의심. 비용 최소화 위해 복합 시나리오 2건만.

S1: C9 폭락-회복 (큰 변동) — equity peak/trough/MDD 가 입력 가격 곡선과 일관한가?
S2: C6 60/40 monthly mini — path-dependent rebalance 가 합리적인 자산 배분 변화를 보이는가?
"""

from __future__ import annotations

from dataclasses import dataclass, field

from scripts.validation._helpers import CaseResult, FieldCheck
from scripts.validation.case_l2 import case_c6_sixty_forty_monthly_mini
from scripts.validation.case_l3 import case_c9_large_crash_recovery_invariants
from scripts.validation.opus_oracle import (
    OpusVerdict,
    build_sanity_prompt,
    call_opus,
    parse_opus_json,
)


@dataclass
class OpusCaseRecord:
    case_id: str
    title: str
    scenario_md: str
    engine_output_md: str
    verdict: OpusVerdict


def _build_s1_inputs() -> tuple[str, str]:
    scenario = """
- 자산: SPY 1종 (US/USD)
- 초기 자본: $10,000 USD (base=USD)
- 전략: FixedWeight 100% SPY, yearly rebalance (실질 init only)
- 수수료: US 0.005%, 슬리피지 0.10%
- 가격 곡선 (3개월 ~63 거래일):
  - idx 0: $100 (start)
  - idx 1 (settlement): $102.5 (선형 보간 100→150 over 20)
  - idx 20: $150 (peak)
  - idx 40: $60  (trough)
  - idx 마지막: $130 (end)
  - 구간별 선형 보간: [100→150 (20 idx)], [150→60 (20 idx)], [60→130 (~22 idx)]
"""
    # 실측 결과 (위 C9 실행 결과 — 검증 완료한 값만).
    output = """
- num_fills: 1 (init buy)
- initial_equity (Day 0): $9,747.06 (qty=97 × $100 + cash $47.06; init buy at $102.5 settlement)
- final_equity (Day 60): $12,657.06 USD (cumulative return ≈ +29.86%)
- equity_curve 길이: 61
- equity peak: $14,597.06 (idx 20 = 가격 peak $150 일자와 일치)
- equity trough: $5,867.06 (idx 40 = 가격 trough $60 일자와 일치)
- days_span: 86 일 (~0.2355 년)
- MDD: -0.598066 (-59.81%)
- CAGR: 2.032996 (= (12657/9747)^(1/0.2355) - 1 = 203.30% 연환산)
- Calmar: 3.399285 (= 2.0330 / 0.5981, identity 검증 통과)
- 회계 항등식: equity == positions_value + cash 검증 통과 (final 일치, 1e-9 tol)
- peak monotone non-decreasing: True
- 모든 cash ≥ 0, 모든 qty ≥ 0
"""
    return scenario, output


def _build_s2_inputs() -> tuple[str, str]:
    scenario = """
- 자산: SPY + TLT 2종 (둘 다 US/USD)
- 초기 자본: $10,000 USD (base=USD)
- 전략: FixedWeight {SPY: 60%, TLT: 40%}, monthly rebalance
- 수수료: US 0.005%, 슬리피지 0.10%
- 기간: 2024-01-29 ~ 2024-02-02 (NYSE 5 거래일, Jan-Feb 경계)
- 가격:
  - SPY: Day 0,1 = $100 / Day 2,3,4 = $110 (Jan 31 부터 +10%)
  - TLT: 평탄 $100
- rebalance 발생: Day 0 (Jan 29 init), Day 3 (Feb 1 monthly). Day 4 = Feb 2 = settlement of Day 3 rebalance.
"""
    output = """
- num_fills: 4 (init buy SPY + init buy TLT + Day 3 rebalance sell SPY + Day 3 rebalance buy TLT)
- final_qty_spy: 57 주
- final_qty_tlt: 42 주
- final_cash_USD: $118.94
- final_equity: $10,588.94
- equity_curve = [9989.60, 9989.60, 10589.60, 10588.94, 10588.94]
- peak: $10,589.60 (Day 2 SPY 상승 후 / Day 3 rebalance 직전)
- MDD: -6.21e-5 (-0.0062%)
- 초기 매수 시 60/40 정수 단위 조정: target SPY=60주, TLT=40주이지만 cash 부족으로 TLT 39주 체결 (-1주, observation: TLT 의도 비중 미달)
- Day 3 rebalance: SPY 60→57 (sell 3), TLT 39→42 (buy 3). 60/40 회복 시도.
"""
    return scenario, output


def run_l4_opus_cases() -> tuple[list[CaseResult], list[OpusCaseRecord]]:
    """2 Opus 호출 → CaseResult + 상세 레코드 반환."""
    records: list[OpusCaseRecord] = []
    results: list[CaseResult] = []

    # S1
    print("[L4] Calling Opus for S1 (crash-recovery)...")
    scenario, output = _build_s1_inputs()
    prompt = build_sanity_prompt(scenario, output)
    raw = call_opus(prompt)
    verdict = parse_opus_json(raw)
    records.append(
        OpusCaseRecord(
            case_id="S1",
            title="Opus sanity: C9 폭락-회복 invariants",
            scenario_md=scenario,
            engine_output_md=output,
            verdict=verdict,
        )
    )
    plausible = verdict.verdict == "PLAUSIBLE"
    results.append(
        CaseResult(
            case_id="S1",
            title="Opus sanity: 폭락-회복",
            layer="L4",
            checks=[
                FieldCheck(
                    name="opus_verdict",
                    actual=verdict.verdict,
                    expected="PLAUSIBLE",
                    passed=plausible,
                )
            ],
            notes=[
                f"reasoning: {verdict.reasoning}",
                f"suspicions: {verdict.suspicions if verdict.suspicions else 'none'}",
            ],
        )
    )

    # S2
    print("[L4] Calling Opus for S2 (60/40 monthly)...")
    scenario, output = _build_s2_inputs()
    prompt = build_sanity_prompt(scenario, output)
    raw = call_opus(prompt)
    verdict = parse_opus_json(raw)
    records.append(
        OpusCaseRecord(
            case_id="S2",
            title="Opus sanity: C6 60/40 monthly mini",
            scenario_md=scenario,
            engine_output_md=output,
            verdict=verdict,
        )
    )
    plausible = verdict.verdict == "PLAUSIBLE"
    results.append(
        CaseResult(
            case_id="S2",
            title="Opus sanity: 60/40 monthly",
            layer="L4",
            checks=[
                FieldCheck(
                    name="opus_verdict",
                    actual=verdict.verdict,
                    expected="PLAUSIBLE",
                    passed=plausible,
                )
            ],
            notes=[
                f"reasoning: {verdict.reasoning}",
                f"suspicions: {verdict.suspicions if verdict.suspicions else 'none'}",
            ],
        )
    )

    return results, records
