"""SqlAssetRepository — AssetRepository Protocol 의 SQLAlchemy 구현.

domain 의 Asset 엔티티 (frozen dataclass) 와 ORM 의 Asset 모델 사이를 매핑한다.
ORM 객체는 본 모듈을 벗어나지 않게 하여 domain/usecase 가 SQLAlchemy 에 결합되지 않도록 한다.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import cast

from sqlalchemy import func, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.domain.asset.entity import Asset as AssetEntity
from app.domain.asset.entity import AssetType, Market
from app.models.asset import Asset as AssetModel


def _to_entity(model: AssetModel) -> AssetEntity:
    """ORM 모델 → 도메인 엔티티 변환 일원화."""
    return AssetEntity(
        asset_id=model.asset_id,
        symbol=model.symbol,
        market=cast(Market, model.market),
        asset_type=cast(AssetType, model.asset_type),
        currency=model.currency,
        name=model.name,
        meta=model.meta or {},
        active=model.active,
        start_date=model.start_date,
        last_ingested_at=model.last_ingested_at,
    )


class SqlAssetRepository:
    """`AssetRepository` Protocol 의 SQLAlchemy 구현.

    Protocol 을 명시적으로 상속하지 않는 이유: 덕 타이핑(structural typing) 으로 충분하며
    Protocol 상속은 런타임 isinstance 체크가 필요한 경우에만 가치가 있다.
    """

    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, asset_id: int) -> AssetEntity | None:
        model = self._session.get(AssetModel, asset_id)
        return _to_entity(model) if model else None

    def find_by_symbol_market(self, symbol: str, market: Market) -> AssetEntity | None:
        stmt = select(AssetModel).where(
            AssetModel.symbol == symbol,
            AssetModel.market == market,
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return _to_entity(model) if model else None

    def search(
        self,
        q: str | None = None,
        market: Market | None = None,
        asset_type: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[AssetEntity]:
        stmt = select(AssetModel).where(AssetModel.active.is_(True))
        if q:
            # 한글명 prefix + symbol prefix 동시 매칭. ilike 로 대소문자 무시.
            pattern = f"{q}%"
            stmt = stmt.where(
                or_(AssetModel.symbol.ilike(pattern), AssetModel.name.ilike(pattern))
            )
        if market:
            stmt = stmt.where(AssetModel.market == market)
        if asset_type:
            stmt = stmt.where(AssetModel.asset_type == asset_type)
        stmt = stmt.order_by(AssetModel.name).limit(limit).offset(offset)
        return [_to_entity(m) for m in self._session.execute(stmt).scalars().all()]

    def count(
        self,
        q: str | None = None,
        market: Market | None = None,
        asset_type: str | None = None,
    ) -> int:
        """`search(...)` 와 동일 필터를 적용한 row 수.

        TASK-234: PaginatedResponse.total 정확화 — limit/offset 를 적용하지 않고
        조건에 맞는 전체 row 수를 반환한다 (페이지 수 산정 용도).
        search 와 필터 조건 동치성을 유지하기 위해 동일 분기를 그대로 복제했다.
        """
        stmt = (
            select(func.count())
            .select_from(AssetModel)
            .where(AssetModel.active.is_(True))
        )
        if q:
            pattern = f"{q}%"
            stmt = stmt.where(
                or_(AssetModel.symbol.ilike(pattern), AssetModel.name.ilike(pattern))
            )
        if market:
            stmt = stmt.where(AssetModel.market == market)
        if asset_type:
            stmt = stmt.where(AssetModel.asset_type == asset_type)
        return int(self._session.execute(stmt).scalar_one())

    def list_active(self) -> list[AssetEntity]:
        stmt = select(AssetModel).where(AssetModel.active.is_(True))
        return [_to_entity(m) for m in self._session.execute(stmt).scalars().all()]

    def upsert(self, asset: AssetEntity) -> AssetEntity:
        """ON CONFLICT (symbol, market) DO UPDATE.

        TASK-031 의 사용자 자유 추가 워크플로우에서 사용. asset_id 는 DB 가 결정.
        meta 는 NULL 허용 컬럼이지만 도메인은 dict 로 정규화하므로 빈 dict 도 그대로 저장.
        """
        stmt = (
            insert(AssetModel)
            .values(
                symbol=asset.symbol,
                market=asset.market,
                asset_type=asset.asset_type,
                currency=asset.currency,
                name=asset.name,
                meta=asset.meta,
                active=asset.active,
                start_date=asset.start_date,
                last_ingested_at=asset.last_ingested_at,
            )
            .on_conflict_do_update(
                index_elements=["symbol", "market"],
                set_={
                    "asset_type": asset.asset_type,
                    "currency": asset.currency,
                    "name": asset.name,
                    "meta": asset.meta,
                    "active": asset.active,
                    "start_date": asset.start_date,
                    "last_ingested_at": asset.last_ingested_at,
                },
            )
            .returning(AssetModel)
        )
        model = self._session.execute(stmt).scalar_one()
        self._session.flush()
        return _to_entity(model)

    def update_ingestion_state(
        self,
        asset_id: int,
        start_date: date | None,
        last_ingested_at: datetime | None,
    ) -> None:
        """None 인자는 기존 값 유지 (선택적 갱신)."""
        model = self._session.get(AssetModel, asset_id)
        if model is None:
            return
        if start_date is not None:
            model.start_date = start_date
        if last_ingested_at is not None:
            model.last_ingested_at = last_ingested_at
        self._session.flush()
