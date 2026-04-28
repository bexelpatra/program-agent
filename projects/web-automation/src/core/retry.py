"""재시도 데코레이터 모듈.

동기/비동기 함수에 지수 백오프 기반 재시도 로직을 적용하는
데코레이터를 제공한다. Config에서 기본값을 읽거나,
데코레이터 인자로 직접 제어할 수 있다.
"""

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Tuple, Type, TypeVar

logger = logging.getLogger(__name__)

# 기본 설정값 (Config가 없을 때 폴백)
_DEFAULT_MAX_ATTEMPTS = 3
_DEFAULT_DELAY = 2.0
_DEFAULT_BACKOFF_FACTOR = 2.0

F = TypeVar("F", bound=Callable[..., Any])


def _resolve_defaults(
    max_attempts: int | None,
    delay: float | None,
    backoff_factor: float | None,
) -> tuple[int, float, float]:
    """Config 참조 키에서 기본값을 가져오고, 명시적 인자로 오버라이드한다.

    Config 로드 실패 시 하드코딩된 폴백값을 사용한다.

    Args:
        max_attempts: 최대 재시도 횟수 (None이면 Config/폴백값 사용)
        delay: 초기 대기 시간 (None이면 Config/폴백값 사용)
        backoff_factor: 지수 백오프 배수 (None이면 Config/폴백값 사용)

    Returns:
        (max_attempts, delay, backoff_factor) 튜플
    """
    # Config에서 기본값 조회 시도
    config_max = _DEFAULT_MAX_ATTEMPTS
    config_delay = _DEFAULT_DELAY
    config_backoff = _DEFAULT_BACKOFF_FACTOR

    try:
        from src.core.config import Config

        cfg = Config()
        val = cfg.get("retry.max_attempts")
        if val is not None:
            config_max = int(val)
        val = cfg.get("retry.delay")
        if val is not None:
            config_delay = float(val)
        val = cfg.get("retry.backoff_factor")
        if val is not None:
            config_backoff = float(val)
    except Exception:
        # Config 로드 실패 시 폴백값 사용 (설정 파일 없음 등)
        pass

    return (
        max_attempts if max_attempts is not None else config_max,
        delay if delay is not None else config_delay,
        backoff_factor if backoff_factor is not None else config_backoff,
    )


def retry(
    max_attempts: int | None = None,
    delay: float | None = None,
    backoff_factor: float | None = None,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable[[F], F]:
    """동기 함수에 재시도 로직을 적용하는 데코레이터.

    지수 백오프 방식으로 대기 시간을 증가시키며,
    지정된 예외 타입에 대해서만 재시도한다.

    Args:
        max_attempts: 최대 시도 횟수 (None이면 Config 기본값 사용)
        delay: 첫 실패 후 대기 시간(초) (None이면 Config 기본값 사용)
        backoff_factor: 대기 시간 증가 배수 (None이면 Config 기본값 사용)
        exceptions: 재시도 대상 예외 타입 튜플

    Returns:
        데코레이터 함수

    사용 예시::

        @retry(max_attempts=3, delay=1, exceptions=(TimeoutError,))
        def unstable_operation():
            ...
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            resolved_max, resolved_delay, resolved_backoff = _resolve_defaults(
                max_attempts, delay, backoff_factor
            )
            current_delay = resolved_delay
            last_exception: BaseException | None = None

            for attempt in range(1, resolved_max + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt < resolved_max:
                        logger.warning(
                            "[retry] %s - 시도 %d/%d 실패: %s. " "%.1f초 후 재시도합니다.",
                            func.__name__,
                            attempt,
                            resolved_max,
                            exc,
                            current_delay,
                        )
                        time.sleep(current_delay)
                        current_delay *= resolved_backoff
                    else:
                        logger.error(
                            "[retry] %s - 시도 %d/%d 실패: %s. " "최대 재시도 횟수에 도달했습니다.",
                            func.__name__,
                            attempt,
                            resolved_max,
                            exc,
                        )

            # 모든 시도 실패 시 마지막 예외를 그대로 raise
            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


def async_retry(
    max_attempts: int | None = None,
    delay: float | None = None,
    backoff_factor: float | None = None,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable[[F], F]:
    """비동기 함수에 재시도 로직을 적용하는 데코레이터.

    지수 백오프 방식으로 대기 시간을 증가시키며,
    지정된 예외 타입에 대해서만 재시도한다.
    대기에는 asyncio.sleep을 사용한다.

    Args:
        max_attempts: 최대 시도 횟수 (None이면 Config 기본값 사용)
        delay: 첫 실패 후 대기 시간(초) (None이면 Config 기본값 사용)
        backoff_factor: 대기 시간 증가 배수 (None이면 Config 기본값 사용)
        exceptions: 재시도 대상 예외 타입 튜플

    Returns:
        데코레이터 함수

    사용 예시::

        @async_retry(max_attempts=5, backoff_factor=1.5)
        async def async_unstable():
            ...
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            resolved_max, resolved_delay, resolved_backoff = _resolve_defaults(
                max_attempts, delay, backoff_factor
            )
            current_delay = resolved_delay
            last_exception: BaseException | None = None

            for attempt in range(1, resolved_max + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt < resolved_max:
                        logger.warning(
                            "[async_retry] %s - 시도 %d/%d 실패: %s. " "%.1f초 후 재시도합니다.",
                            func.__name__,
                            attempt,
                            resolved_max,
                            exc,
                            current_delay,
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= resolved_backoff
                    else:
                        logger.error(
                            "[async_retry] %s - 시도 %d/%d 실패: %s. " "최대 재시도 횟수에 도달했습니다.",
                            func.__name__,
                            attempt,
                            resolved_max,
                            exc,
                        )

            # 모든 시도 실패 시 마지막 예외를 그대로 raise
            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator
