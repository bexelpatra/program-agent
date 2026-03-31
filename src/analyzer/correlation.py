"""
자산 간 상관관계 분석 전략.
여러 심볼의 종가 데이터를 받아 상관관계 행렬과 롤링 상관관계를 계산한다.
"""

import pandas as pd
import numpy as np

from src.analyzer.base import BaseStrategy


class CorrelationStrategy(BaseStrategy):
    """자산 간 상관관계 분석 전략."""

    @property
    def name(self) -> str:
        return "correlation"

    @property
    def description(self) -> str:
        return "자산 간 상관관계 행렬 및 롤링 상관관계 분석"

    def analyze(self, df: pd.DataFrame, **params) -> dict:
        """
        여러 심볼의 종가 데이터로 상관관계를 분석한다.

        Args:
            df: 멀티 심볼 피벗 테이블 DataFrame.
                - 인덱스: date
                - 컬럼: 심볼명 (예: "^GSPC", "GC=F", "TLT")
                - 값: 종가 (close)
            **params:
                rolling_window (int): 롤링 상관관계 윈도우. 기본 60일.
                method (str): 상관관계 방법. 기본 "pearson".

        Returns:
            {
                "summary": 분석 요약 텍스트,
                "metrics": {
                    "correlation_matrix": 전체 기간 상관관계 행렬 (dict of dict),
                    "significant_changes": 주요 상관관계 변화 목록,
                },
                "details": 롤링 상관관계 DataFrame,
            }
        """
        rolling_window = params.get("rolling_window", 60)
        method = params.get("method", "pearson")

        # 입력 검증
        if df.empty or df.shape[1] < 2:
            return {
                "summary": "상관관계 분석에는 최소 2개 이상의 심볼 데이터가 필요합니다.",
                "metrics": {
                    "correlation_matrix": {},
                    "significant_changes": [],
                },
                "details": pd.DataFrame(),
            }

        # 인덱스를 datetime으로 변환
        data = df.copy()
        data.index = pd.to_datetime(data.index)
        data = data.sort_index().dropna()

        if len(data) < rolling_window:
            return {
                "summary": f"데이터 부족: {len(data)}행 (최소 {rolling_window}행 필요)",
                "metrics": {
                    "correlation_matrix": {},
                    "significant_changes": [],
                },
                "details": pd.DataFrame(),
            }

        # 일간 수익률 기반 상관관계 (가격 수준이 다르므로 수익률로 정규화)
        returns = data.pct_change().dropna()

        # 전체 기간 상관관계 행렬
        corr_matrix = returns.corr(method=method)
        corr_dict = corr_matrix.to_dict()

        # 롤링 상관관계 계산 (모든 심볼 쌍)
        symbols = list(data.columns)
        rolling_corr_frames = []

        for i in range(len(symbols)):
            for j in range(i + 1, len(symbols)):
                sym_a = symbols[i]
                sym_b = symbols[j]
                pair_name = f"{sym_a}_vs_{sym_b}"

                rolling = (
                    returns[sym_a].rolling(window=rolling_window).corr(returns[sym_b])
                )
                rolling_corr_frames.append(rolling.rename(pair_name))

        if rolling_corr_frames:
            rolling_df = pd.concat(rolling_corr_frames, axis=1).dropna()
        else:
            rolling_df = pd.DataFrame()

        # 주요 상관관계 변화 감지: 최근 값과 전체 평균의 차이가 큰 쌍
        significant_changes = []
        for col in rolling_df.columns:
            overall_mean = rolling_df[col].mean()
            recent_mean = rolling_df[col].iloc[-rolling_window:].mean()
            change = recent_mean - overall_mean

            if abs(change) > 0.2:  # 상관관계 0.2 이상 변화 시 유의미
                significant_changes.append(
                    {
                        "pair": col,
                        "overall_corr": round(float(overall_mean), 4),
                        "recent_corr": round(float(recent_mean), 4),
                        "change": round(float(change), 4),
                        "direction": "증가" if change > 0 else "감소",
                    }
                )

        # 요약 텍스트
        summary_parts = [
            f"상관관계 분석 완료 ({len(symbols)}개 심볼, {len(returns)}거래일, "
            f"롤링 윈도우={rolling_window}일)."
        ]
        if significant_changes:
            summary_parts.append(f"주요 변화 감지: {len(significant_changes)}건.")
            for ch in significant_changes:
                summary_parts.append(
                    f"  - {ch['pair']}: {ch['overall_corr']:.3f} → "
                    f"{ch['recent_corr']:.3f} ({ch['direction']})"
                )
        else:
            summary_parts.append("주요 상관관계 변화 없음.")

        return {
            "summary": "\n".join(summary_parts),
            "metrics": {
                "correlation_matrix": corr_dict,
                "significant_changes": significant_changes,
            },
            "details": rolling_df,
        }
