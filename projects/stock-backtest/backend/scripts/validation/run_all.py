"""전체 validation harness 실행 → signal/.../validation-report.md 생성.

Usage:
    cd projects/stock-backtest/backend
    .venv/bin/python -m scripts.validation.run_all [--skip-opus]

옵션:
    --skip-opus  L4 Opus 호출 스킵 (L1~L3 만 실행, 비용 0)
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from scripts.validation._helpers import CaseResult
from scripts.validation.case_l1 import CASES_L1
from scripts.validation.case_l2 import CASES_L2
from scripts.validation.case_l3 import CASES_L3


def run_case(f) -> tuple[CaseResult, float]:
    t0 = time.time()
    try:
        r = f()
        return r, time.time() - t0
    except Exception as e:
        import traceback

        tb = traceback.format_exc()
        return (
            CaseResult(
                case_id="?",
                title=f.__name__,
                layer="?",
                checks=[],
                notes=[f"EXCEPTION: {e}", tb],
            ),
            time.time() - t0,
        )


def format_md_report(
    all_results: list[tuple[CaseResult, float]],
    opus_records=None,
) -> str:
    lines: list[str] = []
    lines.append("# Backtest Engine Validation Report")
    lines.append("")
    lines.append("Plan C 검증 (Layer 1~4) — 2026-05-06 실행.")
    lines.append("")
    lines.append("## 요약")
    lines.append("")

    by_layer: dict[str, list[CaseResult]] = {}
    total_time = 0.0
    for r, t in all_results:
        by_layer.setdefault(r.layer, []).append(r)
        total_time += t

    lines.append("| Layer | 케이스 수 | PASS | FAIL | 정밀도 |")
    lines.append("|-------|-----------|------|------|--------|")
    for layer in ["L1", "L2", "L3", "L4"]:
        rs = by_layer.get(layer, [])
        if not rs:
            continue
        passed = sum(1 for r in rs if r.passed)
        failed = len(rs) - passed
        precision_note = {
            "L1": "1e-9 (닫힌식 한 줄 수식)",
            "L2": "1e-6 (손계산 박제)",
            "L3": "invariant (engine 무관 명제)",
            "L4": "qualitative (Opus sanity)",
        }.get(layer, "")
        lines.append(f"| {layer} | {len(rs)} | {passed} | {failed} | {precision_note} |")
    lines.append("")
    total_pass = sum(1 for r, _ in all_results if r.passed)
    total = len(all_results)
    lines.append(f"**Total: {total_pass}/{total} PASS, runtime ≈ {total_time:.1f}s**")
    lines.append("")

    lines.append("## 검증 방법론 (4-Layer)")
    lines.append("")
    lines.append("- **L1 닫힌식**: 시뮬 0줄, 한 줄 수식 (BH 케이스). 엔진은 일별 시뮬 + Decimal,")
    lines.append("  오라클은 float + math.floor 한 줄 — 알고리즘 패러다임 자체가 다름. 같은 버그 동시")
    lines.append("  침투 가능성 무시 가능.")
    lines.append("- **L2 손계산 박제**: pen+paper 로 5-day mini case 풀어 결과 숫자를 코드에 literal")
    lines.append("  상수로 박제. 엔진 코드 import 안 함. 100% 독립.")
    lines.append("- **L3 invariants**: engine 무관 수학 명제 (회계 항등식, peak monotone, MDD ≤ 0,")
    lines.append("  Calmar = CAGR/|MDD|, equity peak idx == price peak idx for BH).")
    lines.append("- **L4 Opus 4.7 sanity**: 시계열 요약 + 엔진 출력만 Opus 에 전달. JSON 응답으로")
    lines.append("  PLAUSIBLE/SUSPECT 평가. 정량 비교 안 함 (LLM 산술 정밀도 부족 — 의심점 자유서술만).")
    lines.append("")
    lines.append("## 케이스별 결과")
    lines.append("")

    for layer in ["L1", "L2", "L3", "L4"]:
        rs = by_layer.get(layer, [])
        if not rs:
            continue
        lines.append(f"### Layer {layer}")
        lines.append("")
        for r in rs:
            lines.append(r.format_md())
            lines.append("")

    if opus_records:
        lines.append("## Opus 4.7 응답 원문 (L4)")
        lines.append("")
        for rec in opus_records:
            lines.append(f"### {rec.case_id}: {rec.title}")
            lines.append("")
            lines.append(f"**verdict**: `{rec.verdict.verdict}`")
            lines.append("")
            lines.append("**reasoning**:")
            lines.append("")
            lines.append("> " + rec.verdict.reasoning.replace("\n", "\n> "))
            lines.append("")
            if rec.verdict.suspicions:
                lines.append("**suspicions**:")
                for s in rec.verdict.suspicions:
                    lines.append(f"- {s}")
                lines.append("")
            lines.append("<details><summary>raw response</summary>")
            lines.append("")
            lines.append("```")
            lines.append(rec.verdict.raw_response[:2000])
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-opus", action="store_true", help="skip L4 Opus calls")
    parser.add_argument(
        "--report-path",
        default="../../../signal/stock-backtest/validation-report.md",
        help="output md report path (relative to backend cwd; worktree root + 3 levels up)",
    )
    args = parser.parse_args()

    all_results: list[tuple[CaseResult, float]] = []
    opus_records = None

    print("=" * 70)
    print("Layer 1 — 닫힌식 오라클 (5 cases)")
    print("=" * 70)
    for f in CASES_L1:
        r, t = run_case(f)
        all_results.append((r, t))
        status = "✅ PASS" if r.passed else "❌ FAIL"
        print(f"  {r.case_id} {status} ({t:.2f}s) — {r.title}")

    print()
    print("=" * 70)
    print("Layer 2 — 손계산 박제 (3 cases)")
    print("=" * 70)
    for f in CASES_L2:
        r, t = run_case(f)
        all_results.append((r, t))
        status = "✅ PASS" if r.passed else "❌ FAIL"
        print(f"  {r.case_id} {status} ({t:.2f}s) — {r.title}")

    print()
    print("=" * 70)
    print("Layer 3 — Invariants (1 case)")
    print("=" * 70)
    for f in CASES_L3:
        r, t = run_case(f)
        all_results.append((r, t))
        status = "✅ PASS" if r.passed else "❌ FAIL"
        print(f"  {r.case_id} {status} ({t:.2f}s) — {r.title}")

    if not args.skip_opus:
        print()
        print("=" * 70)
        print("Layer 4 — Opus 4.7 sanity (2 cases) — 호출에 시간 소요")
        print("=" * 70)
        from scripts.validation.case_l4 import run_l4_opus_cases

        l4_results, opus_records = run_l4_opus_cases()
        for r in l4_results:
            status = "✅ PASS" if r.passed else "❌ FAIL"
            print(f"  {r.case_id} {status} — {r.title}")
            for c in r.checks:
                print(f"    {c.format()}")
        all_results.extend([(r, 0.0) for r in l4_results])

    print()
    print("=" * 70)
    total_pass = sum(1 for r, _ in all_results if r.passed)
    total = len(all_results)
    print(f"FINAL: {total_pass}/{total} PASS")
    print("=" * 70)

    md = format_md_report(all_results, opus_records)
    out_path = Path(args.report_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md)
    print(f"\nReport written: {out_path}")

    return 0 if total_pass == total else 1


if __name__ == "__main__":
    sys.exit(main())
