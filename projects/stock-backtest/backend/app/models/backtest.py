"""백테스트 결과 도메인 ORM 모델 (4개 한 파일 묶음).

architecture.md V3 § "DB 스키마" L242-251 (V1 살림) + § "비동기 job 모델" L437-446
+ § "에러 응답 계약" L450 (V2 살림 - error_json) 근거.

4개 모델(BacktestRun, BacktestEquity, BacktestTrade, BacktestMetric)을 한 파일에
묶는 이유:
  - 모두 backtest_runs.run_id 기반 관계로 응집도 ↑
  - 분리하면 Trade/Equity/Metric 가 Run 을 import 하면서 순환 import 위험
  - "백테스트 결과" 라는 단일 도메인 책임

가격/수량은 Numeric(20, 8) (가격) 또는 Numeric(20, 0) (정수 주) — ohlcv 와 일관.
모든 timestamp 는 timezone-aware (UTC 저장, 표시 계층에서 변환).
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BacktestRun(Base):
    """단일 백테스트 실행(job) 레코드.

    run_hash 는 (strategy_name, params, universe, period, base_currency) 직렬화 해시 —
    동일 입력 재실행 시 캐시 hit 판정 키 (중복 실행 방지). UNIQUE 제약으로 DB 가 강제.

    status 는 String + 애플리케이션 검증(Pydantic Literal) — pending/running/done/failed/cancelled.
    Postgres ENUM 마이그레이션 부담 회피 (assets.asset_type / ingestion_log.status 와 동일 패턴).

    progress 는 0.0~1.0 (리밸런싱 date 진행 기준). cancel_requested 는 엔진 루프가
    주기적으로 폴링하여 abort. error_json 은 V2 § "에러 응답 계약" 의
    {stage, type, message, request_ctx, trace_id} 형태로 적재.
    """

    __tablename__ = "backtest_runs"
    __table_args__ = (
        Index("ix_backtest_runs_status", "status"),
        Index("ix_backtest_runs_run_hash", "run_hash", unique=True),
        Index("ix_backtest_runs_created_at", "created_at"),
    )

    run_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # (strategy_name, params, universe, period, base_currency) 결정적 해시. 길이 64 는 sha256 hex.
    run_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    # 단일 사용자 모드 기본값 'local'. 추후 멀티유저 도입 시 FK 로 승격.
    user_id: Mapped[str] = mapped_column(String(64), nullable=False, server_default="local")
    strategy_name: Mapped[str] = mapped_column(String(64), nullable=False)
    # 전략 파라미터 (allocator/filters/rebalance) 직렬화. JSONB 로 부분 인덱싱 가능성 확보.
    params: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    # universe = [{"asset_id": int, ...}, ...] 형식. asset_id 는 별도 FK 미지정 (스냅샷성).
    universe: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    base_currency: Mapped[str] = mapped_column(String(8), nullable=False)
    # STOCK / CRYPTO / MIXED — V1 결정 5 (시장 모드 분리). UI/엔진 라우팅 키.
    market_mode: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="STOCK",
    )
    # pending / running / done / failed / cancelled — Pydantic Literal 로 호출 경계 검증.
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="pending",
    )
    # 0.0 ~ 1.0 — 리밸런싱 date 진행 기준 (V3 비동기 job 모델 L440).
    progress: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        server_default="0.0",
    )
    # API DELETE → 엔진 루프 폴링 → abort. 별도 cancelled_at 컬럼 없이 finished_at 으로 통합.
    cancel_requested: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )
    # 실패 시 {stage, type, message, request_ctx, trace_id} (V2 에러 응답 계약 L450).
    # Pydantic schema 는 TASK-062 에서 정의.
    error_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    # 재현성 추적용. 길이 64 는 git commit hash (40자) 와 향후 확장 여유.
    code_commit_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # universe ohlcv snapshot 해시 — 동일 코드 + 다른 데이터일 때 판별.
    data_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class BacktestEquity(Base):
    """run_id × time 의 포트폴리오 평가액 시계열 (TimescaleDB hypertable).

    equity = 모든 보유 자산 base_currency 평가액 + cash. cash 는 base_currency 잔고 합 분리 보관.
    drawdown 은 누적 MDD % (음수) — 매 시점 재계산 비용 회피용 미리 계산 적재.

    (run_id, time) 복합 PK — 동일 run 의 동일 시점 중복 차단.
    """

    __tablename__ = "backtest_equity"

    run_id: Mapped[int] = mapped_column(
        ForeignKey("backtest_runs.run_id", ondelete="CASCADE"),
        primary_key=True,
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )
    # base_currency 기준 총 평가액. Numeric(20, 8) — ohlcv 와 동일 정밀도.
    equity: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    # base_currency 기준 모든 통화 잔고 합 (FX 변환 후).
    cash: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    # 누적 최대 낙폭 % — 음수 또는 0. Numeric(10, 6) 으로 -99.999999% 까지 표현.
    drawdown: Mapped[Decimal] = mapped_column(
        Numeric(10, 6),
        nullable=False,
        server_default="0.0",
    )


class BacktestTrade(Base):
    """단일 매매 체결 한 건.

    qty 는 V3 Q8 재결정(2026-04-29) 으로 Numeric(20, 8) — 코인 한정 fractional.
    주식/ETF/지수/채권/원자재(KR/US) 는 정수 주 (Decimal(int) 형태로 저장),
    암호화폐(CRYPTO) 는 소수점 8자리 (BTC 1코인 = $50k 같은 고가 자산이 작은
    자본으로 매수 불가능해 모든 백테스트가 평탄선이 되는 사고 방지).
    price 는 native currency (자산의 currency) 가격 — Numeric(20, 8).
    commission 은 시장별 차등 (KR 0.015% / US 0.005% / Crypto 0.1%) — base_currency 가 아닌 native.

    side CHECK constraint 는 V3 § FX trade 미기록 정책 (architecture.md L389) 강제 —
    BUY/SELL 외 값 (예: FX_BUY, FX_SELL) 은 DB 레벨에서 거부.
    """

    __tablename__ = "backtest_trades"
    __table_args__ = (
        CheckConstraint(
            "side IN ('BUY', 'SELL')",
            name="ck_backtest_trades_side",
        ),
        Index("ix_backtest_trades_run_time", "run_id", "time"),
    )

    trade_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(
        ForeignKey("backtest_runs.run_id", ondelete="CASCADE"),
        nullable=False,
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.asset_id", ondelete="RESTRICT"),
        nullable=False,
    )
    # CHECK 제약으로 BUY/SELL 만 허용 (FX trade 미기록 정책).
    side: Mapped[str] = mapped_column(String(8), nullable=False)
    # V3 Q8 재결정(2026-04-29): 정수/소수 자산 통합 — Numeric(20, 8).
    # 알렘빅 0004_fractional_qty 마이그레이션으로 0001/0002/0003 baseline 에서 변환.
    qty: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    # 자산 native currency 가격 — base_currency 환산은 결과 표시 단계에서.
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    # 시장별 차등 수수료 (KR 0.015% / US 0.005% / Crypto 0.1%). native currency.
    commission: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        server_default="0",
    )
    # 자산의 native currency (assets.currency 와 동일하나 스냅샷성으로 별도 보관).
    currency: Mapped[str] = mapped_column(String(8), nullable=False)


class BacktestMetric(Base):
    """run 결과 메트릭 한 건 (cagr, mdd, sharpe, sortino, calmar, win_rate 등).

    (run_id, metric_name) UNIQUE — 동일 run 에 동일 메트릭 중복 적재 방지.
    metric_name 은 String + 애플리케이션 검증 — Postgres ENUM 회피 (assets.asset_type 패턴).
    annual_return_2024 같은 동적 메트릭명도 수용해야 하므로 ENUM 부적합.
    """

    __tablename__ = "backtest_metrics"
    __table_args__ = (
        UniqueConstraint("run_id", "metric_name", name="uq_backtest_metrics_run_name"),
    )

    metric_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(
        ForeignKey("backtest_runs.run_id", ondelete="CASCADE"),
        nullable=False,
    )
    # cagr / mdd / sharpe / sortino / calmar / win_rate / annual_return_YYYY / monthly_return_YYYYMM 등.
    metric_name: Mapped[str] = mapped_column(String(64), nullable=False)
    # 메트릭 값 (수익률은 비율, drawdown 은 음수 %, sharpe 등은 무차원). Numeric(20, 8) 통일.
    value: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
