"""사용자 요청 백테스트 기간 ↔ universe 데이터 가용 구간 비교 + 자동 조정.

architecture.md V3 § "universe 시작일 불일치" L545-547 근거.
TASK-030 산출물 `Universe.common_period()` 위에 사용자 명시 기간 비교, 한국어 통지
메시지 생성 책임을 추가한다.

UI/UX 원칙:
- 원칙 2: 한국어 메시지로 사용자에게 통지.
- 원칙 3: PeriodAdjustment dataclass 가 진행 상태를 그대로 노출.

도메인 순수: stdlib + Universe/Asset 엔티티만 import.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

from .entity import Universe

AdjustmentReason = Literal[
    "universe_start_later",
    "universe_end_earlier",
    "no_data",
    "ok",
]


@dataclass(frozen=True)
class PeriodAdjustment:
    """사용자가 요청한 (start, end) 와 universe 데이터 가용 구간 비교 결과.

    UI 가 이 객체를 그대로 사용자에게 통지 메시지로 노출 (UI/UX 원칙 3 진행 상태 가시화).

    Attributes:
        requested_start: 사용자가 폼에서 선택한 시작일.
        requested_end: 사용자가 폼에서 선택한 종료일.
        adjusted_start: universe 데이터 가용 구간을 반영해 조정된 시작일.
        adjusted_end: universe 데이터 가용 구간을 반영해 조정된 종료일.
        reason: 조정 사유 분류.
        message: 한국어 사용자 통지 메시지.
        affected_assets: 조정 원인이 된 자산 symbol 튜플.
    """

    requested_start: date
    requested_end: date
    adjusted_start: date
    adjusted_end: date
    reason: AdjustmentReason
    message: str
    affected_assets: tuple[str, ...]

    @property
    def was_adjusted(self) -> bool:
        """요청 기간이 실제로 조정됐는지 여부."""
        return (
            self.requested_start != self.adjusted_start
            or self.requested_end != self.adjusted_end
        )


def adjust_period_for_universe(
    universe: Universe,
    requested_start: date,
    requested_end: date,
) -> PeriodAdjustment:
    """universe 자산 가용 구간과 사용자 요청 기간을 비교해 조정 결과 + 한국어 메시지 생성.

    조정 규칙:
    - 빈 universe → reason=no_data, 한국어 안내.
    - universe 자산 중 start_date None (백필 미완) 이 있으면 → reason=no_data,
      adjusted=requested 그대로. 호출자가 백필 안내 후 재시도 처리.
    - 자산 중 가장 늦은 start_date 가 requested_start 보다 늦으면
      → adjusted_start 갱신, reason=universe_start_later.
    - 자산 중 가장 이른 last_ingested_at (None 인 자산은 today 로 간주) 이 requested_end 보다
      이르면 → adjusted_end 갱신, reason=universe_end_earlier.
    - 양쪽 다 조정되면 reason=universe_start_later (시작일 우선) 로 묶어 메시지에 둘 다 표기.
    - 둘 다 조정 없음 → reason=ok, was_adjusted=False.

    Args:
        universe: 비교 대상 universe.
        requested_start: 사용자 요청 시작일 (포함).
        requested_end: 사용자 요청 종료일 (포함).

    Returns:
        PeriodAdjustment.
    """
    if not universe.assets:
        return PeriodAdjustment(
            requested_start=requested_start,
            requested_end=requested_end,
            adjusted_start=requested_start,
            adjusted_end=requested_end,
            reason="no_data",
            message="universe 가 비어 있습니다. 자산을 1개 이상 추가하세요.",
            affected_assets=(),
        )

    # 백필 미완 자산 탐지
    no_data_assets = tuple(
        a.symbol for a in universe.assets if a.start_date is None
    )
    if no_data_assets:
        return PeriodAdjustment(
            requested_start=requested_start,
            requested_end=requested_end,
            adjusted_start=requested_start,
            adjusted_end=requested_end,
            reason="no_data",
            message=(
                f"다음 자산의 데이터가 아직 백필되지 않았습니다: "
                f"{', '.join(no_data_assets)}. 백필 완료 후 백테스트를 시도하세요."
            ),
            affected_assets=no_data_assets,
        )

    # 가장 늦은 start_date 와 가장 이른 last_ingested_at 탐색
    # mypy/타입체커 안심: 위에서 None 인 자산은 모두 걸러졌으므로 a.start_date 는 not None.
    latest_start = max(a.start_date for a in universe.assets if a.start_date is not None)
    earliest_end = min(
        a.last_ingested_at.date() if a.last_ingested_at is not None else date.today()
        for a in universe.assets
    )

    adjusted_start = max(requested_start, latest_start)
    adjusted_end = min(requested_end, earliest_end)

    start_was_adjusted = adjusted_start > requested_start
    end_was_adjusted = adjusted_end < requested_end

    affected_start = tuple(
        a.symbol
        for a in universe.assets
        if a.start_date == latest_start and start_was_adjusted
    )
    affected_end = tuple(
        a.symbol
        for a in universe.assets
        if (
            (a.last_ingested_at.date() if a.last_ingested_at is not None else date.today())
            == earliest_end
        )
        and end_was_adjusted
    )

    if start_was_adjusted and end_was_adjusted:
        message = (
            f"기간이 자동 조정됐습니다: {adjusted_start} ~ {adjusted_end}. "
            f"시작일은 {', '.join(affected_start)}, "
            f"종료일은 {', '.join(affected_end)} 의 데이터 가용 구간 때문입니다."
        )
        # reason 우선순위: 시작일 조정이 더 임팩트가 크므로 universe_start_later 로 통합.
        return PeriodAdjustment(
            requested_start=requested_start,
            requested_end=requested_end,
            adjusted_start=adjusted_start,
            adjusted_end=adjusted_end,
            reason="universe_start_later",
            message=message,
            affected_assets=affected_start + affected_end,
        )
    if start_was_adjusted:
        message = (
            f"시작일이 {adjusted_start} 로 자동 조정됐습니다. "
            f"{', '.join(affected_start)} 의 데이터 시작일이 {latest_start} 이기 때문입니다."
        )
        return PeriodAdjustment(
            requested_start=requested_start,
            requested_end=requested_end,
            adjusted_start=adjusted_start,
            adjusted_end=adjusted_end,
            reason="universe_start_later",
            message=message,
            affected_assets=affected_start,
        )
    if end_was_adjusted:
        message = (
            f"종료일이 {adjusted_end} 로 자동 조정됐습니다. "
            f"{', '.join(affected_end)} 의 마지막 백필일이 {earliest_end} 이기 때문입니다."
        )
        return PeriodAdjustment(
            requested_start=requested_start,
            requested_end=requested_end,
            adjusted_start=adjusted_start,
            adjusted_end=adjusted_end,
            reason="universe_end_earlier",
            message=message,
            affected_assets=affected_end,
        )

    return PeriodAdjustment(
        requested_start=requested_start,
        requested_end=requested_end,
        adjusted_start=adjusted_start,
        adjusted_end=adjusted_end,
        reason="ok",
        message="기간이 사용자 요청대로 적용됐습니다.",
        affected_assets=(),
    )
