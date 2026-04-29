"""Asset Repository Protocol — 의존성 역전.

domain 이 인터페이스를 정의하고 data 레이어가 구현한다 (clean architecture).
TASK-031 의 비동기 백필이 이 Protocol 만 의존하도록 하여 ORM·DB 교체를 자유롭게 한다.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Protocol

from app.domain.asset.entity import Asset, Market


class AssetRepository(Protocol):
    """자산 마스터 카탈로그에 대한 도메인 Repository.

    구현체는 SQLAlchemy 기반 (`app.data.asset_repository.SqlAssetRepository`) 이지만
    domain/usecase 코드는 Protocol 만 import 한다.
    """

    def find_by_id(self, asset_id: int) -> Asset | None:
        """PK 단건 조회. 없으면 None."""
        ...

    def find_by_symbol_market(self, symbol: str, market: Market) -> Asset | None:
        """(symbol, market) UNIQUE 조회. 없으면 None."""
        ...

    def search(
        self,
        q: str | None = None,
        market: Market | None = None,
        asset_type: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Asset]:
        """카탈로그 검색.

        Args:
            q: symbol 또는 name 의 prefix (한글 이름 prefix 매칭 포함). None 이면 필터 미적용.
            market: 시장 필터. None 이면 전체.
            asset_type: 내부 분류 필터. None 이면 전체.
            limit/offset: 페이지네이션.

        Returns:
            active=True 자산 목록 (이름 정렬).
        """
        ...

    def list_active(self) -> list[Asset]:
        """active=True 인 모든 자산. 백필 스케줄러가 사용."""
        ...

    def upsert(self, asset: Asset) -> Asset:
        """자산 등록 또는 갱신. (symbol, market) UNIQUE 충돌 시 업데이트.

        TASK-031 의 사용자 자유 추가 워크플로우에서 사용. asset_id 는 DB 가 결정하므로
        신규 등록 시 asset.asset_id 값은 무시된다 (반환 객체에 실제 PK 가 채워짐).
        """
        ...

    def update_ingestion_state(
        self,
        asset_id: int,
        start_date: date | None,
        last_ingested_at: datetime | None,
    ) -> None:
        """백필 / 일일 ingestion 후 상태 갱신.

        None 인 인자는 갱신 스킵 (기존 값 유지).
        """
        ...
