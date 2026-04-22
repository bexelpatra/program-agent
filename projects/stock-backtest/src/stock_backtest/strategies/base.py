"""전략(Strategy) 추상 베이스 모듈.

이 모듈은 백테스트 플랫폼의 모든 전략이 구현해야 하는 공통 인터페이스를
정의한다. 각 전략은 :class:`Strategy`를 상속하고, 전략별 파라미터는
:class:`StrategyParams`를 상속한 pydantic 모델로 선언한다.

설계 배경
---------
- architecture.md의 설계 결정 #8 참조.
- 파라미터는 pydantic 스키마로 선언하여 웹 UI가 자동으로 입력 폼을
  생성할 수 있도록 한다.
- ``generate_weights``는 리밸런싱 시점별 목표 비중 행렬을 반환한다
  (행=리밸런싱일, 열=자산 심볼, 값=비중, 합계=1).
- ``required_universe``는 전략이 특정 자산 심볼에 한정되는 경우를 표현
  한다. 사용자가 임의 universe를 지정할 수 있는 전략은 ``None``을 반환
  한다.

사용 예시
---------
>>> from stock_backtest.strategies.base import Strategy, StrategyParams
>>> from stock_backtest.strategies.registry import register
>>> class MyParams(StrategyParams):
...     lookback: int = 12
>>> @register
... class MyStrategy(Strategy):
...     name = "my_strategy"
...     params_schema = MyParams
...     description = "예시 전략"
...     def generate_weights(self, prices, rebalance_dates):
...         ...
...     def required_universe(self):
...         return None
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel, ConfigDict


class StrategyParams(BaseModel):
    """전략 파라미터의 pydantic 기본 베이스.

    각 전략은 이 클래스를 상속하여 자신만의 파라미터 스키마를 정의한다.
    타입 힌트와 기본값을 선언하면 웹 UI에서 자동으로 입력 폼이 생성된다.

    Notes
    -----
    - ``extra="forbid"``: 선언되지 않은 파라미터가 들어오면 검증 실패.
    - ``validate_assignment=True``: 속성 할당 시에도 검증을 수행.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        frozen=False,
    )


class Strategy(ABC):
    """모든 백테스트 전략의 추상 베이스 클래스.

    Attributes
    ----------
    name : str
        전략 식별자. registry에서 키로 사용되므로 전역적으로 고유해야 한다.
        소문자 + 언더스코어 권장 (예: ``"fixed_weight"``).
    params_schema : type[StrategyParams]
        이 전략이 사용하는 파라미터 스키마 클래스.
    description : str
        전략에 대한 사람이 읽을 수 있는 설명. 웹 UI에서 노출된다.

    Parameters
    ----------
    params : StrategyParams
        이 전략의 ``params_schema`` 인스턴스. 검증된 파라미터 값.
    """

    name: ClassVar[str]
    params_schema: ClassVar[type[StrategyParams]]
    description: ClassVar[str] = ""

    def __init__(self, params: StrategyParams) -> None:
        """전략 인스턴스를 초기화한다.

        Parameters
        ----------
        params : StrategyParams
            ``params_schema``의 인스턴스. 호출 측에서 생성·검증 후 넘긴다.

        Raises
        ------
        TypeError
            ``params``가 ``params_schema``의 인스턴스가 아닌 경우.
        """
        if not isinstance(params, self.params_schema):
            raise TypeError(
                f"Strategy {type(self).__name__} expected params of type "
                f"{self.params_schema.__name__}, got {type(params).__name__}"
            )
        self.params: StrategyParams = params

    @abstractmethod
    def generate_weights(
        self,
        prices: pd.DataFrame,
        rebalance_dates: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        """리밸런싱 시점별 목표 자산 비중을 산출한다.

        Parameters
        ----------
        prices : pd.DataFrame
            일별 가격 시계열. 인덱스는 ``DatetimeIndex``, 컬럼은 자산
            심볼. 값은 수정 종가(adjusted close) 기준.
        rebalance_dates : pd.DatetimeIndex
            리밸런싱을 수행할 일자 목록 (거래일 캘린더 기준).

        Returns
        -------
        pd.DataFrame
            인덱스=``rebalance_dates``, 컬럼=자산 심볼, 값=목표 비중
            (0~1 사이, 행 합계=1). 쇼트 포지션을 쓰는 전략은 음수를
            허용할 수 있으나 기본 구현체는 롱 온리.
        """

    @abstractmethod
    def required_universe(self) -> list[str] | None:
        """이 전략이 강제하는 자산 universe를 반환한다.

        Returns
        -------
        list[str] | None
            특정 심볼 목록이 필요한 전략(예: 올웨더)은 해당 심볼들을
            반환. 사용자 지정 universe를 허용하는 전략은 ``None``.
        """
