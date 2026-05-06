"""Opus 4.7 sanity oracle — claude CLI subprocess 호출.

L4 정책:
- L1/L2/L3 가 통과한 후 *복합 케이스* 에 대해서만 호출 (산술 정밀도가 아닌 설계 sanity).
- 시계열 전체를 LLM 에 넣지 않음 — 요약 통계 + 체크포인트 가격 + 엔진 결과만 전달.
- 응답 형식 강제 (JSON: verdict / reasoning / suspicions).
- 정량 비교 안 함, 자유서술 의심점만 수집.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass


@dataclass
class OpusVerdict:
    raw_response: str
    verdict: str  # "PLAUSIBLE" | "SUSPECT" | "PARSE_ERROR"
    reasoning: str
    suspicions: list[str]


def call_opus(prompt: str, timeout_sec: int = 300) -> str:
    """claude -p --model claude-opus-4-7 호출. stdin 으로 prompt 전달."""
    proc = subprocess.run(
        [
            "claude",
            "-p",
            "--model",
            "claude-opus-4-7",
            "--output-format",
            "text",
        ],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    if proc.returncode != 0:
        return f"[OPUS_ERROR exit={proc.returncode}] stderr={proc.stderr[:500]}"
    return proc.stdout.strip()


def parse_opus_json(raw: str) -> OpusVerdict:
    """Opus 응답에서 첫 번째 JSON 객체를 파싱. 실패 시 PARSE_ERROR."""
    # Markdown code block 제거 (```json ... ```)
    cleaned = raw
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if m:
        cleaned = m.group(1)
    else:
        # 첫 { ... 마지막 } 찾기
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            cleaned = raw[start : end + 1]

    try:
        obj = json.loads(cleaned)
        return OpusVerdict(
            raw_response=raw,
            verdict=str(obj.get("verdict", "UNKNOWN")),
            reasoning=str(obj.get("reasoning", "")),
            suspicions=[str(s) for s in obj.get("suspicions", [])],
        )
    except json.JSONDecodeError as e:
        return OpusVerdict(
            raw_response=raw,
            verdict="PARSE_ERROR",
            reasoning=f"JSON parse failed: {e}",
            suspicions=[],
        )


def build_sanity_prompt(scenario_md: str, engine_output_md: str) -> str:
    """공통 sanity check 프롬프트 — Korean, JSON 응답 강제."""
    return f"""당신은 백테스팅 엔진의 정확성을 평가하는 검토자입니다. 아래 시나리오 입력과 엔진 출력을 보고, 결과가 입력 조건에 비추어 **합리적**인지 판단해주세요.

당신은 *세부 산술 정확성* 을 검증하지 않습니다 (이미 닫힌식 검증을 통과). 대신 **설계 레벨의 의심점** 만 봅니다:
- 부호 반전 (음수가 양수로 등)
- 자릿수 오류 (10배 차이 등)
- look-ahead bias 의심 (D+1 데이터를 D 시그널에 사용한 흔적)
- 비현실적 결과 (수익률 100x, 음수 수량, 0 리밸런싱 등)
- 입력 조건에서 도출되는 결과 범위와 큰 괴리

# 시나리오 입력

{scenario_md}

# 엔진 출력

{engine_output_md}

# 응답 형식 (JSON 만, markdown code block 가능)

```json
{{
  "verdict": "PLAUSIBLE" 또는 "SUSPECT",
  "reasoning": "왜 그렇게 판단했는지 2-3 문장",
  "suspicions": ["의심점 1", "의심점 2", ...]
}}
```

`PLAUSIBLE` = 결과가 입력 조건에 비추어 합리적, 명백한 설계 의심점 없음.
`SUSPECT` = 1개 이상의 명백한 설계 의심점 존재. suspicions 에 구체적으로 명시.

산술 차이 0.001% 같은 미세 오차는 SUSPECT 사유 아님 (이미 다른 레이어에서 검증됨).
"""
