"""Asset 도메인 패키지.

architecture.md V3 § "자산 도메인 모델" 의 도메인 레이어. SQLAlchemy/HTTP 등 외부 의존을
배제한 순수 엔티티 + Repository Protocol + 거래일 정책을 정의한다.

data 레이어 (`app.data.asset_repository`) 가 이 Protocol 을 구현하여 의존성 역전을 이룬다.
"""
from app.domain.asset.entity import Asset, AssetType, Market, Universe
from app.domain.asset.repository import AssetRepository
from app.domain.asset.calendar_guard import GuardMode, guard_trading_day, is_trading_day
from app.domain.asset.period_adjustment import (
    AdjustmentReason,
    PeriodAdjustment,
    adjust_period_for_universe,
)

__all__ = [
    "Asset",
    "AssetType",
    "Market",
    "Universe",
    "AssetRepository",
    "GuardMode",
    "guard_trading_day",
    "is_trading_day",
    "AdjustmentReason",
    "PeriodAdjustment",
    "adjust_period_for_universe",
]

# TASK-031: 자산 자유 추가 워크플로우 (도메인 서비스)
from app.domain.asset.registration import (  # noqa: E402
    AlreadyRegistered,
    BackfillEnqueuer,
    RegistrationRequest,
    RegistrationResult,
    TickerValidationFailed,
    TickerValidator,
    ValidationOutcome,
    register_asset,
)

__all__ += [
    "AlreadyRegistered",
    "BackfillEnqueuer",
    "RegistrationRequest",
    "RegistrationResult",
    "TickerValidationFailed",
    "TickerValidator",
    "ValidationOutcome",
    "register_asset",
]
