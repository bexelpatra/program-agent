"""
Analyzer 엔트리포인트 (CLI).
argparse 기반 서브커맨드로 분석, 백테스팅, 전략 목록 조회를 지원한다.

실행 예시:
    python -m src.run_analyzer analyze --strategy moving_average --symbol ^GSPC
    python -m src.run_analyzer backtest --strategy moving_average --symbol ^GSPC --capital 10000
    python -m src.run_analyzer list
"""

import argparse
import sys
from datetime import datetime

from src.config import setup_logger
from src.database import Database
from src.analyzer import StrategyRegistry
from src.backtester import Backtester

logger = setup_logger("run_analyzer", "analyzer.log")


def cmd_analyze(args):
    """analyze 서브커맨드 실행."""
    strategy_name = args.strategy
    symbol = args.symbol
    start_date = args.start_date or "1900-01-01"
    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")

    logger.info(
        "분석 시작: strategy=%s, symbol=%s, period=%s~%s",
        strategy_name,
        symbol,
        start_date,
        end_date,
    )

    # 전략 조회
    try:
        strategy = StrategyRegistry.get(strategy_name)
    except KeyError as e:
        print(f"오류: {e}")
        sys.exit(1)

    # DB에서 데이터 조회
    db = Database()
    try:
        df = db.select_prices(symbol, start_date, end_date)
    finally:
        db.close()

    if df.empty:
        print(f"데이터 없음: {symbol} [{start_date} ~ {end_date}]")
        print("먼저 python -m src.run_collector 로 데이터를 수집하세요.")
        sys.exit(1)

    # 분석 실행
    result = strategy.analyze(df)

    # 결과 출력
    print("=" * 60)
    print(f"  ANALYSIS REPORT: {strategy.name}")
    print(f"  Symbol: {symbol}")
    print(f"  Period: {start_date} ~ {end_date}")
    print(f"  Data Points: {len(df)}")
    print("=" * 60)

    if "summary" in result:
        print()
        print("  Summary:")
        print(f"  {result['summary']}")

    if "metrics" in result and isinstance(result["metrics"], dict):
        print()
        print("-" * 60)
        print("  Metrics:")
        for key, value in result["metrics"].items():
            if isinstance(value, float):
                print(f"    {key}: {value:.6f}")
            else:
                print(f"    {key}: {value}")

    if "details" in result and hasattr(result["details"], "to_string"):
        print()
        print("-" * 60)
        print("  Details (last 10 rows):")
        print(result["details"].tail(10).to_string(index=False))

    print("=" * 60)
    logger.info("분석 완료: %s / %s", strategy_name, symbol)


def cmd_backtest(args):
    """backtest 서브커맨드 실행."""
    strategy_name = args.strategy
    symbol = args.symbol
    capital = args.capital
    commission = args.commission
    start_date = args.start_date or "1900-01-01"
    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")

    logger.info(
        "백테스트 시작: strategy=%s, symbol=%s, capital=%.2f, commission=%.4f, period=%s~%s",
        strategy_name,
        symbol,
        capital,
        commission,
        start_date,
        end_date,
    )

    # 전략 조회
    try:
        strategy = StrategyRegistry.get(strategy_name)
    except KeyError as e:
        print(f"오류: {e}")
        sys.exit(1)

    # DB에서 데이터 조회
    db = Database()
    try:
        df = db.select_prices(symbol, start_date, end_date)
    finally:
        db.close()

    if df.empty:
        print(f"데이터 없음: {symbol} [{start_date} ~ {end_date}]")
        print("먼저 python -m src.run_collector 로 데이터를 수집하세요.")
        sys.exit(1)

    # 시그널 생성
    signals = strategy.generate_signals(df)

    if not signals:
        print(f"전략 '{strategy_name}'이 시그널을 생성하지 않았습니다.")
        print("이 전략은 매매 시그널을 지원하지 않을 수 있습니다.")
        sys.exit(0)

    # 백테스팅 실행
    backtester = Backtester(
        initial_capital=capital,
        commission_rate=commission,
    )

    report = backtester.summary(signals, df)
    print(report)

    logger.info("백테스트 완료: %s / %s", strategy_name, symbol)


def cmd_list(args):
    """list 서브커맨드 실행."""
    strategies = StrategyRegistry.list_all()

    print("=" * 60)
    print("  REGISTERED STRATEGIES")
    print("=" * 60)

    if not strategies:
        print("  (등록된 전략 없음)")
    else:
        for name in strategies:
            strategy = StrategyRegistry.get(name)
            desc = strategy.description if strategy.description else "(설명 없음)"
            print(f"  - {name}: {desc}")

    print("=" * 60)
    print(f"  Total: {len(strategies)} strategies")


def build_parser() -> argparse.ArgumentParser:
    """argparse 파서를 구성하고 반환한다."""
    parser = argparse.ArgumentParser(
        prog="run_analyzer",
        description="Asset Price Analyzer & Backtester CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 커맨드")

    # analyze 서브커맨드
    analyze_parser = subparsers.add_parser("analyze", help="특정 전략으로 심볼 분석")
    analyze_parser.add_argument(
        "--strategy", required=True, help="전략 이름 (예: moving_average)"
    )
    analyze_parser.add_argument("--symbol", required=True, help="티커 심볼 (예: ^GSPC)")
    analyze_parser.add_argument(
        "--start-date", default=None, help="분석 시작일 (YYYY-MM-DD)"
    )
    analyze_parser.add_argument("--end-date", default=None, help="분석 종료일 (YYYY-MM-DD)")

    # backtest 서브커맨드
    backtest_parser = subparsers.add_parser("backtest", help="특정 전략으로 백테스팅")
    backtest_parser.add_argument(
        "--strategy", required=True, help="전략 이름 (예: moving_average)"
    )
    backtest_parser.add_argument("--symbol", required=True, help="티커 심볼 (예: ^GSPC)")
    backtest_parser.add_argument(
        "--capital", type=float, default=10000.0, help="초기 자본 (기본: 10000)"
    )
    backtest_parser.add_argument(
        "--commission", type=float, default=0.001, help="수수료율 (기본: 0.001)"
    )
    backtest_parser.add_argument(
        "--start-date", default=None, help="백테스트 시작일 (YYYY-MM-DD)"
    )
    backtest_parser.add_argument(
        "--end-date", default=None, help="백테스트 종료일 (YYYY-MM-DD)"
    )

    # list 서브커맨드
    subparsers.add_parser("list", help="등록된 전략 목록 출력")

    return parser


def main():
    """Analyzer CLI 메인 함수."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    commands = {
        "analyze": cmd_analyze,
        "backtest": cmd_backtest,
        "list": cmd_list,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
