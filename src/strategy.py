"""Strategy module for vectorized SMA signal generation."""

import pandas as pd


def generate_sma_signals(
    df: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.DataFrame:
    """
    Generate vectorized SMA crossover signals.

    Args:
        df:            DataFrame with at least a 'Close' column
        short_window:  Short SMA period
        long_window:   Long SMA period

    Returns:
        DataFrame with SMA columns, signal, position, strategy_return
    """
    if "Close" not in df.columns:
        raise ValueError("DataFrame must contain a 'Close' column")
    if short_window <= 0 or long_window <= 0:
        raise ValueError("Window sizes must be positive integers")
    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window")

    data = df.copy()

    data["return"] = data["Close"].pct_change()
    data["sma_short"] = data["Close"].rolling(window=short_window).mean()
    data["sma_long"] = data["Close"].rolling(window=long_window).mean()

    data["signal"] = 0
    data.loc[data["sma_short"] > data["sma_long"], "signal"] = 1

    # shift(1) prevents look-ahead bias: signal from day N executes on day N+1
    data["position"] = data["signal"].shift(1).fillna(0)
    data["position_change"] = data["position"].diff().fillna(0)

    data["strategy_return"] = data["position"] * data["return"]

    return data
