"""Backtesting metrics: Sharpe Ratio, Max Drawdown, cumulative returns."""

import numpy as np
import pandas as pd


def compute_metrics(data: pd.DataFrame, trading_days: int = 252) -> dict:
    """
    Compute performance metrics for a backtested strategy.

    Args:
        data:         Output DataFrame from generate_sma_signals()
        trading_days: Annualization factor (252 for stocks)

    Returns:
        Dictionary with cumulative returns, Sharpe Ratio, Max Drawdown
    """
    strategy_ret = data["strategy_return"].dropna()
    market_ret = data["return"].dropna()

    cum_strategy = (1 + strategy_ret).cumprod()
    cum_market = (1 + market_ret).cumprod()

    total_strategy_return = cum_strategy.iloc[-1] - 1
    total_market_return = cum_market.iloc[-1] - 1

    # Sharpe Ratio: annualized mean / std (assumes risk-free rate = 0)
    sharpe = (
        strategy_ret.mean() / strategy_ret.std() * np.sqrt(trading_days)
        if strategy_ret.std() != 0
        else 0.0
    )

    # Max Drawdown: largest peak-to-trough decline
    rolling_max = cum_strategy.cummax()
    drawdown = (cum_strategy - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    return {
        "total_strategy_return": round(total_strategy_return * 100, 2),
        "total_market_return": round(total_market_return * 100, 2),
        "sharpe_ratio": round(sharpe, 4),
        "max_drawdown": round(max_drawdown * 100, 2),
        "cum_strategy": cum_strategy,
        "cum_market": cum_market,
    }
