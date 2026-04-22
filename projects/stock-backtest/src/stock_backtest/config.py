"""Configuration loader and schema for stock-backtest.

Loads ``config/defaults.yaml`` into a validated Pydantic v2 model tree
(:class:`Settings`) and provides resolution helpers for market-level cost
overrides and tax profile access.

Environment variable ``STOCK_BACKTEST_CONFIG`` overrides the config path.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    model_validator,
)


# ---------------------------------------------------------------------------
# Costs
# ---------------------------------------------------------------------------


class MarketCostOverride(BaseModel):
    """Market-specific overrides for trading costs. All fields are optional;
    missing fields inherit from the top-level :class:`CostsConfig` values."""

    model_config = ConfigDict(extra="forbid")

    commission_buy_bps: NonNegativeFloat | None = None
    commission_sell_bps: NonNegativeFloat | None = None
    slippage_bps: NonNegativeFloat | None = None
    fx_spread_bps: NonNegativeFloat | None = None


class CostsConfig(BaseModel):
    """Top-level trading cost configuration with per-market overrides."""

    model_config = ConfigDict(extra="forbid")

    commission_buy_bps: NonNegativeFloat = 15
    commission_sell_bps: NonNegativeFloat = 15
    slippage_bps: NonNegativeFloat = 5
    fx_spread_bps: NonNegativeFloat = 20
    market_overrides: dict[str, MarketCostOverride] = Field(default_factory=dict)


class CostsResolved(BaseModel):
    """Fully-resolved trading costs for a specific market (no Nones)."""

    model_config = ConfigDict(extra="forbid")

    market: str
    commission_buy_bps: NonNegativeFloat
    commission_sell_bps: NonNegativeFloat
    slippage_bps: NonNegativeFloat
    fx_spread_bps: NonNegativeFloat


# ---------------------------------------------------------------------------
# Rebalance
# ---------------------------------------------------------------------------


RebalanceFrequency = Literal["D", "W", "ME", "Q", "Y", "threshold"]


class RebalanceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    frequency: RebalanceFrequency = "ME"
    threshold_pct: float | None = None

    @model_validator(mode="after")
    def _validate_threshold(self) -> "RebalanceConfig":
        if self.frequency == "threshold":
            if self.threshold_pct is None:
                raise ValueError(
                    "rebalance.threshold_pct must be set when frequency='threshold'"
                )
            if self.threshold_pct <= 0:
                raise ValueError("rebalance.threshold_pct must be > 0")
        return self


# ---------------------------------------------------------------------------
# Tax
# ---------------------------------------------------------------------------


class TaxProfile(BaseModel):
    """A single tax profile. All fields optional to allow empty profiles
    (e.g. ``none: {}``) used when tax is disabled or for comparison runs."""

    model_config = ConfigDict(extra="allow")

    overseas_capital_gains_rate: float | None = None
    overseas_annual_deduction_krw: NonNegativeInt | None = None
    overseas_dividend_rate: float | None = None
    crypto_enabled: bool | None = None
    crypto_capital_gains_rate: float | None = None
    crypto_annual_deduction_krw: NonNegativeInt | None = None


class TaxConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    profile: str = "kr_resident"
    profiles: dict[str, TaxProfile] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_profile_exists(self) -> "TaxConfig":
        if self.enabled and self.profile not in self.profiles:
            raise ValueError(
                f"tax.profile='{self.profile}' not found in tax.profiles "
                f"(available: {sorted(self.profiles.keys())})"
            )
        return self


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------


class RateLimitConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    yfinance_requests_per_sec: float = 1.5
    pykrx_min_interval_ms: NonNegativeInt = 100


class IngestionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    retry_max: NonNegativeInt = 3
    retry_backoff_seconds: list[NonNegativeFloat] = Field(
        default_factory=lambda: [1, 2, 4]
    )
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    reject_close_zero_or_null: bool = True


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------


class ReproducibilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stale_run_warning: bool = True


# ---------------------------------------------------------------------------
# Top-level Settings
# ---------------------------------------------------------------------------


MarketMode = Literal["STOCK", "CRYPTO", "MIXED"]


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_currency: str = "USD"
    market_mode: MarketMode = "STOCK"
    costs: CostsConfig = Field(default_factory=CostsConfig)
    rebalance: RebalanceConfig = Field(default_factory=RebalanceConfig)
    calendars: dict[str, str] = Field(default_factory=dict)
    crypto_daily_cutoff_utc: str = "00:00"
    tax: TaxConfig = Field(default_factory=TaxConfig)
    ingestion: IngestionConfig = Field(default_factory=IngestionConfig)
    reproducibility: ReproducibilityConfig = Field(
        default_factory=ReproducibilityConfig
    )


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------


def _default_config_path() -> Path:
    # src/stock_backtest/config.py -> project root = parents[2]
    return Path(__file__).resolve().parents[2] / "config" / "defaults.yaml"


def load_config(path: Path | str | None = None) -> Settings:
    """Load and validate configuration.

    Resolution order:
      1. Explicit ``path`` argument.
      2. ``STOCK_BACKTEST_CONFIG`` environment variable.
      3. ``projects/stock-backtest/config/defaults.yaml`` (package default).
    """

    if path is None:
        env_path = os.environ.get("STOCK_BACKTEST_CONFIG")
        path = Path(env_path) if env_path else _default_config_path()
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return Settings.model_validate(raw)


# ---------------------------------------------------------------------------
# Convenience accessors
# ---------------------------------------------------------------------------


def get_costs(settings: Settings, market: str) -> CostsResolved:
    """Resolve effective trading costs for ``market`` by merging market-level
    overrides onto the top-level defaults. Unknown markets fall back to
    top-level defaults entirely."""

    base = settings.costs
    override = base.market_overrides.get(market)

    def pick(attr: str) -> float:
        if override is not None:
            val = getattr(override, attr)
            if val is not None:
                return val
        return getattr(base, attr)

    return CostsResolved(
        market=market,
        commission_buy_bps=pick("commission_buy_bps"),
        commission_sell_bps=pick("commission_sell_bps"),
        slippage_bps=pick("slippage_bps"),
        fx_spread_bps=pick("fx_spread_bps"),
    )


def get_tax_profile(settings: Settings) -> TaxProfile | None:
    """Return the active tax profile, or ``None`` if taxation is disabled."""

    if not settings.tax.enabled:
        return None
    return settings.tax.profiles[settings.tax.profile]
