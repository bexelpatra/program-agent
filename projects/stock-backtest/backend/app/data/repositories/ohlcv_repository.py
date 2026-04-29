"""OhlcvRepository — ohlcv 테이블 SQLAlchemy 접근.

증분 파이프라인 (TASK-022) 에서 사용:
- latest_time: 자산별 MAX(time) 조회 → 백필 시작점 결정
- existing_dates: 기간 내 적재된 날짜 집합 → 갭 감지
- upsert_bars: ON CONFLICT (asset_id, time) DO UPDATE 로 멱등 적재

ORM 객체는 본 모듈을 벗어나지 않게 하여 도메인이 SQLAlchemy 에 결합되지 않도록 한다
(asset_repository.py 와 같은 정책).
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.data.sources.base import OhlcvBar
from app.models.ohlcv import Ohlcv


class OhlcvRepository:
    """ohlcv 테이블에 대한 데이터 접근.

    어댑터(sources/) 가 OhlcvBar 로 표현한 row 를 받아 ORM 으로 적재한다.
    """

    def __init__(self, session: Session):
        self._session = session

    def latest_time(self, asset_id: int) -> datetime | None:
        """asset 별 ohlcv 최신 time. 백필 시작점 결정에 사용.

        해당 자산에 적재된 row 가 없으면 None.
        """
        return self._session.execute(
            select(func.max(Ohlcv.time)).where(Ohlcv.asset_id == asset_id)
        ).scalar_one_or_none()

    def existing_dates(self, asset_id: int, start: date, end: date) -> set[date]:
        """[start, end] 구간 내 이미 적재된 날짜 집합.

        파이프라인의 갭 감지에서 expected_days(거래일 캘린더) 와 차집합 비교에 쓴다.
        time 컬럼은 timezone-aware datetime 이므로 .date() 로 일자 환산.
        """
        rows = self._session.execute(
            select(Ohlcv.time).where(
                Ohlcv.asset_id == asset_id,
                Ohlcv.time >= datetime.combine(start, datetime.min.time()),
                Ohlcv.time <= datetime.combine(end, datetime.max.time()),
            )
        ).scalars().all()
        return {ts.date() for ts in rows}

    def upsert_bars(self, asset_id: int, bars: Iterable[OhlcvBar]) -> int:
        """ON CONFLICT (asset_id, time) DO UPDATE 멱등 적재.

        Args:
            asset_id: 대상 자산 PK.
            bars: 어댑터가 반환한 OhlcvBar 시퀀스. close=0/null/NaN 는 어댑터가 이미 거른 상태.

        Returns:
            UPSERT 시도 row 수 (PG 의 실제 INSERT/UPDATE 분포는 별도). bars 가 비면 0.
        """
        rows: list[dict] = []
        for bar in bars:
            rows.append(
                {
                    "asset_id": asset_id,
                    "time": bar.time,
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "adj_close": bar.adj_close,
                    "volume": bar.volume,
                }
            )
        if not rows:
            return 0
        stmt = insert(Ohlcv).values(rows)
        # excluded.* 는 conflict 발생한 신규 row 의 값. 동일 (asset_id, time) 에 대해
        # 가격/거래량을 새 값으로 덮어써 idempotent 재수집을 보장.
        stmt = stmt.on_conflict_do_update(
            index_elements=["asset_id", "time"],
            set_={
                "open": stmt.excluded.open,
                "high": stmt.excluded.high,
                "low": stmt.excluded.low,
                "close": stmt.excluded.close,
                "adj_close": stmt.excluded.adj_close,
                "volume": stmt.excluded.volume,
            },
        )
        self._session.execute(stmt)
        self._session.flush()
        return len(rows)
