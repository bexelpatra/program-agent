"""
백테스팅 엔진.
전략의 generate_signals() 결과를 받아 과거 데이터에서 매매를 시뮬레이션하고
성과 지표를 계산한다.
"""

import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from src.analyzer.base import Signal, SignalType
from src.config import setup_logger

logger = setup_logger("backtester", "backtester.log")


@dataclass
class Trade:
    """개별 거래 기록."""

    date: str
    action: str  # "BUY" or "SELL"
    price: float
    shares: float
    cost: float  # 수수료 + 슬리피지 포함 총 비용/수입
    commission: float
    slippage_cost: float


class Backtester:
    """
    백테스팅 엔진.

    전략이 생성한 시그널 리스트와 가격 DataFrame을 받아
    매매 시뮬레이션을 수행하고 성과 지표를 산출한다.
    """

    def __init__(
        self,
        initial_capital: float = 10000.0,
        commission_rate: float = 0.001,
        slippage: float = 0.0005,
        risk_free_rate: float = 0.02,
    ):
        """
        Args:
            initial_capital: 초기 자본금
            commission_rate: 거래 수수료율 (0.001 = 0.1%)
            slippage: 슬리피지 비율 (0.0005 = 0.05%)
            risk_free_rate: 무위험 수익률 (연율, 샤프 비율 계산용)
        """
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage
        self.risk_free_rate = risk_free_rate

    def run(
        self,
        signals: list[Signal],
        price_df: pd.DataFrame,
    ) -> dict:
        """
        백테스팅 실행.

        Args:
            signals: 전략이 생성한 시그널 리스트
            price_df: 가격 DataFrame (date, close 컬럼 필수)

        Returns:
            {
                "metrics": {성과 지표},
                "benchmark": {Buy & Hold 벤치마크 지표},
                "portfolio": DataFrame (일별 포트폴리오 가치),
                "trades": list[Trade] (거래 내역),
            }
        """
        df = self._prepare_price_df(price_df)
        if df.empty:
            logger.warning("가격 데이터가 비어있습니다.")
            return self._empty_result()

        # 시그널을 날짜별 dict로 변환
        signal_map = self._build_signal_map(signals)

        # 전략 시뮬레이션
        portfolio_df, trades = self._simulate(df, signal_map)

        # 성과 지표 계산
        metrics = self._calculate_metrics(portfolio_df, trades)

        # 벤치마크 (Buy & Hold) 시뮬레이션
        benchmark_df, benchmark_trades = self._simulate_buy_and_hold(df)
        benchmark_metrics = self._calculate_metrics(benchmark_df, benchmark_trades)

        # 알파 계산
        metrics["alpha"] = metrics["total_return"] - benchmark_metrics["total_return"]

        return {
            "metrics": metrics,
            "benchmark": benchmark_metrics,
            "portfolio": portfolio_df,
            "trades": trades,
        }

    def summary(
        self,
        signals: list[Signal],
        price_df: pd.DataFrame,
    ) -> str:
        """
        백테스팅 결과를 텍스트 리포트로 반환한다.

        Args:
            signals: 전략이 생성한 시그널 리스트
            price_df: 가격 DataFrame

        Returns:
            터미널 출력용 텍스트 리포트
        """
        result = self.run(signals, price_df)
        m = result["metrics"]
        b = result["benchmark"]

        lines = [
            "=" * 60,
            "  BACKTEST REPORT",
            "=" * 60,
            "",
            f"  Initial Capital:      ${self.initial_capital:>14,.2f}",
            f"  Final Value:          ${m.get('final_value', 0):>14,.2f}",
            f"  Commission Rate:      {self.commission_rate * 100:.2f}%",
            f"  Slippage:             {self.slippage * 100:.2f}%",
            "",
            "-" * 60,
            "  PERFORMANCE METRICS",
            "-" * 60,
            f"  Total Return:         {m['total_return'] * 100:>10.2f}%",
            f"  CAGR:                 {m['cagr'] * 100:>10.2f}%",
            f"  Max Drawdown (MDD):   {m['mdd'] * 100:>10.2f}%",
            f"  Sharpe Ratio:         {m['sharpe_ratio']:>10.4f}",
            f"  Win Rate:             {m['win_rate'] * 100:>10.2f}%",
            f"  Profit/Loss Ratio:    {m['profit_loss_ratio']:>10.4f}",
            f"  Total Trades:         {m['total_trades']:>10d}",
            "",
            "-" * 60,
            "  BENCHMARK (Buy & Hold)",
            "-" * 60,
            f"  Total Return:         {b['total_return'] * 100:>10.2f}%",
            f"  CAGR:                 {b['cagr'] * 100:>10.2f}%",
            f"  Max Drawdown (MDD):   {b['mdd'] * 100:>10.2f}%",
            f"  Sharpe Ratio:         {b['sharpe_ratio']:>10.4f}",
            "",
            "-" * 60,
            f"  Alpha (vs Benchmark): {m['alpha'] * 100:>10.2f}%",
            "=" * 60,
        ]
        return "\n".join(lines)

    # =========================================================================
    # Internal methods
    # =========================================================================

    def _prepare_price_df(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """가격 DataFrame을 정리하여 date 기준 정렬된 복사본을 반환한다."""
        df = price_df.copy()

        if "date" not in df.columns:
            logger.error("가격 DataFrame에 'date' 컬럼이 없습니다.")
            return pd.DataFrame()

        if "close" not in df.columns:
            logger.error("가격 DataFrame에 'close' 컬럼이 없습니다.")
            return pd.DataFrame()

        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df = df.sort_values("date").reset_index(drop=True)
        return df

    def _build_signal_map(self, signals: list[Signal]) -> dict[str, Signal]:
        """시그널 리스트를 날짜별 dict로 변환한다. 같은 날짜에 여러 시그널이면 마지막 것을 사용."""
        signal_map: dict[str, Signal] = {}
        for sig in signals:
            signal_map[sig.date] = sig
        return signal_map

    def _simulate(
        self,
        df: pd.DataFrame,
        signal_map: dict[str, Signal],
    ) -> tuple[pd.DataFrame, list[Trade]]:
        """
        일별 시뮬레이션을 수행한다.

        Returns:
            (portfolio_df, trades)
        """
        cash = self.initial_capital
        shares = 0.0
        trades: list[Trade] = []

        dates = []
        portfolio_values = []
        cash_values = []
        shares_values = []

        for _, row in df.iterrows():
            date_str = row["date"]
            close_price = row["close"]

            # 시그널이 있으면 매매 실행
            if date_str in signal_map:
                signal = signal_map[date_str]

                if signal.signal_type == SignalType.BUY and cash > 0:
                    cash, shares, trade = self._execute_buy(
                        date_str, close_price, cash, shares, signal.weight
                    )
                    if trade:
                        trades.append(trade)

                elif signal.signal_type == SignalType.SELL and shares > 0:
                    cash, shares, trade = self._execute_sell(
                        date_str, close_price, cash, shares, signal.weight
                    )
                    if trade:
                        trades.append(trade)

                # HOLD: 아무 것도 하지 않음

            # 일별 포트폴리오 가치 기록
            portfolio_value = cash + shares * close_price
            dates.append(date_str)
            portfolio_values.append(portfolio_value)
            cash_values.append(cash)
            shares_values.append(shares)

        portfolio_df = pd.DataFrame(
            {
                "date": dates,
                "portfolio_value": portfolio_values,
                "cash": cash_values,
                "shares": shares_values,
            }
        )

        return portfolio_df, trades

    def _execute_buy(
        self,
        date: str,
        price: float,
        cash: float,
        shares: float,
        weight: float,
    ) -> tuple[float, float, Trade | None]:
        """
        매수 실행. 현금의 (weight * 100)%를 사용하여 매수.

        Returns:
            (남은 현금, 보유 주식수, Trade 기록)
        """
        # 슬리피지 적용 (매수 시 가격 상승)
        exec_price = price * (1 + self.slippage)

        # 투자 금액 계산
        invest_amount = cash * weight

        # 수수료 계산
        commission = invest_amount * self.commission_rate

        # 실제 매수 가능 금액 (수수료 차감)
        net_amount = invest_amount - commission
        if net_amount <= 0:
            return cash, shares, None

        # 매수 주식 수
        buy_shares = net_amount / exec_price
        slippage_cost = buy_shares * price * self.slippage

        trade = Trade(
            date=date,
            action="BUY",
            price=exec_price,
            shares=buy_shares,
            cost=invest_amount,
            commission=commission,
            slippage_cost=slippage_cost,
        )

        cash -= invest_amount
        shares += buy_shares

        logger.debug(
            f"BUY  {date}: {buy_shares:.4f} shares @ ${exec_price:.2f} "
            f"(commission: ${commission:.2f})"
        )

        return cash, shares, trade

    def _execute_sell(
        self,
        date: str,
        price: float,
        cash: float,
        shares: float,
        weight: float,
    ) -> tuple[float, float, Trade | None]:
        """
        매도 실행. 보유 주식의 (weight * 100)%를 매도.

        Returns:
            (남은 현금, 보유 주식수, Trade 기록)
        """
        # 슬리피지 적용 (매도 시 가격 하락)
        exec_price = price * (1 - self.slippage)

        # 매도 주식 수
        sell_shares = shares * weight
        if sell_shares <= 0:
            return cash, shares, None

        # 매도 대금
        gross_amount = sell_shares * exec_price

        # 수수료 계산
        commission = gross_amount * self.commission_rate
        net_amount = gross_amount - commission
        slippage_cost = sell_shares * price * self.slippage

        trade = Trade(
            date=date,
            action="SELL",
            price=exec_price,
            shares=sell_shares,
            cost=net_amount,
            commission=commission,
            slippage_cost=slippage_cost,
        )

        cash += net_amount
        shares -= sell_shares

        logger.debug(
            f"SELL {date}: {sell_shares:.4f} shares @ ${exec_price:.2f} "
            f"(commission: ${commission:.2f})"
        )

        return cash, shares, trade

    def _simulate_buy_and_hold(
        self, df: pd.DataFrame
    ) -> tuple[pd.DataFrame, list[Trade]]:
        """Buy & Hold 벤치마크 시뮬레이션. 첫 날 전액 매수, 마지막 날까지 보유."""
        first_date = df.iloc[0]["date"]
        signal_map = {
            first_date: Signal(date=first_date, signal_type=SignalType.BUY, weight=1.0)
        }
        return self._simulate(df, signal_map)

    def _calculate_metrics(
        self, portfolio_df: pd.DataFrame, trades: list[Trade]
    ) -> dict:
        """
        성과 지표를 계산한다.

        Returns:
            {
                "total_return", "cagr", "mdd", "sharpe_ratio",
                "win_rate", "profit_loss_ratio", "total_trades",
                "final_value"
            }
        """
        if portfolio_df.empty:
            return self._empty_metrics()

        values = portfolio_df["portfolio_value"].values
        final_value = values[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital

        # 거래 일수로 연수 계산 (영업일 기준 약 252일)
        n_days = len(values)
        n_years = n_days / 252.0

        # CAGR
        if n_years > 0 and final_value > 0:
            cagr = (final_value / self.initial_capital) ** (1 / n_years) - 1
        else:
            cagr = 0.0

        # MDD (Maximum Drawdown)
        mdd = self._calculate_mdd(values)

        # 일별 수익률 (Sharpe 계산용)
        daily_returns = (
            np.diff(values) / values[:-1] if len(values) > 1 else np.array([0.0])
        )

        # Sharpe Ratio (연환산)
        sharpe_ratio = self._calculate_sharpe(daily_returns)

        # 거래 기반 지표
        win_rate, profit_loss_ratio = self._calculate_trade_metrics(trades)
        total_trades = len(trades)

        return {
            "total_return": total_return,
            "cagr": cagr,
            "mdd": mdd,
            "sharpe_ratio": sharpe_ratio,
            "win_rate": win_rate,
            "profit_loss_ratio": profit_loss_ratio,
            "total_trades": total_trades,
            "final_value": final_value,
        }

    def _calculate_mdd(self, values: np.ndarray) -> float:
        """최대 낙폭(MDD)을 계산한다. 음수 값으로 반환."""
        if len(values) < 2:
            return 0.0

        peak = values[0]
        max_drawdown = 0.0

        for val in values:
            if val > peak:
                peak = val
            drawdown = (val - peak) / peak
            if drawdown < max_drawdown:
                max_drawdown = drawdown

        return max_drawdown

    def _calculate_sharpe(self, daily_returns: np.ndarray) -> float:
        """
        샤프 비율을 계산한다 (연환산).
        Sharpe = (mean_return - risk_free_daily) / std_return * sqrt(252)
        """
        if len(daily_returns) < 2:
            return 0.0

        std = np.std(daily_returns, ddof=1)
        if std == 0:
            return 0.0

        daily_rf = self.risk_free_rate / 252.0
        excess_return = np.mean(daily_returns) - daily_rf
        sharpe = (excess_return / std) * math.sqrt(252)

        return sharpe

    def _calculate_trade_metrics(self, trades: list[Trade]) -> tuple[float, float]:
        """
        거래 기반 승률과 수익/손실 비율을 계산한다.
        매수-매도 쌍을 기준으로 수익/손실을 판단한다.

        Returns:
            (win_rate, profit_loss_ratio)
        """
        if not trades:
            return 0.0, 0.0

        # 매수-매도 쌍으로 수익 계산
        buy_queue: list[tuple[float, float]] = []  # (exec_price, shares)
        profits: list[float] = []

        for trade in trades:
            if trade.action == "BUY":
                buy_queue.append((trade.price, trade.shares))
            elif trade.action == "SELL":
                sell_price = trade.price
                sell_shares_remaining = trade.shares

                while sell_shares_remaining > 0 and buy_queue:
                    buy_price, buy_shares = buy_queue[0]
                    matched = min(sell_shares_remaining, buy_shares)
                    pnl = (sell_price - buy_price) * matched
                    profits.append(pnl)

                    sell_shares_remaining -= matched
                    remaining_buy = buy_shares - matched
                    if remaining_buy > 0:
                        buy_queue[0] = (buy_price, remaining_buy)
                    else:
                        buy_queue.pop(0)

        if not profits:
            return 0.0, 0.0

        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p < 0]

        win_rate = len(wins) / len(profits) if profits else 0.0

        avg_win = np.mean(wins) if wins else 0.0
        avg_loss = abs(np.mean(losses)) if losses else 0.0
        profit_loss_ratio = (
            avg_win / avg_loss if avg_loss > 0 else float("inf") if avg_win > 0 else 0.0
        )

        return win_rate, profit_loss_ratio

    def _empty_result(self) -> dict:
        """빈 결과를 반환한다."""
        return {
            "metrics": self._empty_metrics(),
            "benchmark": self._empty_metrics(),
            "portfolio": pd.DataFrame(
                columns=["date", "portfolio_value", "cash", "shares"]
            ),
            "trades": [],
        }

    def _empty_metrics(self) -> dict:
        """빈 성과 지표를 반환한다."""
        return {
            "total_return": 0.0,
            "cagr": 0.0,
            "mdd": 0.0,
            "sharpe_ratio": 0.0,
            "win_rate": 0.0,
            "profit_loss_ratio": 0.0,
            "total_trades": 0,
            "final_value": self.initial_capital,
        }
