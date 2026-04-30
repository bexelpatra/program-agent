"""register_asset 도메인 서비스 단위 테스트 (TASK-236).

검증 목적:
    V3 silent fallback 금지 원칙 — 백필 enqueue 가 raise 했을 때 logger.warning
    으로 흔적이 남고, 등록 자체는 enqueued=False 로 정상 반환되는지 확인.

clean architecture: Protocol 구현을 인메모리 스텁으로 작성하여 DB / yfinance /
스케줄러 의존을 끊는다. caplog fixture 로 로그 emit 을 검증한다.
"""

from __future__ import annotations

import logging
from datetime import date

import pytest

from app.domain.asset.entity import Asset
from app.domain.asset.registration import (
    BackfillEnqueuer,
    RegistrationRequest,
    TickerValidator,
    ValidationOutcome,
    register_asset,
)


# --- 인메모리 스텁 (Protocol 구현) -----------------------------------------


class _StubAssetRepository:
    """find_by_symbol_market 는 항상 None (신규 자산), upsert 는 PK 부여."""

    def __init__(self, assigned_id: int = 42) -> None:
        self._assigned_id = assigned_id
        self.upsert_calls: list[Asset] = []

    def find_by_symbol_market(self, symbol, market):  # type: ignore[no-untyped-def]
        return None

    def upsert(self, asset: Asset) -> Asset:
        self.upsert_calls.append(asset)
        # PK 가 채워진 새 객체 반환 (frozen dataclass 라 dataclasses.replace 사용).
        from dataclasses import replace

        return replace(asset, asset_id=self._assigned_id)

    # 다른 메서드는 본 테스트에서 호출되지 않으므로 정의 생략.


class _StubValidator:
    """validate_ticker 가 정상 outcome 을 반환."""

    def validate_ticker(self, symbol: str) -> ValidationOutcome:
        return ValidationOutcome(
            ticker=symbol.upper(),
            exists=True,
            has_min_history=True,
            earliest_date=date(2020, 1, 1),
            note=None,
        )


class _RaisingEnqueuer:
    """enqueue 호출 시 항상 예외 raise — silent swallow 검증용."""

    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def enqueue(self, asset_id: int) -> None:
        raise self._exc


class _OkEnqueuer:
    def __init__(self) -> None:
        self.calls: list[int] = []

    def enqueue(self, asset_id: int) -> None:
        self.calls.append(asset_id)


# --- 테스트 ----------------------------------------------------------------


def _make_request() -> RegistrationRequest:
    return RegistrationRequest(
        symbol="SPY",
        market="US",
        asset_type="ETF",
        currency="USD",
        name="SPDR S&P 500",
        meta={},
    )


def test_enqueue_failure_logs_warning_and_returns_false(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """enqueue 가 raise 하면 logger.warning emit + enqueued=False (silent swallow 금지)."""
    repo = _StubAssetRepository(assigned_id=42)
    validator = _StubValidator()
    enqueuer = _RaisingEnqueuer(RuntimeError("scheduler down"))

    caplog.set_level(logging.WARNING, logger="app.domain.asset.registration")

    result = register_asset(_make_request(), repo, validator, enqueuer)  # type: ignore[arg-type]

    # 등록 자체는 성공.
    assert result.asset.asset_id == 42
    assert result.asset.symbol == "SPY"
    assert result.backfill_enqueued is False
    assert result.note is not None and "백필 큐잉 실패" in result.note

    # logger.warning emit 검증 — asset_id / symbol / 예외 메시지 포함.
    warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert (
        len(warning_records) == 1
    ), f"expected exactly 1 WARNING, got {len(warning_records)}: {caplog.records}"
    msg = warning_records[0].getMessage()
    assert "42" in msg, f"asset_id=42 missing in log: {msg}"
    assert "SPY" in msg, f"symbol SPY missing in log: {msg}"
    assert "scheduler down" in msg, f"exception message missing in log: {msg}"


def test_enqueue_success_no_warning(caplog: pytest.LogCaptureFixture) -> None:
    """enqueue 정상 케이스 — logger.warning emit 안 됨, enqueued=True."""
    repo = _StubAssetRepository(assigned_id=7)
    validator = _StubValidator()
    enqueuer = _OkEnqueuer()

    caplog.set_level(logging.WARNING, logger="app.domain.asset.registration")

    result = register_asset(_make_request(), repo, validator, enqueuer)  # type: ignore[arg-type]

    assert result.backfill_enqueued is True
    assert enqueuer.calls == [7]
    # WARNING 레코드가 한 건도 없어야 함 (모듈 한정).
    target = [
        r
        for r in caplog.records
        if r.levelno == logging.WARNING and r.name == "app.domain.asset.registration"
    ]
    assert target == [], f"unexpected WARNING records: {target}"


def test_enqueue_failure_value_error_also_logs(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """RuntimeError 외 다른 Exception 종류 (예: ValueError) 도 동일하게 처리."""
    repo = _StubAssetRepository(assigned_id=99)
    validator = _StubValidator()
    enqueuer = _RaisingEnqueuer(ValueError("invalid asset id"))

    caplog.set_level(logging.WARNING, logger="app.domain.asset.registration")

    result = register_asset(_make_request(), repo, validator, enqueuer)  # type: ignore[arg-type]

    assert result.backfill_enqueued is False
    warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warning_records) == 1
    msg = warning_records[0].getMessage()
    assert "99" in msg
    assert "invalid asset id" in msg


# Protocol 구현 호환성 컴파일 타임 체크 (mypy 시 Protocol 매칭).
_REPO_PROTOCOL_HINT: type = _StubAssetRepository
_VALIDATOR_PROTOCOL_HINT: type[TickerValidator] = _StubValidator  # type: ignore[type-abstract]
_ENQUEUER_PROTOCOL_HINT: type[BackfillEnqueuer] = _OkEnqueuer  # type: ignore[type-abstract]
