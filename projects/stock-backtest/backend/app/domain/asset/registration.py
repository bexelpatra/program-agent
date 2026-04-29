"""자산 자유 추가 도메인 서비스.

architecture.md V3 § "자산 카탈로그 + 사용자 자유 추가" L528-538:
1. 즉시 검증 (3초 이내): yfinance/pykrx ticker 존재 + 최소 1년치 데이터
2. 검증 통과 시 카탈로그 등록 (active=true)
3. 비동기 백필 큐잉 (scheduler 위임)
4. 부분 백필 중 사용 가능

Reviewer N5: domain 은 data 어댑터를 의존성 주입으로 호출 (직접 import 금지).
TickerValidator / BackfillEnqueuer 는 Protocol — data / scheduler 어댑터가 구현한다.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.domain.asset.entity import Asset, AssetType, Market
from app.domain.asset.repository import AssetRepository


# --- 예외 (사용자 노출 가능 한국어 메시지) ----------------------------------

class TickerValidationFailed(Exception):
    """즉시 검증 실패. message 는 사용자 노출 가능 한국어."""


class AlreadyRegistered(Exception):
    """동일 (symbol, market) 이 이미 카탈로그에 active=true 로 있음."""


# --- 입력/출력 DTO ---------------------------------------------------------

@dataclass(frozen=True)
class RegistrationRequest:
    """사용자가 폼에서 입력한 신규 자산 등록 요청."""

    symbol: str
    market: Market
    asset_type: AssetType
    currency: str
    name: str
    meta: dict


@dataclass(frozen=True)
class ValidationOutcome:
    """TickerValidator 가 반환하는 즉시 검증 결과.

    Attributes:
        ticker: 정규화된 ticker (대문자/접미사 포함).
        exists: 시장 데이터 소스에 티커가 존재하는가.
        has_min_history: 최소 1년치 일봉이 있는가.
        earliest_date: 가용 데이터 가장 이른 일자 (없으면 None).
            domain 순수성을 위해 datetime.date 대신 object 로 받는다.
        note: 사용자에게 보여줄 한국어 안내 (선택).
    """

    ticker: str
    exists: bool
    has_min_history: bool
    earliest_date: object | None
    note: str | None


@dataclass(frozen=True)
class RegistrationResult:
    """register_asset 의 결과.

    Attributes:
        asset: DB 에 저장된 (PK 가 채워진) Asset.
        backfill_enqueued: 백필 큐잉 성공 여부. 실패해도 등록은 OK.
        note: 사용자에게 보여줄 한국어 안내 (선택).
    """

    asset: Asset
    backfill_enqueued: bool
    note: str | None


# --- 의존성 역전 Protocol --------------------------------------------------

class TickerValidator(Protocol):
    """data 어댑터 (YfinanceSource / PykrxSource) 가 구현.

    domain 은 인터페이스만 안다. 실제 yfinance/pykrx 호출은 어댑터 책임.
    """

    def validate_ticker(self, symbol: str) -> ValidationOutcome:
        """3초 이내에 검증 결과를 반환해야 한다 (블로킹 허용)."""
        ...


class BackfillEnqueuer(Protocol):
    """scheduler 가 구현. domain 은 큐잉 의도만 알고 비동기 실행 메커니즘은 모른다."""

    def enqueue(self, asset_id: int) -> None:
        """asset_id 를 백필 큐에 넣는다. 실패 시 예외 raise 가능."""
        ...


# --- 도메인 서비스 ---------------------------------------------------------

def register_asset(
    request: RegistrationRequest,
    repo: AssetRepository,
    validator: TickerValidator,
    enqueuer: BackfillEnqueuer,
) -> RegistrationResult:
    """자산 자유 추가 워크플로우.

    절차:
        1. 중복 체크 — 동일 (symbol, market) 이 active=true 로 이미 있으면 AlreadyRegistered.
        2. 즉시 검증 — validator.validate_ticker 호출. 실패 시 TickerValidationFailed.
        3. DB upsert — Asset 엔티티 생성 후 repo.upsert. PK 채워진 객체 반환.
        4. 백필 큐잉 — enqueuer.enqueue 호출. 실패 시 등록은 유지하고 note 로 안내.

    Args:
        request: 사용자 폼 입력.
        repo: AssetRepository 구현체 (data 레이어).
        validator: TickerValidator 구현체 (data 레이어).
        enqueuer: BackfillEnqueuer 구현체 (scheduler 레이어).

    Returns:
        RegistrationResult — 저장된 Asset, 큐잉 여부, 안내 note.

    Raises:
        AlreadyRegistered: 이미 active 로 등록된 경우.
        TickerValidationFailed: 시장 데이터 소스에서 티커 미발견 또는 검증 실패.
    """
    # 1) 중복 체크
    existing = repo.find_by_symbol_market(request.symbol, request.market)
    if existing is not None and existing.active:
        raise AlreadyRegistered(
            f"이미 등록된 자산입니다: {request.symbol} ({request.market})"
        )

    # 2) 즉시 검증 (3초 이내 — validator 내부 책임)
    outcome = validator.validate_ticker(request.symbol)
    if not outcome.exists:
        msg = outcome.note or (
            f"티커 '{request.symbol}' 를 찾을 수 없습니다. "
            "유효한 ticker 인지 확인하세요."
        )
        raise TickerValidationFailed(msg)

    # 3) DB upsert — 신규면 asset_id=0 (DB 가 부여), 기존 inactive 면 existing.asset_id 재사용
    asset = Asset(
        asset_id=existing.asset_id if existing is not None else 0,
        symbol=request.symbol,
        market=request.market,
        asset_type=request.asset_type,
        currency=request.currency,
        name=request.name,
        meta=request.meta,
        active=True,
        start_date=outcome.earliest_date,  # type: ignore[arg-type]
        last_ingested_at=None,
    )
    saved = repo.upsert(asset)

    # 4) 백필 큐잉 — 실패는 치명적이지 않음 (다음 cron 주기에 자동 수집)
    try:
        enqueuer.enqueue(saved.asset_id)
        enqueued = True
    except Exception:
        enqueued = False

    # 사용자 안내 note 결정 (우선순위: 검증 부족 > 큐잉 실패 > None)
    note: str | None = None
    if not outcome.has_min_history:
        note = (
            "최소 1년치 데이터 부족 — 백필 후 일부 백테스트 기간이 제한될 수 있습니다."
        )
    elif not enqueued:
        note = (
            "등록 완료. 백필 큐잉 실패로 데이터는 다음 cron 주기에 자동 수집됩니다."
        )

    return RegistrationResult(asset=saved, backfill_enqueued=enqueued, note=note)
