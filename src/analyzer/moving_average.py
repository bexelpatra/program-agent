"""
이동평균 크로스오버 전략.
단기(50일) / 장기(200일) SMA를 계산하고, 골든크로스/데드크로스를 탐지하여
BUY/SELL 시그널을 생성한다.
"""

import pandas as pd

from src.analyzer.base import BaseStrategy, Signal, SignalType


class MovingAverageStrategy(BaseStrategy):
    """이동평균 크로스오버 전략."""

    @property
    def name(self) -> str:
        return "moving_average"

    @property
    def description(self) -> str:
        return "단기/장기 SMA 크로스오버 기반 매매 시그널 생성"

    def analyze(self, df: pd.DataFrame, **params) -> dict:
        """
        이동평균 크로스오버를 분석한다.

        Args:
            df: OHLCV DataFrame (date, close 컬럼 필수)
            **params:
                short_window (int): 단기 SMA 기간. 기본 50.
                long_window (int): 장기 SMA 기간. 기본 200.

        Returns:
            {
                "summary": 분석 요약 텍스트,
                "metrics": {
                    "total_crossovers": 크로스오버 총 횟수,
                    "golden_crosses": 골든크로스 횟수,
                    "dead_crosses": 데드크로스 횟수,
                    "current_state": 현재 상태 ("bullish" / "bearish" / "unknown"),
                },
                "details": 크로스오버 이벤트 DataFrame,
            }
        """
        short_window = params.get("short_window", 50)
        long_window = params.get("long_window", 200)

        # 데이터 준비
        data = df[["date", "close"]].copy()
        data["date"] = pd.to_datetime(data["date"])
        data = data.sort_values("date").reset_index(drop=True)

        if len(data) < long_window:
            return {
                "summary": f"데이터 부족: {len(data)}행 (최소 {long_window}행 필요)",
                "metrics": {
                    "total_crossovers": 0,
                    "golden_crosses": 0,
                    "dead_crosses": 0,
                    "current_state": "unknown",
                },
                "details": pd.DataFrame(),
            }

        # SMA 계산
        data["sma_short"] = data["close"].rolling(window=short_window).mean()
        data["sma_long"] = data["close"].rolling(window=long_window).mean()

        # 크로스오버 탐지: 단기 - 장기의 부호 변화
        valid = data.dropna(subset=["sma_short", "sma_long"]).copy()
        valid["diff"] = valid["sma_short"] - valid["sma_long"]
        valid["prev_diff"] = valid["diff"].shift(1)

        # 부호 전환 지점 탐지
        crossovers = valid[
            (valid["diff"] * valid["prev_diff"] < 0) & valid["prev_diff"].notna()
        ].copy()

        crossovers["type"] = crossovers["diff"].apply(
            lambda x: "golden_cross" if x > 0 else "dead_cross"
        )

        golden_count = (crossovers["type"] == "golden_cross").sum()
        dead_count = (crossovers["type"] == "dead_cross").sum()

        # 현재 상태
        if len(valid) > 0:
            last_diff = valid["diff"].iloc[-1]
            current_state = "bullish" if last_diff > 0 else "bearish"
        else:
            current_state = "unknown"

        # 이벤트 DataFrame
        details = crossovers[["date", "close", "sma_short", "sma_long", "type"]].copy()
        details = details.reset_index(drop=True)

        summary = (
            f"SMA 크로스오버 분석 완료 (단기={short_window}, 장기={long_window}). "
            f"골든크로스 {golden_count}회, 데드크로스 {dead_count}회. "
            f"현재 상태: {current_state}."
        )

        return {
            "summary": summary,
            "metrics": {
                "total_crossovers": golden_count + dead_count,
                "golden_crosses": int(golden_count),
                "dead_crosses": int(dead_count),
                "current_state": current_state,
            },
            "details": details,
        }

    def generate_signals(self, df: pd.DataFrame, **params) -> list[Signal]:
        """
        골든크로스 = BUY, 데드크로스 = SELL 시그널을 생성한다.

        Args:
            df: OHLCV DataFrame
            **params: short_window, long_window

        Returns:
            Signal 리스트 (weight=1.0)
        """
        result = self.analyze(df, **params)
        details = result["details"]

        if details.empty:
            return []

        signals = []
        for _, row in details.iterrows():
            date_str = (
                row["date"].strftime("%Y-%m-%d")
                if hasattr(row["date"], "strftime")
                else str(row["date"])
            )
            if row["type"] == "golden_cross":
                signals.append(
                    Signal(
                        date=date_str,
                        signal_type=SignalType.BUY,
                        weight=1.0,
                    )
                )
            else:
                signals.append(
                    Signal(
                        date=date_str,
                        signal_type=SignalType.SELL,
                        weight=1.0,
                    )
                )

        return signals
