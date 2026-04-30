"""backtest_runner 분해 함수 단위 테스트 (TASK-232).

`_persist_results` 가 3 책임을 갖던 단일 함수에서 3 헬퍼로 분해:
- `_build_equity_rows`: equity peak 추적 + drawdown 즉석 계산
- `_build_trade_dicts`: TradeFill → DB row dict (Decimal 변환 + UTC midnight)
- `_compute_and_flatten_metrics`: compute_metrics + annual/monthly flatten

각 헬퍼의 핵심 패턴을 회귀로 묶는다 (DB 의존 없음 — 순수 함수).
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from app.domain.engine import BacktestEquityPoint
from app.domain.trade import TradeFill
from app.services.backtest_runner import (
    _build_equity_rows,
    _build_trade_dicts,
    _compute_and_flatten_metrics,
)


class TestBuildEquityRows:
    """equity peak 추적 + drawdown 즉석 계산.

    drawdown = equity / running_peak - 1. peak 갱신 후의 첫 행은 drawdown=0,
    peak 미만으로 떨어진 행은 음수.
    """

    def test_monotonic_increasing_curve_has_zero_drawdown(self) -> None:
        """equity 가 단조 증가하면 모든 row 의 drawdown 은 0."""
        curve = [
            BacktestEquityPoint(
                time=date(2024, 1, i),
                equity=Decimal(str(100 + i * 10)),
                cash_total_in_base=Decimal("0"),
            )
            for i in range(1, 4)
        ]
        rows = _build_equity_rows(curve)

        assert len(rows) == 3
        for _time, _equity, _cash, drawdown in rows:
            assert drawdown == Decimal("0")

    def test_peak_then_drop_records_negative_drawdown(self) -> None:
        """peak (200) 후 100 으로 떨어지면 drawdown = -0.5."""
        curve = [
            BacktestEquityPoint(
                time=date(2024, 1, 1),
                equity=Decimal("100"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2024, 1, 2),
                equity=Decimal("200"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2024, 1, 3),
                equity=Decimal("100"),
                cash_total_in_base=Decimal("0"),
            ),
        ]
        rows = _build_equity_rows(curve)

        # row[0]: peak=100, dd=0
        assert rows[0][3] == Decimal("0")
        # row[1]: peak=200 갱신, dd=0
        assert rows[1][3] == Decimal("0")
        # row[2]: peak=200 유지, equity=100 → dd = 100/200 - 1 = -0.5
        assert rows[2][3] == Decimal("100") / Decimal("200") - Decimal("1")

    def test_time_converts_to_utc_midnight_datetime(self) -> None:
        """date → datetime(UTC midnight) 변환. tzinfo 가 timezone.utc."""
        curve = [
            BacktestEquityPoint(
                time=date(2024, 6, 15),
                equity=Decimal("100"),
                cash_total_in_base=Decimal("50"),
            ),
        ]
        rows = _build_equity_rows(curve)

        assert rows[0][0] == datetime(2024, 6, 15, 0, 0, 0, tzinfo=timezone.utc)
        assert rows[0][1] == Decimal("100")
        assert rows[0][2] == Decimal("50")

    def test_empty_curve_returns_empty_list(self) -> None:
        """빈 입력 → 빈 출력."""
        assert _build_equity_rows([]) == []


class TestBuildTradeDicts:
    """TradeFill → backtest_trades insert dict.

    핵심 변환:
    - settlement_date (date) → time (datetime, UTC midnight)
    - qty_filled (Decimal) 그대로, 그 외 price/commission 도 Decimal 화
    """

    def test_decimal_qty_preserved_and_time_is_utc_midnight(self) -> None:
        """Decimal qty 가 그대로 보존되고 time 이 settlement_date 의 UTC midnight."""
        fill = TradeFill(
            asset_id=42,
            side="BUY",
            qty_filled=Decimal("3.14159265"),
            price=Decimal("100.50"),
            commission=Decimal("0.05"),
            currency="USD",
            settlement_date=date(2024, 3, 15),
        )

        dicts = _build_trade_dicts([fill])

        assert len(dicts) == 1
        d = dicts[0]
        assert d["asset_id"] == 42
        assert d["side"] == "BUY"
        assert d["qty"] == Decimal("3.14159265")
        assert d["price"] == Decimal("100.50")
        assert d["commission"] == Decimal("0.05")
        assert d["currency"] == "USD"
        assert d["time"] == datetime(2024, 3, 15, 0, 0, 0, tzinfo=timezone.utc)

    def test_settlement_date_drives_time_not_now(self) -> None:
        """TASK-212 회귀: time 이 datetime.now() fallback 이 아니라 settlement_date 기반."""
        # 과거 일자 — datetime.now() fallback 이 적용됐다면 오늘 일자로 기록됐을 것.
        fill = TradeFill(
            asset_id=1,
            side="SELL",
            qty_filled=Decimal("10"),
            price=Decimal("50"),
            commission=Decimal("0"),
            currency="KRW",
            settlement_date=date(2010, 1, 4),
        )

        dicts = _build_trade_dicts([fill])

        assert dicts[0]["time"] == datetime(2010, 1, 4, 0, 0, 0, tzinfo=timezone.utc)

    def test_empty_fills_returns_empty_list(self) -> None:
        assert _build_trade_dicts([]) == []


class TestComputeAndFlattenMetrics:
    """compute_metrics 결과를 backtest_metrics 적재 dict 로 flatten.

    핵심 패턴:
    - cagr/mdd/sharpe/sortino/calmar/win_rate 6개는 이름 그대로 키
    - annual_returns: {YYYY: ret} → "annual_return_{YYYY}" 키
    - monthly_returns: {"YYYY-MM": ret} → "monthly_return_{YYYY-MM}" 키
    """

    def test_flat_keys_include_six_base_metrics(self) -> None:
        """6개 기본 메트릭 키가 모두 존재."""
        # 2 년 이상 걸친 단조 증가 curve — 다양한 metric 이 0 이 아닌 값을 갖게.
        curve = [
            BacktestEquityPoint(
                time=date(2023, 1, 2),
                equity=Decimal("100"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2023, 12, 29),
                equity=Decimal("110"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2024, 12, 31),
                equity=Decimal("120"),
                cash_total_in_base=Decimal("0"),
            ),
        ]
        flat = _compute_and_flatten_metrics(curve)

        for key in ("cagr", "mdd", "sharpe", "sortino", "calmar", "win_rate"):
            assert key in flat, f"missing base metric: {key}"

    def test_annual_returns_flatten_to_annual_return_year_keys(self) -> None:
        """annual_returns 가 'annual_return_{YYYY}' prefix 로 flatten."""
        curve = [
            BacktestEquityPoint(
                time=date(2023, 1, 2),
                equity=Decimal("100"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2023, 12, 29),
                equity=Decimal("110"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2024, 12, 31),
                equity=Decimal("120"),
                cash_total_in_base=Decimal("0"),
            ),
        ]
        flat = _compute_and_flatten_metrics(curve)

        annual_keys = [k for k in flat if k.startswith("annual_return_")]
        # 적어도 한 해는 등록돼야 한다.
        assert len(annual_keys) >= 1
        # 키 형식은 annual_return_{4자리 연도}
        for k in annual_keys:
            year_str = k.removeprefix("annual_return_")
            assert year_str.isdigit() and len(year_str) == 4

    def test_monthly_returns_flatten_to_monthly_return_yyyymm_keys(self) -> None:
        """monthly_returns 가 'monthly_return_{YYYY-MM}' prefix 로 flatten."""
        curve = [
            BacktestEquityPoint(
                time=date(2024, 1, 2),
                equity=Decimal("100"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2024, 1, 31),
                equity=Decimal("105"),
                cash_total_in_base=Decimal("0"),
            ),
            BacktestEquityPoint(
                time=date(2024, 2, 29),
                equity=Decimal("108"),
                cash_total_in_base=Decimal("0"),
            ),
        ]
        flat = _compute_and_flatten_metrics(curve)

        monthly_keys = [k for k in flat if k.startswith("monthly_return_")]
        assert len(monthly_keys) >= 1
        for k in monthly_keys:
            ym = k.removeprefix("monthly_return_")
            # YYYY-MM 형식
            assert len(ym) == 7 and ym[4] == "-"
            assert ym[:4].isdigit() and ym[5:].isdigit()

    def test_empty_curve_yields_zero_base_metrics_only(self) -> None:
        """빈 curve → 기본 6개 메트릭은 0.0, annual/monthly 키는 없음."""
        flat = _compute_and_flatten_metrics([])

        assert flat["cagr"] == 0.0
        assert flat["mdd"] == 0.0
        assert flat["sharpe"] == 0.0
        assert flat["sortino"] == 0.0
        assert flat["calmar"] == 0.0
        assert flat["win_rate"] == 0.0
        assert not any(k.startswith("annual_return_") for k in flat)
        assert not any(k.startswith("monthly_return_") for k in flat)
