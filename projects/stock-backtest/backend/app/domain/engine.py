"""백테스트 메인 루프 (모델 A 강제 — D 시그널 → D+1 settlement 큐잉).

architecture.md V3 § "거래 정책" 모델 A (L615-630) + § "EOD equity 기록 시점" (L635-648):
- D 일 종가 → 시그널 판정
- D+1 일 시가 → 체결 (실제로는 다음 iteration 의 d 가 D+1)
- 구조적 차단: prices_until_d = prices_aligned.loc[:d] (D+1 절대 노출 X)
- D EOD equity = D 시그널 이전 (= 어제 시그널 D-1 이 오늘 D 에 settlement 된 직후)
  → 사용자 멘탈 모델 / 실거래 정합 (매도 시그널 D EOD = 아직 보유, 매수 시그널 D EOD = 아직 cash).

architecture.md V3 § "백엔드 모듈 분할" L654-666:
- engine.py 는 백테스트 메인 루프만. 도메인 모델 (Portfolio/Strategy/Trade/Calendar)
  전부 import 만, 자체 정의 금지.
- 시간 루프 + 시그널 호출 + 리밸런싱 호출 + equity 기록 + 진행률/취소.

루프 시퀀스 (큐잉 패턴, TASK-244 fix 후):
1. trading_days_in_period(base, start, end) → 시간축 D_0, D_1, ..., D_N
2. 각 iteration d 시작 시:
   a. (settlement) 어제 큐잉된 pending_rebalance 가 있으면 오늘 d 가격으로 execute.
   b. (equity) d 가격 + post-settlement portfolio 로 EOD equity 기록.
      - Day 0 = pure cash (어제 큐잉 없음 → settlement skip → portfolio = initial_cash).
      - Day k≥1 = 어제 시그널이 오늘 settlement 된 직후 평가.
   c. (signal) d 가 rebalance_day 면 D 종가 기준 target_weights 산출 → pending 큐잉.
3. 마지막 iteration 의 큐잉은 다음 iteration 부재로 settlement 안 됨 (실거래 일관성:
   마지막 영업일 시그널은 다음 영업일 부재라 유효 X).
4. progress_callback / cancel_check 가 비동기 job hook (TASK-062).

도메인 순수: SQLAlchemy/HTTP/외부 라이브러리 import 금지. pandas 는 시계열 본질 (허용).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable

import pandas as pd

from app.domain.calendar import trading_days_in_period
from app.domain.portfolio import Portfolio
from app.domain.strategy import (
    RebalanceSchedule,
    Strategy,
    apply_filters_and_allocator,
)
from app.domain.trade import TradeFill, execute_rebalance

_LOG = logging.getLogger(__name__)


# ===== 입출력 컨텍스트 =====


@dataclass
class BacktestRunContext:
    """백테스트 1회 실행 컨텍스트. API 레이어 (TASK-062) 가 채워서 run_backtest 호출.

    prices_aligned 는 사전에 calendar.align_universe_prices 로 base 캘린더 정렬 완료
    상태여야 한다. engine 은 추가 정렬을 하지 않는다.
    """

    base_currency: str
    period_start: date
    period_end: date
    initial_cash: dict[str, Decimal]
    """초기 자본 (통화별 dict). 예: {"KRW": Decimal("10000000")}."""

    universe_market_meta: dict[int, tuple[str, str]]
    """asset_id → (market, currency). 예: {1: ("US", "USD"), 2: ("KR", "KRW")}."""

    prices_aligned: pd.DataFrame
    """index=date (base 거래일, 오름차순), columns=asset_id (int), values=close (float).
    base 캘린더 정렬 + forward-fill 완료 상태. NaN 은 자산별 결측 (기간 내 미상장 등).
    """

    fx_rates_to_base: dict[date, dict[str, Decimal]]
    """date → {ccy → base_per_ccy}. 예: base=KRW, 2024-01-02 → {"USD": 1300}."""

    strategy: Strategy
    progress_callback: Callable[[float], None] | None = None
    """진행률 hook (0.0 ~ 1.0). TASK-062 비동기 job 이 backtest_runs.progress 갱신에 사용."""

    cancel_check: Callable[[], bool] | None = None
    """True 면 즉시 abort. TASK-062 비동기 job 이 DB 플래그 폴링."""


@dataclass
class BacktestEquityPoint:
    """일별 equity 스냅샷 (D 일 종가 기준)."""

    time: date
    equity: Decimal
    cash_total_in_base: Decimal


@dataclass
class BacktestRunResult:
    """run_backtest 반환. TASK-062 가 DB 적재 (backtest_equity / backtest_trades)."""

    equity_curve: list[BacktestEquityPoint]
    fills: list[TradeFill]
    final_portfolio: Portfolio
    aborted: bool
    """cancel_check 가 True 였으면 True (부분 결과 반환)."""


# ===== 리밸런싱 일자 판정 =====


def _is_rebalance_day(
    d: date, prev_d: date | None, schedule: RebalanceSchedule
) -> bool:
    """rebalance_schedule 에 따라 d 가 리밸런싱 일자인지.

    첫날 (prev_d is None) 은 항상 True (초기 진입 매수).

    - daily: 매일
    - weekly: ISO 주차 변경 시
    - monthly: 월 변경 시 (예: 1/31 → 2/1 True)
    - quarterly: 분기 변경 시 ((month-1)//3 변경)
    - semi_annual: 반기 변경 시 ((month-1)//6 변경) — 1월·7월 첫 거래일 trigger.
      quarterly 와 의미론 일관 (TASK-220 사용자 결정 2026-04-30).
    - yearly: 연도 변경 시
    - signal_event: 매일 시그널 체크 (실제 변화 여부는 allocator/filter 결정)
    """
    if prev_d is None:
        return True
    if schedule == "daily":
        return True
    if schedule == "weekly":
        prev_year, prev_week, _ = prev_d.isocalendar()
        cur_year, cur_week, _ = d.isocalendar()
        return cur_week != prev_week or cur_year != prev_year
    if schedule == "monthly":
        return d.month != prev_d.month or d.year != prev_d.year
    if schedule == "quarterly":
        prev_q = (prev_d.month - 1) // 3
        cur_q = (d.month - 1) // 3
        return cur_q != prev_q or d.year != prev_d.year
    if schedule == "semi_annual":
        prev_h = (prev_d.month - 1) // 6
        cur_h = (d.month - 1) // 6
        return cur_h != prev_h or d.year != prev_d.year
    if schedule == "yearly":
        return d.year != prev_d.year
    if schedule == "signal_event":
        return True
    raise ValueError(f"unknown rebalance_schedule: {schedule}")


# ===== 메인 루프 =====


def _eod_prices_dict(
    prices_aligned: pd.DataFrame,
    d: date,
    universe_asset_ids: list[int],
) -> dict[int, Decimal]:
    """prices_aligned.loc[d] 행에서 universe 자산 가격 dict (NaN 제외)."""
    if d not in prices_aligned.index:
        return {}
    row = prices_aligned.loc[d]
    out: dict[int, Decimal] = {}
    for aid in universe_asset_ids:
        if aid not in row.index:
            continue
        v = row[aid]
        if pd.notna(v):
            out[aid] = Decimal(str(v))
    return out


@dataclass
class _PendingRebalance:
    """D 에서 산출된 시그널을 다음 iteration (D+1) settlement 까지 보관하는 큐잉 박스."""

    signal_date: date
    target_weights: dict[int, Decimal]


def _settle_pending_rebalance(
    pending: _PendingRebalance,
    portfolio: Portfolio,
    ctx: BacktestRunContext,
    settlement_d: date,
    universe_asset_ids: list[int],
    fills: list[TradeFill],
) -> None:
    """큐잉된 시그널을 settlement_d 가격으로 체결.

    실패 (NonTradingDayError / MissingPriceError / 잔고 부족 등) 는 로그만 — 1회 누락이
    전체 백테스트 중단 사유는 아님 (TASK-080 골든 테스트에서 정책 검증).
    """
    settlement_prices = _eod_prices_dict(
        ctx.prices_aligned, settlement_d, universe_asset_ids
    )
    fx_at_settlement = ctx.fx_rates_to_base.get(
        settlement_d, ctx.fx_rates_to_base.get(pending.signal_date, {})
    )
    try:
        rebalance_fills = execute_rebalance(
            portfolio,
            pending.target_weights,
            ctx.universe_market_meta,
            settlement_prices,
            fx_at_settlement,
            settlement_d,
        )
        fills.extend(rebalance_fills)
    except Exception as e:
        _LOG.warning(
            "rebalance failed at settlement_date=%s (signal=%s): %s",
            settlement_d,
            pending.signal_date,
            e,
        )


def _record_eod_equity(
    portfolio: Portfolio,
    ctx: BacktestRunContext,
    d: date,
    universe_asset_ids: list[int],
    equity_curve: list[BacktestEquityPoint],
) -> None:
    """D 가격 + 현 portfolio 로 EOD equity 1포인트 기록 (가격/FX 누락 시 skip)."""
    eod_prices = _eod_prices_dict(ctx.prices_aligned, d, universe_asset_ids)
    fx_at_d = ctx.fx_rates_to_base.get(d, {})
    held_asset_ids = list(portfolio.positions.keys())
    missing_held = [aid for aid in held_asset_ids if aid not in eod_prices]
    if missing_held:
        _LOG.debug("skip equity at %s: missing prices for held %s", d, missing_held[:3])
        return
    try:
        equity = portfolio.equity_in_base(eod_prices, fx_at_d)
        cash_total = portfolio.total_cash_in_base(fx_at_d)
    except ValueError as e:
        _LOG.debug("skip equity at %s: %s", d, e)
        return
    equity_curve.append(
        BacktestEquityPoint(time=d, equity=equity, cash_total_in_base=cash_total)
    )


def _generate_signal_for_day(
    ctx: BacktestRunContext,
    d: date,
    portfolio: Portfolio,
    universe_asset_ids: list[int],
) -> dict[int, Decimal]:
    """D 종가까지의 데이터로 target_weights 산출 (look-ahead 0).

    universe 부분집합 invariant 도 함께 검증 — 보유 자산이 universe 외부면 즉시 ValueError.
    """
    # 모델 A 구조적 차단: prices_until_d 는 d 까지만 (D+1 절대 노출 X).
    # 이 한 줄이 look-ahead bias 방어 핵심 — Allocator/Filter 가 prices.tail()
    # 이상으로 인덱싱해도 D+1 데이터에 도달 불가능.
    prices_until_d = ctx.prices_aligned.loc[:d]

    # universe 부분집합 invariant (TASK-211): 보유 자산은 항상 universe 부분집합.
    # 시그널 산출 전에 검사 — 위반은 silent 0 가 아닌 명시적 에러로 catch.
    held_not_in_universe = [
        aid
        for aid in portfolio.positions.keys()
        if aid not in ctx.universe_market_meta
    ]
    if held_not_in_universe:
        raise ValueError(
            f"invariant violation at {d}: held assets not in universe: "
            f"{held_not_in_universe}"
        )

    # 전략 적용 (필터 AND → allocator).
    # 빈 dict 도 정상 결과 — strategy.py L154 주석 "cash-only 로 해석".
    # 보유 포지션이 있으면 trade._classify_orders L191-198 가 전량 매도 sells
    # 에 추가 → 청산 동작 (TASK-211 회귀 가드).
    return apply_filters_and_allocator(
        ctx.strategy,
        universe_asset_ids,
        prices_until_d,
        d,
    )


def run_backtest(ctx: BacktestRunContext) -> BacktestRunResult:
    """백테스트 메인 루프 (모델 A — D 시그널 → D+1 settlement 큐잉 패턴).

    Returns:
        BacktestRunResult — equity_curve / fills / final_portfolio / aborted.

    Raises:
        ValueError: timeline 이 비어있으면 (period 내 거래일 0).
    """
    # 시간축 (base 캘린더 거래일).
    timeline = trading_days_in_period(
        ctx.base_currency, ctx.period_start, ctx.period_end
    )
    if not timeline:
        raise ValueError(
            f"no trading days in period {ctx.period_start} ~ {ctx.period_end} "
            f"for base_currency={ctx.base_currency}"
        )

    # 초기 portfolio.
    portfolio = Portfolio(base_currency=ctx.base_currency)
    for ccy, amount in ctx.initial_cash.items():
        portfolio.deposit(ccy, amount)

    universe_asset_ids = list(ctx.universe_market_meta.keys())
    equity_curve: list[BacktestEquityPoint] = []
    fills: list[TradeFill] = []
    aborted = False

    # D 시그널을 D+1 settlement 까지 보관하는 큐 (None = 큐잉 비어있음).
    # 큐잉 패턴 (TASK-244 fix) — D iteration 안에서 시그널/체결/equity 를 모두 처리하던
    # 기존 흐름이 D EOD 평가에 D+1 가격으로 산 새 포지션을 D 가격으로 평가하는 회계
    # 결함을 만들어, 큐잉으로 시그널과 체결을 한 iteration 분리.
    pending_rebalance: _PendingRebalance | None = None

    prev_d: date | None = None
    total = len(timeline)

    for i, d in enumerate(timeline):
        # 취소 체크 (TASK-062 비동기 hook).
        if ctx.cancel_check is not None and ctx.cancel_check():
            aborted = True
            break

        # ① settlement: 어제 큐잉된 시그널을 오늘 d 가격으로 체결.
        if pending_rebalance is not None:
            _settle_pending_rebalance(
                pending_rebalance, portfolio, ctx, d, universe_asset_ids, fills
            )
            pending_rebalance = None

        # ② equity 기록: post-settlement portfolio + d 가격.
        # Day 0 = pure cash (큐잉 없었음 → settlement skip → portfolio = initial_cash).
        # Day k≥1 = 어제 시그널이 오늘 settlement 된 직후 평가.
        _record_eod_equity(portfolio, ctx, d, universe_asset_ids, equity_curve)

        # ③ signal: d 가 rebalance day 면 target_weights 산출 후 큐잉
        # (다음 iteration 의 d 가 D+1 = settlement 일).
        if _is_rebalance_day(d, prev_d, ctx.strategy.rebalance_schedule):
            target_weights = _generate_signal_for_day(
                ctx, d, portfolio, universe_asset_ids
            )
            pending_rebalance = _PendingRebalance(
                signal_date=d, target_weights=target_weights
            )

        # progress.
        if ctx.progress_callback is not None:
            ctx.progress_callback((i + 1) / total)

        prev_d = d

    # 마지막 iteration 의 시그널은 다음 iteration 부재로 settlement 안 됨 — 실거래
    # 일관성 (마지막 영업일 시그널은 다음 영업일 부재라 유효 X). architecture.md L646.

    return BacktestRunResult(
        equity_curve=equity_curve,
        fills=fills,
        final_portfolio=portfolio,
        aborted=aborted,
    )
