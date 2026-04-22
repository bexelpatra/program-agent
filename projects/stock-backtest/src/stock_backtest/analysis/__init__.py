"""Analysis subpackage: seasonality, political cycle, etc."""

from stock_backtest.analysis.political_cycle import (
    earnings_season_effect,
    election_year_effect,
    fomc_week_effect,
    presidential_term_year_effect,
)
from stock_backtest.analysis.seasonality import (
    daily_returns,
    day_of_week_effect,
    halloween_indicator,
    month_edge_effect,
    monthly_effect,
    sell_in_may,
)
from stock_backtest.analysis.stats import (
    annotate_significance,
    bootstrap_ci,
    bootstrap_mean_diff,
    welch_t_test,
)

__all__ = [
    "daily_returns",
    "monthly_effect",
    "day_of_week_effect",
    "month_edge_effect",
    "sell_in_may",
    "halloween_indicator",
    "presidential_term_year_effect",
    "election_year_effect",
    "fomc_week_effect",
    "earnings_season_effect",
    "welch_t_test",
    "bootstrap_mean_diff",
    "bootstrap_ci",
    "annotate_significance",
]
