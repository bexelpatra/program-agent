"""DataSource 어댑터 공용 헬퍼.

yfinance / pykrx 어댑터가 동일하게 필요로 하는 두 가지 관심사를 응집한다:

1. **호출 간격 보장 (RateLimiter)** — V1 결정 9. 어댑터별 sleep 간격 (yfinance 0.5s,
   pykrx 0.1s) 만 다를 뿐 로직은 동일. 인스턴스로 격리해 모듈 간 락 공유 없이도
   각 어댑터가 독립된 호출 간격을 갖는다.
2. **수집 레이어 close 거부 정책 (is_invalid_close)** — architecture.md V3
   § "비거래일 방어" 1단계. 어댑터 종류 무관하게 동일.
3. **None/NaN-safe float 변환 (safe_float)** — pandas / external API 응답에서
   누락치를 None 으로 정규화한다. 일부 어댑터(pykrx)가 비숫자 객체를 돌려줄 수
   있어 try/except 를 포함한 안전한 구현으로 통일한다.
"""
from __future__ import annotations

import time
from threading import Lock
from typing import Any


def _is_nan(value: Any) -> bool:
    """NaN 검출 — float NaN 은 자기 자신과 같지 않다.

    pandas Timestamp 등 비교 자체가 예외를 던질 수 있는 타입을 안전하게 흡수.
    """
    try:
        return value != value
    except Exception:  # noqa: BLE001 - 외부 타입 다양성 흡수
        return False


def safe_float(value: Any) -> float | None:
    """None/NaN → None, 그 외 → float.

    pykrx 가 가끔 비숫자 객체를 row.get 으로 돌려줘 float() 가 raise 할 수 있어
    TypeError/ValueError 를 None 으로 흡수한다 (안전한 쪽 통일).
    """
    if value is None or _is_nan(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def is_invalid_close(close: Any) -> bool:
    """수집 레이어 close 거부 정책: None / NaN / 0 → invalid.

    음수는 현재 정책상 invalid 가 아니다 (거래소 데이터에 음수 close 없음).
    """
    if close is None or _is_nan(close):
        return True
    try:
        return float(close) == 0.0
    except (TypeError, ValueError):
        return True


class RateLimiter:
    """모듈 단위 호출 간격 보장. 멀티스레드 안전.

    인스턴스마다 독립된 lock + 마지막 호출 시각을 보유하므로 어댑터별로
    별도의 RateLimiter 를 두면 호출 간격이 서로 간섭하지 않는다.
    """

    def __init__(self, min_interval_sec: float) -> None:
        self._min_interval_sec = min_interval_sec
        self._lock = Lock()
        self._last_call_monotonic = 0.0

    def wait(self) -> None:
        """직전 wait() 호출 이후 최소 min_interval_sec 가 경과하도록 sleep."""
        with self._lock:
            elapsed = time.monotonic() - self._last_call_monotonic
            if elapsed < self._min_interval_sec:
                time.sleep(self._min_interval_sec - elapsed)
            self._last_call_monotonic = time.monotonic()
