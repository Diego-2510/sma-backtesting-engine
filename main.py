"""Entry point: runs full SMA backtest pipeline."""

import os
from src.data_loader import load_data
from src.strategy import generate_sma_signals
from src.backtest import compute_metrics
from src.visualizer import plot_sma_signals, plot_cumulative_returns

os.makedirs("output", exist_ok=True)

TICKER = "AAPL"
START = "2020-01-01"
END = "2024-01-01"
SHORT_WINDOW = 20
LONG_WINDOW = 50

if __name__ == "__main__":
    df = load_data(TICKER, START, END)
    data = generate_sma_signals(df, short_window=SHORT_WINDOW, long_window=LONG_WINDOW)
    metrics = compute_metrics(data)

    print(f"\n{'='*40}")
    print(f"  Backtest Results — {TICKER}")
    print(f"{'='*40}")
    print(f"  Strategy Return : {metrics['total_strategy_return']}%")
    print(f"  Market Return   : {metrics['total_market_return']}%")
    print(f"  Sharpe Ratio    : {metrics['sharpe_ratio']}")
    print(f"  Max Drawdown    : {metrics['max_drawdown']}%")
    print(f"{'='*40}\n")

    plot_sma_signals(data, ticker=TICKER)
    plot_cumulative_returns(metrics, ticker=TICKER)
