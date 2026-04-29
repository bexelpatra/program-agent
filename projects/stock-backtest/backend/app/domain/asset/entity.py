"""Asset / Universe 도메인 엔티티.

POPO (frozen dataclass) — SQLAlchemy / FastAPI / 시장 데이터 어댑터 의존 금지.
data 레이어가 ORM 모델 ↔ 본 엔티티 변환을 책임진다.

architecture.md V3 § "자산 도메인 모델" L514-555 근거.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

# UI 노출 기준 시장 분류. (DB 컬럼 정의와 일치)
Market = Literal["KR", "US", "CRYPTO"]

# 내부 정밀 분류. Phase 2 에서 UI 세분화 시 활용.
AssetType = Literal["EQUITY_INDEX", "ETF", "BOND", "COMMODITY", "CRYPTO"]


@dataclass(frozen=True)
class Asset:
    """카탈로그에 등록된 단일 자산.

    Attributes:
        asset_id: DB PK.
        symbol: yfinance/pykrx ticker. (symbol, market) 조합이 UNIQUE.
        market: UI 노출 시장 분류.
        asset_type: 내부 정밀 분류.
        currency: native currency (ISO 4217). 환전·배당 계산 기준.
        name: 한글 표시명.
        meta: 미래 확장(kr_tax_class 등). 빈 dict 허용.
        active: 카탈로그 노출 여부.
        start_date: 보유한 가장 오래된 일봉 일자. 백필 전이면 None.
        last_ingested_at: 마지막 ingestion 시각. 백필 전이면 None.
    """

    asset_id: int
    symbol: str
    market: Market
    asset_type: AssetType
    currency: str
    name: str
    meta: dict
    active: bool
    start_date: date | None
    last_ingested_at: datetime | None


@dataclass(frozen=True)
class Universe:
    """백테스트 1회에 사용할 자산 묶음.

    백테스트 생성 폼에서 사용자가 자산 선택해 구성한다 (architecture.md V3 § "universe 정의").
    """

    assets: tuple[Asset, ...]

    def common_period(self) -> tuple[date, date] | None:
        """모든 자산의 가용 기간 교집합.

        - 빈 universe 또는 단 하나의 자산이라도 start_date 가 None 이면 None 반환
          (백필 진행 중·실패로 데이터 가용 기간 불확정).
        - 시작일은 universe 자산 중 가장 늦은 start_date (architecture.md V3 § "universe 시작일 불일치").
        - 종료일은 호출자가 last_ingested_at 등으로 결정. 본 메서드는 today 를 상한으로 반환.

        Returns:
            (start, end) 튜플 또는 None.
        """
        if not self.assets:
            return None
        starts = [a.start_date for a in self.assets if a.start_date is not None]
        if len(starts) != len(self.assets):
            # 일부 자산이 아직 백필 전 — 안전하게 None.
            return None
        return (max(starts), date.today())

    def assets_by_currency(self) -> dict[str, tuple[Asset, ...]]:
        """통화별 자산 그룹.

        환전 정책 (architecture.md V3 § "환전 정책 — native 우선") 에서
        같은 native currency 끼리는 환전 없이 잔고 직접 활용하기 위한 그룹핑.

        Returns:
            currency -> 해당 통화 자산 튜플.
        """
        groups: dict[str, list[Asset]] = {}
        for asset in self.assets:
            groups.setdefault(asset.currency, []).append(asset)
        return {ccy: tuple(items) for ccy, items in groups.items()}
