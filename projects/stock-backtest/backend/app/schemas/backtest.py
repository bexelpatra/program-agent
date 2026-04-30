"""백테스트 API Pydantic 스키마.

architecture.md V3 § "V2 API" L426-446 (비동기 job 모델) + § "결과 시각화" L703-708
+ Quant Lab CLAUDE.md L24 (지표 6종) 근거.

레이아웃:
- BacktestStatus / RebalanceSchedule: Literal 타입 (DB 의 String + 애플리케이션 검증).
- StrategyConfig: 사용자가 폼에서 입력하는 3요소 (allocator + filters + schedule).
- BacktestCreate: POST /api/backtests 요청 본문.
- BacktestRun: 단일 run 메타 (status/progress/error 포함).
- EquityPoint / TradeRecord / MetricsPayload: 결과 단위 schema.
- BacktestResult: GET /api/backtests/{run_id}/result 응답.

도메인 객체 (BacktestRunContext / BacktestRunResult / Strategy 등) 와 분리해 HTTP 경계
DTO 로 한정한다 (asset 패턴과 동일 — schemas/asset.py 가 도메인 Asset 과 분리되어 있음).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# DB BacktestRun.status 와 동기. ENUM 회피 + Pydantic Literal 로 호출 경계 검증.
BacktestStatus = Literal["pending", "running", "done", "failed", "cancelled"]

# domain.strategy.RebalanceSchedule 와 동일 값. HTTP 경계에서 동기.
RebalanceSchedule = Literal[
    "daily",
    "weekly",
    "monthly",
    "quarterly",
    "yearly",
    "signal_event",
]


class StrategyConfig(BaseModel):
    """사용자가 UI 폼에서 입력하는 3요소 조합 (allocator + filters AND + schedule).

    Quant Lab CLAUDE.md L10-15 + architecture.md V3 § "전략 인터페이스" L729 근거.

    allocator_params / filter_configs 는 dict[str, Any] 로 후행 검증을 위임 —
    실제 검증은 services/backtest_runner.build_strategy_from_config 에서 각 allocator/
    filter 의 Pydantic params_schema 가 수행 (전략별 schema 가 다양해서 여기서는 통일된
    bag of params 로 노출).
    """

    model_config = ConfigDict(frozen=True)

    allocator_name: str = Field(
        ...,
        examples=["fixed_weight", "all_weather", "equal_weight"],
        description="MVP 프리셋 3종 중 하나 (Quant Lab CLAUDE.md L26).",
    )
    allocator_params: dict[str, Any] = Field(
        ...,
        description="allocator 별 params (FixedWeightParams/AllWeatherParams/EqualWeightParams).",
    )
    filter_configs: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "[{name: 'moving_average', params: {window: 200}}, ...] — AND 결합. "
            "빈 리스트면 필터 없음."
        ),
    )
    rebalance_schedule: RebalanceSchedule = Field(
        "monthly",
        description="리밸런싱 주기 (monthly 가 백테스트 디폴트).",
    )


class BacktestCreate(BaseModel):
    """POST /api/backtests 요청 본문.

    initial_cash 는 통화별 초기 자본 dict (예: {"KRW": 10_000_000}). base_currency
    와 다른 통화도 허용 — 엔진이 base 환산해 equity 평가.
    """

    model_config = ConfigDict(frozen=True)

    name: str | None = Field(
        None,
        description="사용자 친화 이름 (선택, 이력 화면 노출용).",
    )
    strategy: StrategyConfig
    universe_asset_ids: list[int] = Field(
        ...,
        min_length=1,
        description="백테스트 universe 자산 ID 목록 (1개 이상).",
    )
    period_start: date
    period_end: date
    base_currency: str = Field(
        ...,
        min_length=2,
        max_length=8,
        description="기준 통화 (KRW/USD 등). 디폴트 강제 안 함 (architecture.md L568).",
    )
    initial_cash: dict[str, float] = Field(
        ...,
        description='통화별 초기 자본. 예: {"KRW": 10000000}.',
    )


class BacktestRun(BaseModel):
    """단일 run 메타 응답 (GET /api/backtests/{run_id} 및 list 항목).

    error 는 status='failed' 일 때만 채워짐 (V2 § 에러 응답 계약 — stage/type/message/
    request_ctx/trace_id).
    """

    model_config = ConfigDict(frozen=True)

    run_id: int
    run_hash: str
    status: BacktestStatus
    progress: float = Field(..., ge=0.0, le=1.0)
    name: str | None = None
    strategy_name: str
    period_start: date
    period_end: date
    base_currency: str
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: dict[str, Any] | None = None


class EquityPoint(BaseModel):
    """일별 equity 시계열 1점 (base_currency 기준)."""

    model_config = ConfigDict(frozen=True)

    time: date
    equity: float
    cash: float
    drawdown: float = Field(
        ...,
        description="누적 최대 낙폭 % (음수 또는 0).",
    )


class TradeRecord(BaseModel):
    """단일 매매 체결 한 건. native currency 기준."""

    model_config = ConfigDict(frozen=True)

    time: datetime
    asset_id: int
    side: Literal["BUY", "SELL"]
    qty: float  # CRYPTO 는 fractional (소수점 8자리), 그 외는 정수. JSON 직렬화는 float.
    price: float
    commission: float
    currency: str


class MetricsPayload(BaseModel):
    """Quant Lab CLAUDE.md L24 결과 지표 6종 + 연/월 수익률 테이블."""

    model_config = ConfigDict(frozen=True)

    cagr: float
    mdd: float
    sharpe: float
    sortino: float
    calmar: float
    win_rate: float
    annual_returns: dict[int, float] = Field(default_factory=dict)
    monthly_returns: dict[str, float] = Field(default_factory=dict)


class BacktestResult(BaseModel):
    """GET /api/backtests/{run_id}/result 응답. status='done' 일 때만 호출 가능."""

    model_config = ConfigDict(frozen=True)

    run: BacktestRun
    equity_curve: list[EquityPoint]
    trades: list[TradeRecord]
    metrics: MetricsPayload | None = None
