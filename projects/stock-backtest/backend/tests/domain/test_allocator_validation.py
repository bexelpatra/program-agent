"""validate_weight_dict 단위 테스트 (TASK-231).

`backend/app/domain/allocators/_validation.py` 의 공용 검증 함수를 직접 호출하여
fixed_weight / ma_signal / all_weather 가 위임하는 4 단계 (allow_empty=False)
또는 3 단계 (allow_empty=True) 정책이 정확히 동작하는지 박제한다.

5 분기 (TASK-231 DoD ①):
    1. 빈 dict 거부 (allow_empty=False)
    2. 빈 dict 통과 (allow_empty=True)
    3. 음수 비중 거부
    4. 합계 0 거부
    5. tolerance 검증 — 합계 0.9 / 0.95 / 1.0 / 1.05 / 1.1 (기본 ±5%).
        - 1.0 → 통과 (정확)
        - 0.9, 1.1 → 거부 (±5% 밖)
        - 0.95, 1.05 → 거부 (IEEE 754 부동소수점으로 abs(0.95 - 1.0) ≈ 0.0500…044
          가 0.05 보다 크게 평가됨 — 기존 fixed_weight / ma_signal 코드의 strict
          `> 0.05` 비교와 동일한 의미. 사용자가 정확히 0.95 / 1.05 를 의도하면
          정수 입력 (95, 5) 등으로 우회).

clean architecture: pytest 만 의존, DB / pandas 미접근.
"""

from __future__ import annotations

import pytest

from app.domain.allocators._validation import validate_weight_dict


def test_rejects_empty_dict_when_allow_empty_false() -> None:
    """allow_empty=False (기본) 면 빈 dict 는 ValueError."""

    with pytest.raises(ValueError, match="weights must not be empty"):
        validate_weight_dict({}, name="weights")


def test_accepts_empty_dict_when_allow_empty_true() -> None:
    """allow_empty=True 면 빈 dict 통과 (AllWeather default_factory 시나리오)."""

    result = validate_weight_dict({}, name="category_weights", allow_empty=True)
    assert result == {}


def test_rejects_negative_weight() -> None:
    """음수 비중은 항상 거부 (allow_empty 와 무관)."""

    with pytest.raises(ValueError, match="non-negative"):
        validate_weight_dict({1: -0.1, 2: 1.1}, name="weights")


def test_rejects_total_zero() -> None:
    """전부 0 인 비중 dict 은 거부 (합 ≤ 0)."""

    with pytest.raises(ValueError, match="total must be positive"):
        validate_weight_dict({1: 0.0, 2: 0.0}, name="weights")


@pytest.mark.parametrize(
    ("weights", "should_pass"),
    [
        ({1: 0.9}, False),  # 합 0.9 → ±5% 밖
        ({1: 0.95}, False),  # 합 0.95 → IEEE 754 로 strict `> 0.05` 거부 (위 docstring)
        ({1: 1.0}, True),  # 합 1.0 → 정확 통과
        ({1: 1.05}, False),  # 합 1.05 → IEEE 754 로 strict `> 0.05` 거부
        ({1: 1.1}, False),  # 합 1.1 → ±5% 밖
    ],
)
def test_total_tolerance_boundary(weights: dict[int, float], should_pass: bool) -> None:
    """기본 tolerance 0.05 (±5%) 의 경계 5 케이스 — 기존 allocator 의 strict 비교 박제."""

    if should_pass:
        result = validate_weight_dict(weights, name="weights")
        assert result == weights
    else:
        with pytest.raises(ValueError, match="close to 1.0"):
            validate_weight_dict(weights, name="weights")
