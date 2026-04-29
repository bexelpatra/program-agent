"""SignalFilter 베이스. allocator 와 동일하게 pydantic params_schema 패턴.

architecture.md V3 § "Phase 1 MVP" L728 + Quant Lab CLAUDE.md L26 (MovingAverage filter).

- name: ClassVar[str] — 카탈로그/직렬화 식별자 (snake_case).
- params_schema: ClassVar[type[BaseModel]] — 파라미터 스키마 (UI 폼 생성/검증).
- is_eligible: 자산별 독립 적용 (engine 이 자산별로 호출).

도메인 순수: SQLAlchemy/HTTP import 금지. pandas 는 시계열 자료구조로 허용.
"""

from __future__ import annotations

from abc import abstractmethod
from datetime import date
from typing import ClassVar, Generic, TypeVar

import pandas as pd
from pydantic import BaseModel

P = TypeVar("P", bound=BaseModel)


class SignalFilterBase(Generic[P]):
    """SignalFilter Protocol 의 공통 베이스.

    구현체는 `name`, `params_schema`, `is_eligible` 을 정의해야 한다.
    자산별 독립 적용 — engine 이 universe 의 각 자산별로 호출.

    strategy.py 의 SignalFilter Protocol (name + is_eligible) 을 자동 만족.
    """

    name: ClassVar[str]
    params_schema: ClassVar[type[BaseModel]]

    def __init__(self, params: P):
        self.params = params

    @abstractmethod
    def is_eligible(
        self,
        asset_id: int,
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> bool:
        """asset_id 가 signal_date 시점에 보유 가능한지.

        Args:
            asset_id: 평가 대상 자산.
            prices_until_d: index=date, columns=asset_id, values=close.
                D 일 (signal_date) 까지만 (engine 슬라이싱 책임).
            signal_date: D.

        Returns:
            True 면 universe 포함 후보, False 면 제외.
        """
        ...
