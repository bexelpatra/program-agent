"""전략 레지스트리 및 자동 스캔 모듈.

이 모듈은 ``static/``, ``dynamic/`` 하위 패키지에 정의된 전략 클래스를
자동으로 import하여 전역 레지스트리에 등록한다. 웹 UI와 CLI는 이 레지
스트리를 통해 사용 가능한 전략 목록을 얻는다.

설계 배경
---------
- architecture.md 설계 결정 #8: 파일 드롭으로 전략 추가 → 즉시 UI 노출.
- 임의 Python 코드 업로드 기능은 제공하지 않는다 (보안).

사용 예시
---------
>>> from stock_backtest.strategies.base import Strategy, StrategyParams
>>> from stock_backtest.strategies.registry import (
...     register, discover_strategies, list_strategies, get_strategy,
... )
>>> class MyParams(StrategyParams):
...     lookback: int = 12
>>> @register
... class MyStrategy(Strategy):
...     name = "my_strategy"
...     params_schema = MyParams
...     def generate_weights(self, prices, rebalance_dates): ...
...     def required_universe(self): return None
>>> discover_strategies()           # static/, dynamic/ 재귀 import
>>> list_strategies()               # ['my_strategy', ...]
>>> cls = get_strategy("my_strategy")
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import TypeVar

from stock_backtest.strategies.base import Strategy

__all__ = [
    "STRATEGY_REGISTRY",
    "register",
    "discover_strategies",
    "get_strategy",
    "list_strategies",
]

STRATEGY_REGISTRY: dict[str, type[Strategy]] = {}
"""전략 이름 → 전략 클래스 매핑.

:func:`register` 데코레이터 또는 :func:`discover_strategies`에 의해
자동으로 채워진다. 직접 수정하지 말 것.
"""

_T = TypeVar("_T", bound=type[Strategy])


def register(cls: _T) -> _T:
    """전략 클래스를 전역 레지스트리에 등록하는 데코레이터.

    Parameters
    ----------
    cls : type[Strategy]
        등록할 전략 클래스. 클래스 속성 ``name``이 반드시 정의되어
        있어야 한다.

    Returns
    -------
    type[Strategy]
        입력받은 클래스를 그대로 반환 (데코레이터 패턴).

    Raises
    ------
    TypeError
        ``cls``가 :class:`Strategy`의 서브클래스가 아니거나 ``name``
        속성이 없는 경우.
    ValueError
        동일한 ``name``으로 이미 다른 클래스가 등록되어 있는 경우.
        (같은 클래스의 재등록은 멱등 처리.)
    """
    if not isinstance(cls, type) or not issubclass(cls, Strategy):
        raise TypeError(f"register() expects a Strategy subclass, got {cls!r}")
    name = getattr(cls, "name", None)
    if not isinstance(name, str) or not name:
        raise TypeError(
            f"Strategy class {cls.__name__} must define a non-empty "
            f"class attribute 'name'"
        )

    existing = STRATEGY_REGISTRY.get(name)
    if existing is not None and existing is not cls:
        raise ValueError(
            f"Strategy name '{name}' is already registered by "
            f"{existing.__module__}.{existing.__name__}; cannot re-register "
            f"with {cls.__module__}.{cls.__name__}"
        )

    STRATEGY_REGISTRY[name] = cls
    return cls


def discover_strategies(
    package: str = "stock_backtest.strategies",
) -> list[str]:
    """하위 모듈을 재귀적으로 import하여 전략을 자동 등록한다.

    Parameters
    ----------
    package : str, optional
        스캔할 루트 패키지의 dotted name. 기본값
        ``"stock_backtest.strategies"``.

    Returns
    -------
    list[str]
        import에 성공한 모듈 이름 목록.

    Notes
    -----
    - ``static/``와 ``dynamic/``를 포함한 모든 하위 모듈이 대상이다.
    - 각 전략 모듈은 정의 시점에 :func:`register` 데코레이터를 통해
      ``STRATEGY_REGISTRY``에 등록된다.
    - 이미 import된 모듈은 다시 import해도 멱등이다.
    """
    imported: list[str] = []
    root = importlib.import_module(package)
    root_paths = getattr(root, "__path__", None)
    if root_paths is None:
        return imported

    for mod_info in pkgutil.walk_packages(
        path=root_paths,
        prefix=f"{package}.",
    ):
        # base, registry 자체는 재import할 필요 없음 (이미 로드됨).
        if mod_info.name in {
            f"{package}.base",
            f"{package}.registry",
        }:
            continue
        importlib.import_module(mod_info.name)
        imported.append(mod_info.name)
    return imported


def get_strategy(name: str) -> type[Strategy]:
    """이름으로 전략 클래스를 조회한다.

    Parameters
    ----------
    name : str
        조회할 전략 이름.

    Returns
    -------
    type[Strategy]
        등록된 전략 클래스.

    Raises
    ------
    KeyError
        해당 이름의 전략이 등록되어 있지 않은 경우. 사용 가능한
        전략 목록이 에러 메시지에 포함된다.
    """
    try:
        return STRATEGY_REGISTRY[name]
    except KeyError as exc:
        available = ", ".join(sorted(STRATEGY_REGISTRY)) or "(none)"
        raise KeyError(f"Strategy '{name}' not found. Available: {available}") from exc


def list_strategies() -> list[str]:
    """등록된 전략 이름 목록을 정렬하여 반환한다.

    Returns
    -------
    list[str]
        레지스트리에 등록된 전략 이름들 (알파벳순).
    """
    return sorted(STRATEGY_REGISTRY)
