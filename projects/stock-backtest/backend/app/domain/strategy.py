"""전략 인터페이스 (3요소 조합) + Allocator/SignalFilter Protocol.

Quant Lab CLAUDE.md L10-15 (3요소 조합):
- allocator: 비중 결정 규칙 (FixedWeight, AllWeather, EqualWeight)
- signal_filters[]: 보유 자격 필터 (AND), MovingAverage / Momentum
- rebalance_schedule: daily / weekly / monthly / quarterly / yearly / signal_event

architecture.md V3 § "거래 정책" 모델 A (L615-630):
- D 일 종가 → 시그널 판정
- D+1 일 시가 → 체결
- generate_weights / is_eligible 호출 시 prices_until_d 는 D 까지만 (engine.py 의
  prices_aligned.loc[:d] 슬라이싱이 D+1 노출 차단). 이 인터페이스는 Allocator/Filter
  구현체가 인자로 받은 prices_until_d 만 신뢰하도록 강제하는 설계.

분리 원칙 (V3 § L654-666):
- strategy.py: 인터페이스 (Protocol) + 합성 함수 (apply_filters_and_allocator)
- engine.py: 시간 루프 + 모델 A 강제 슬라이싱
- allocators/, filters/: Protocol 구현체 (TASK-050~054)

도메인 순수: SQLAlchemy/HTTP/외부 라이브러리 import 금지. pandas 는 시계열 기본 자료구조로
도메인 본질에 가까워 허용 (portfolio.py / trade.py 와 동일 정책).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal, Protocol

import pandas as pd

# rebalance_schedule 허용값 (Quant Lab CLAUDE.md L13).
RebalanceSchedule = Literal[
    "daily",
    "weekly",
    "monthly",
    "quarterly",
    "yearly",
    "signal_event",
]


class Allocator(Protocol):
    """비중 결정. universe + 가격 (D 일까지) → asset_id → 목표 비중 (0~1).

    구현체:
    - FixedWeightAllocator (TASK-050): 사용자 지정 고정 비중
    - AllWeatherAllocator (TASK-051): 표준 5자산 비중
    - EqualWeightAllocator (TASK-052): 1/N

    `name` 은 카탈로그/설정 직렬화용 식별자 (snake_case).
    `required_universe()` 는 allocator 가 필수로 요구하는 asset_id 목록 — 빈 리스트면
    universe 자유 (예: EqualWeight). AllWeather 는 정해진 자산 부재 시 명시적 에러
    (engine 호출 전 universe 검증에서 확인).
    """

    name: str

    def required_universe(self) -> list[int]:
        """이 allocator 가 필수로 요구하는 asset_id 목록. 빈 리스트면 universe 자유."""
        ...

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        """asset_id → 목표 비중 (0~1).

        Args:
            universe_asset_ids: 필터 통과한 자산 목록 (apply_filters_and_allocator 가
                필터링 후 전달). 빈 리스트면 호출되지 않음.
            prices_until_d: index=date (오름차순), columns=asset_id, values=close.
                D 일 (signal_date) 까지만. **engine 이 슬라이싱 책임 — Allocator 는
                추가 슬라이싱하지 말 것.**
            signal_date: 시그널 판정 일자 (D). 인덱싱 보조용.

        Returns:
            asset_id → 비중 (Decimal). 합 ≤ 1 권장 (남은 비중은 base cash). 합이
            정확히 1 이 아니어도 호출자(trade.execute_rebalance) 가 처리 가능.
        """
        ...


class SignalFilter(Protocol):
    """자산별 보유 자격 필터. AND 로 결합 — 모든 필터 통과해야 universe 에 포함.

    구현체:
    - MovingAverageFilter (TASK-053): 가격 > MA(window)
    - MomentumFilter (TASK-054): lookback 수익률 > 임계값

    `name` 은 카탈로그/설정 직렬화용 식별자 (snake_case).
    """

    name: str

    def is_eligible(
        self,
        asset_id: int,
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> bool:
        """asset_id 가 signal_date 시점에 보유 가능한지.

        Args:
            asset_id: 평가 대상 자산.
            prices_until_d: D 까지의 가격 (Allocator 와 동일 슬라이싱 규약).
            signal_date: D.

        Returns:
            True 면 universe 포함 후보, False 면 제외.
        """
        ...


@dataclass(frozen=True)
class Strategy:
    """3요소 조합. 단일 Strategy 객체 = 단일 백테스트 전략 정의.

    - allocator: 단일 Allocator (조합 단계에서 1개만 선택).
    - signal_filters: tuple of SignalFilter (AND 결합, 빈 tuple 허용 = 필터 없음).
    - rebalance_schedule: 6가지 중 1개.

    name 은 사용자 표시/저장용 (예: "올웨더 월간 리밸런싱").
    """

    name: str
    allocator: Allocator
    signal_filters: tuple[SignalFilter, ...]
    rebalance_schedule: RebalanceSchedule


def apply_filters_and_allocator(
    strategy: Strategy,
    universe_asset_ids: list[int],
    prices_until_d: pd.DataFrame,
    signal_date: date,
) -> dict[int, Decimal]:
    """전략 = signal_filters (AND) → allocator. 합성 함수.

    1. universe_asset_ids 중 모든 필터를 통과한 자산만 추림 (AND).
    2. 통과한 자산이 없으면 빈 dict (호출자=engine 이 cash-only 로 해석).
    3. 통과한 자산에 대해 allocator.generate_weights 호출.

    Args:
        strategy: 3요소 조합.
        universe_asset_ids: 백테스트 universe 전체 (사용자가 선택한 자산).
        prices_until_d: D 까지의 가격 (engine 이 prices_aligned.loc[:d] 로 슬라이싱).
        signal_date: D (시그널 판정 일자).

    Returns:
        asset_id → 목표 비중. 빈 dict 면 전부 cash 보유.
    """
    if not universe_asset_ids:
        return {}

    eligible = [
        aid
        for aid in universe_asset_ids
        if all(
            f.is_eligible(aid, prices_until_d, signal_date)
            for f in strategy.signal_filters
        )
    ]
    if not eligible:
        return {}

    return strategy.allocator.generate_weights(eligible, prices_until_d, signal_date)
