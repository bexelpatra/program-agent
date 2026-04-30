"""Allocator weight dict 공용 검증 (TASK-231).

배경 (사용자 의도):
    `fixed_weight.py`, `all_weather.py`, `ma_signal.py` 의 `_validate_weights`
    field_validator 가 동일한 4단계 검증을 거의 똑같은 코드로 중복 박제하고
    있었다 (Coder 가이드 6항 — 2~3회 중복 후 추상화 시점에 도달).

    AllWeather 만 `Field(default_factory=...)` 가 빈 dict 진입을 막아주므로
    "non-empty 검사"를 생략한다는 차이가 있어, `allow_empty` 플래그로 제어한다.

검증 단계 (호출 순서):
    1. (allow_empty=False 일 때만) 빈 dict 거부
    2. 음수 비중 거부
    3. 합 ≤ 0 거부 (모두 0 인 경우)
    4. abs(total - 1.0) > total_tolerance 거부 (사용자 입력 편의로 ±5% 허용)

clean architecture:
    - 도메인 순수 (외부 라이브러리 import 없음).
    - 호출자 (allocator 별 _validate_weights field_validator) 가 그대로 입력 dict
      을 반환하므로, 본 함수도 검증 통과 시 입력 dict 을 그대로 돌려준다.
"""

from __future__ import annotations

from typing import TypeVar

K = TypeVar("K")


def validate_weight_dict(
    v: dict[K, float],
    *,
    name: str,
    total_tolerance: float = 0.05,
    allow_empty: bool = False,
) -> dict[K, float]:
    """allocator 비중 dict 공용 검증.

    Args:
        v: 비중 dict (key=asset_id 또는 category, value=비중).
        name: 에러 메시지에 노출할 필드 이름 (예: "weights", "category_weights",
            "assets"). 호출자별로 메시지를 그대로 보존하기 위해 명시적으로 받는다.
        total_tolerance: 합이 1.0 에서 벗어나도 허용할 절대 오차 (기본 0.05 = ±5%).
        allow_empty: True 면 빈 dict 을 허용 (AllWeather 처럼 default_factory 가
            처리하는 경우). False 면 빈 dict 를 ValueError 로 거부.

    Returns:
        검증을 통과한 입력 dict 그대로.

    Raises:
        ValueError: 위 4단계 중 하나라도 위반.
    """
    if not v:
        if allow_empty:
            # 빈 dict 면 후속 sum/tolerance 검사를 건너뛴다 (sum=0 으로 음의
            # 거짓양성 회피). 호출자가 default_factory 로 채울 책임을 진다.
            return v
        raise ValueError(f"{name} must not be empty")
    if any(w < 0 for w in v.values()):
        raise ValueError(f"{name} must be non-negative")
    total = sum(v.values())
    if total <= 0:
        raise ValueError(f"{name} total must be positive")
    if abs(total - 1.0) > total_tolerance:
        raise ValueError(
            f"{name} total {total} must be close to 1.0 (within {total_tolerance:.0%})"
        )
    return v
