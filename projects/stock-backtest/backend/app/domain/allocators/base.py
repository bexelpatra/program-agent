"""Allocator 베이스 클래스.

architecture.md V3 § "Phase 1 MVP" L728 + Quant Lab CLAUDE.md L26 (FixedWeight) 근거.
strategy.py 의 `Allocator` Protocol (TASK-043) 을 구현하는 모든 allocator 의 공통 베이스.

설계 의도:
- params_schema (pydantic BaseModel 클래스) 를 ClassVar 로 보유 → UI 가 JSON Schema
  변환해 폼을 자동 생성 (V3 § "절대원칙 1 - JSON 노출 금지" 충족: 사용자에게는
  폼만 노출, JSON 은 내부 저장 형식).
- __init__(params: P) 로 검증된 pydantic 인스턴스만 받아 인스턴스 변수에 저장
  → 잘못된 입력은 pydantic 단계에서 차단.
- generate_weights 는 abstract — 서브클래스가 강제로 구현해야 함.
- required_universe 디폴트는 빈 리스트 (universe 자유). AllWeather 처럼 특정
  자산을 강제하는 allocator 만 override.

도메인 순수: SQLAlchemy/HTTP/외부 라이브러리 import 금지. pandas/pydantic 만 허용
(strategy.py L20-21 와 동일 정책).
"""

from __future__ import annotations

from abc import abstractmethod
from datetime import date
from decimal import Decimal
from typing import ClassVar, Generic, TypeVar

import pandas as pd
from pydantic import BaseModel

P = TypeVar("P", bound=BaseModel)


class AllocatorBase(Generic[P]):
    """Allocator Protocol 의 공통 베이스.

    Attributes:
        name: snake_case 식별자 (카탈로그/직렬화용). 서브클래스가 ClassVar 로 정의.
        params_schema: pydantic BaseModel 클래스. UI 폼 생성용 JSON Schema 원천.
        params: __init__ 에 전달된 검증된 params 인스턴스.

    Subclass 책임:
        1. `name: ClassVar[str]` 정의
        2. `params_schema: ClassVar[type[BaseModel]]` 정의
        3. `generate_weights` 구현
        4. (선택) `required_universe` override
    """

    name: ClassVar[str]
    params_schema: ClassVar[type[BaseModel]]

    def __init__(self, params: P):
        self.params = params

    def required_universe(self) -> list[int]:
        """이 allocator 가 필수로 요구하는 asset_id 목록.

        디폴트는 빈 리스트 (universe 자유 - 어떤 자산이든 허용).
        AllWeather 등 특정 자산을 강제하는 allocator 가 override.
        """
        return []

    @abstractmethod
    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        """asset_id → 목표 비중 (0~1).

        Args:
            universe_asset_ids: 필터 통과한 자산 목록.
            prices_until_d: index=date (오름차순), columns=asset_id, values=close.
                D 일 (signal_date) 까지만. **engine 이 슬라이싱 책임 — Allocator 는
                추가 슬라이싱하지 말 것.** (strategy.py L75-77 와 동일 규약)
            signal_date: 시그널 판정 일자 (D).

        Returns:
            asset_id → 비중 (Decimal). 합 ≈ 1 권장.
        """
        ...


def normalize_weights(
    weights: dict[int, Decimal],
    allow_cash_slot: bool = True,
) -> dict[int, Decimal]:
    """비중 합 검증 + 정규화.

    Args:
        weights: asset_id → 비중. _CASH_ 슬리브 (asset_id = 0 또는 -1) 허용 시
            allow_cash_slot=True (현재 디폴트, future-proof).
        allow_cash_slot: True 면 음수가 아닌 한 0/-1 asset_id 도 허용.
            False 면 호출자가 직접 검증해야 함.

    Returns:
        - weights 가 비어있거나 합이 0 이하면 빈 dict.
        - 합이 이미 1 ± 1bp 안이면 그대로 반환.
        - 그 외에는 합으로 나눠 정규화.

    Note:
        allow_cash_slot 파라미터는 future-proof 용으로 받아두지만 현재 구현은
        cash 슬롯 분리 로직을 두지 않는다 (호출자가 weights dict 에 cash slot
        을 포함시켜 넘기는 것을 허용). 추후 정책이 정해지면 여기서 분기.
    """
    total = sum(weights.values(), Decimal("0"))
    if total <= Decimal("0"):
        return {}
    if abs(total - Decimal("1")) < Decimal("0.01"):
        return weights
    return {aid: w / total for aid, w in weights.items()}
