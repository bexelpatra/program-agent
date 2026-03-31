"""
STL 계절성 분해 전략.
statsmodels의 STL(Seasonal and Trend decomposition using Loess)을 사용하여
종가 시계열을 추세/계절성/잔차로 분해한다.
"""

import pandas as pd
from statsmodels.tsa.seasonal import STL

from src.analyzer.base import BaseStrategy


class SeasonalityStrategy(BaseStrategy):
    """STL 계절성 분해 전략."""

    @property
    def name(self) -> str:
        return "seasonality"

    @property
    def description(self) -> str:
        return "STL 분해를 통한 계절성/추세/잔차 분석"

    def analyze(self, df: pd.DataFrame, **params) -> dict:
        """
        종가 시계열을 STL로 분해한다.

        Args:
            df: OHLCV DataFrame (date, close 컬럼 필수)
            **params:
                period (int): 계절성 주기. 기본 252 (연간 거래일).

        Returns:
            {
                "summary": 분석 요약 텍스트,
                "metrics": {
                    "seasonal_strength": 계절성 강도 (0~1),
                    "trend_direction": 추세 방향 ("up" / "down" / "flat"),
                },
                "details": 분해 결과 DataFrame (date, close, trend, seasonal, resid),
            }
        """
        period = params.get("period", 252)

        # 날짜 인덱스 설정 및 종가 시리즈 준비
        series = df.set_index("date")["close"].copy()
        series.index = pd.to_datetime(series.index)
        series = series.sort_index().dropna()

        # 데이터가 주기의 2배 이상 필요
        if len(series) < period * 2:
            return {
                "summary": f"데이터 부족: {len(series)}행 (최소 {period * 2}행 필요)",
                "metrics": {"seasonal_strength": 0.0, "trend_direction": "unknown"},
                "details": pd.DataFrame(),
            }

        # STL 분해
        stl = STL(series, period=period, robust=True)
        result = stl.fit()

        # 계절성 강도: 1 - Var(Resid) / Var(Seasonal + Resid)
        seasonal_plus_resid = result.seasonal + result.resid
        var_resid = result.resid.var()
        var_seasonal_resid = seasonal_plus_resid.var()

        if var_seasonal_resid > 0:
            seasonal_strength = max(0.0, 1.0 - var_resid / var_seasonal_resid)
        else:
            seasonal_strength = 0.0

        # 추세 방향: 마지막 period 구간의 추세 기울기
        trend_recent = result.trend.iloc[-period:]
        if len(trend_recent) >= 2:
            slope = trend_recent.iloc[-1] - trend_recent.iloc[0]
            threshold = abs(trend_recent.mean()) * 0.01  # 1% 임계값
            if slope > threshold:
                trend_direction = "up"
            elif slope < -threshold:
                trend_direction = "down"
            else:
                trend_direction = "flat"
        else:
            trend_direction = "unknown"

        # 분해 결과 DataFrame
        details = pd.DataFrame(
            {
                "date": series.index,
                "close": series.values,
                "trend": result.trend.values,
                "seasonal": result.seasonal.values,
                "resid": result.resid.values,
            }
        )

        summary = (
            f"STL 분해 완료 (period={period}, 데이터 {len(series)}행). "
            f"계절성 강도: {seasonal_strength:.3f}, 추세 방향: {trend_direction}."
        )

        return {
            "summary": summary,
            "metrics": {
                "seasonal_strength": round(seasonal_strength, 4),
                "trend_direction": trend_direction,
            },
            "details": details,
        }
