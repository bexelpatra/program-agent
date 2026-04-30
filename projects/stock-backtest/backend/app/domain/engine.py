"""백테스트 메인 루프 (모델 A 강제).

architecture.md V3 § "거래 정책" 모델 A (L615-630):
- D 일 종가 → 시그널 판정
- D+1 일 시가 → 체결
- 구조적 차단: prices_until_d = prices_aligned.loc[:d] (D+1 절대 노출 X)

architecture.md V3 § "백엔드 모듈 분할" L654-666:
- engine.py 는 백테스트 메인 루프만. 도메인 모델 (Portfolio/Strategy/Trade/Calendar)
  전부 import 만, 자체 정의 금지.
- 시간 루프 + 시그널 호출 + 리밸런싱 호출 + equity 기록 + 진행률/취소.

루프 시퀀스 (모델 A):
1. trading_days_in_period(base, start, end) → 시간축 D_0, D_1, ..., D_N
2. 각 D_i 가 rebalance_schedule 에 해당하는 날인지 판정 (_is_rebalance_day)
3. 해당하면:
   a. prices_until_d = prices_aligned.loc[:d] (모델 A 차단 — 한 줄로 D+1 노출 0)
   b. apply_filters_and_allocator(strategy, universe, prices_until_d, signal_date=D_i)
   c. 체결일 = next_trading_day(base, D_i) = D_{i+1}
   d. 체결가 = D_{i+1} 종가 (yfinance 일봉 — 시가 미보유 시 종가 fallback)
   e. execute_rebalance(portfolio, target_weights, ..., settlement_d)
4. 매 D_i 종료 시 portfolio.equity_in_base 기록
5. progress_callback / cancel_check 가 비동기 job hook (TASK-062)

도메인 순수: SQLAlchemy/HTTP/외부 라이브러리 import 금지. pandas 는 시계열 본질 (허용).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable

import pandas as pd

from app.domain.calendar import next_trading_day, trading_days_in_period
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


def run_backtest(ctx: BacktestRunContext) -> BacktestRunResult:
    """백테스트 메인 루프 (모델 A).

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

    prev_d: date | None = None
    total = len(timeline)

    for i, d in enumerate(timeline):
        # 취소 체크 (TASK-062 비동기 hook).
        if ctx.cancel_check is not None and ctx.cancel_check():
            aborted = True
            break

        # 리밸런싱 일자 판정.
        if _is_rebalance_day(d, prev_d, ctx.strategy.rebalance_schedule):
            # 모델 A 구조적 차단: prices_until_d 는 d 까지만 (D+1 절대 노출 X).
            # 이 한 줄이 look-ahead bias 방어 핵심 — Allocator/Filter 가 prices.tail()
            # 이상으로 인덱싱해도 D+1 데이터에 도달 불가능.
            prices_until_d = ctx.prices_aligned.loc[:d]

            # 전략 적용 (필터 AND → allocator).
            # 빈 dict 도 정상 결과 — strategy.py L154 주석 "cash-only 로 해석".
            # 보유 포지션이 있으면 trade._classify_orders L191-198 가 전량 매도 sells
            # 에 추가 → 청산 동작 (TASK-211 회귀: 이전엔 if target_weights 분기로
            # execute_rebalance 호출 자체를 skip 했음 → filter fail 시 청산 누락 버그).
            target_weights = apply_filters_and_allocator(
                ctx.strategy,
                universe_asset_ids,
                prices_until_d,
                d,
            )

            # universe 부분집합 invariant (TASK-211): 보유 자산은 항상 universe 부분집합.
            # universe 가 백테스트 동안 고정 (universe_market_meta 불변), 매수는 universe
            # 자산만 가능 (apply_filters_and_allocator 가 universe_asset_ids 만 weight
            # 산출), 매도는 보유 자산만 → 보유 ⊆ universe 구조적 보장.
            # 빈 target_weights entry path 에서 settlement_prices/asset_meta 가 보유
            # 자산을 cover 하기 위한 전제 조건. 위반은 silent 0 가 아닌 명시적 에러로 catch.
            held_not_in_universe = [
                aid
                for aid in portfolio.positions.keys()
                if aid not in ctx.universe_market_meta
            ]
            if held_not_in_universe:
                # 정상 흐름에서는 발생 불가 — 발생하면 universe_market_meta 변조 등
                # 호출자 버그. silent 진행하지 않고 명시적 에러 (실거래 정합성 원칙).
                raise ValueError(
                    f"invariant violation at {d}: held assets not in universe: "
                    f"{held_not_in_universe}"
                )

            # 체결일 = D+1 (모델 A). D 가 마지막 거래일이거나 캘린더 미지원이면 스킵.
            settlement_d: date | None = None
            try:
                settlement_d = next_trading_day(ctx.base_currency, d)
            except Exception as e:
                _LOG.warning(
                    "next_trading_day failed at signal_date=%s: %s", d, e
                )

            if (
                settlement_d is not None
                and settlement_d in ctx.prices_aligned.index
            ):
                # D+1 종가 기반 체결 (yfinance 일봉만 보유 시 시가 fallback = 종가).
                # 빈 target_weights 인 경우에도 보유 청산을 위해 호출 — 단, 청산 시
                # 가격이 누락된 보유 자산은 trade._execute_sells L216-221 의
                # avg_price fallback 으로 처리 (sell-only 청산 시나리오 방어).
                settlement_prices = _eod_prices_dict(
                    ctx.prices_aligned, settlement_d, universe_asset_ids
                )
                fx_at_settlement = ctx.fx_rates_to_base.get(
                    settlement_d, ctx.fx_rates_to_base.get(d, {})
                )
                try:
                    rebalance_fills = execute_rebalance(
                        portfolio,
                        target_weights,
                        ctx.universe_market_meta,
                        settlement_prices,
                        fx_at_settlement,
                        settlement_d,
                    )
                    fills.extend(rebalance_fills)
                except Exception as e:
                    # 리밸런싱 실패 (NonTradingDayError / MissingPriceError /
                    # 잔고 부족 등) → 로그만, 루프 계속 (1회 누락이 전체 백테스트
                    # 중단 사유는 아님 — TASK-080 골든 테스트에서 정책 검증).
                    _LOG.warning(
                        "rebalance failed at settlement_date=%s: %s",
                        settlement_d,
                        e,
                    )

        # equity 기록 (D 일 종가 기준).
        eod_prices = _eod_prices_dict(ctx.prices_aligned, d, universe_asset_ids)
        fx_at_d = ctx.fx_rates_to_base.get(d, {})
        try:
            # 보유 포지션의 가격이 누락된 경우 equity_in_base 가 ValueError → 스킵.
            held_asset_ids = list(portfolio.positions.keys())
            missing_held = [
                aid for aid in held_asset_ids if aid not in eod_prices
            ]
            if missing_held:
                _LOG.debug(
                    "skip equity at %s: missing prices for held %s",
                    d,
                    missing_held[:3],
                )
            else:
                equity = portfolio.equity_in_base(eod_prices, fx_at_d)
                cash_total = portfolio.total_cash_in_base(fx_at_d)
                equity_curve.append(
                    BacktestEquityPoint(
                        time=d, equity=equity, cash_total_in_base=cash_total
                    )
                )
        except ValueError as e:
            # FX rate 누락 등 — equity 기록 스킵.
            _LOG.debug("skip equity at %s: %s", d, e)

        # progress.
        if ctx.progress_callback is not None:
            ctx.progress_callback((i + 1) / total)

        prev_d = d

    return BacktestRunResult(
        equity_curve=equity_curve,
        fills=fills,
        final_portfolio=portfolio,
        aborted=aborted,
    )
