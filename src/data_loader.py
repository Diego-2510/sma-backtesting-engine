"""Data loader module with yfinance wrapper and CSV caching."""

import os
from datetime import datetime

import pandas as pd
import yfinance as yf


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _cache_path(ticker: str, start: str, end: str) -> str:
    """Generate cache file path based on ticker and date range."""
    return os.path.join(DATA_DIR, f"{ticker}_{start}_{end}.csv")


def _validate(df: pd.DataFrame, ticker: str, start: str, end: str) -> pd.DataFrame:
    """Validate downloaded OHLCV data."""
    required_cols = {"Open", "High", "Low", "Close", "Volume"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns for {ticker}: {missing}")

    if df.empty:
        raise ValueError(f"No data returned for {ticker} ({start} to {end})")

    nan_pct = df[list(required_cols)].isna().mean()
    critical = nan_pct[nan_pct > 0.05]
    if not critical.empty:
        raise ValueError(f"NaN ratio exceeds 5% in: {critical.to_dict()}")

    df = df.dropna(subset=["Close"])

    actual_start = df.index.min().strftime("%Y-%m-%d")
    actual_end = df.index.max().strftime("%Y-%m-%d")
    print(f"[INFO] {ticker}: {len(df)} rows | {actual_start} → {actual_end}")

    return df


def load_data(
    ticker: str,
    start: str,
    end: str,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Load OHLCV data for a ticker. Uses CSV cache if available.

    Args:
        ticker:    Stock symbol (e.g. "AAPL")
        start:     Start date "YYYY-MM-DD"
        end:       End date "YYYY-MM-DD"
        use_cache: Read/write from data/ cache

    Returns:
        DataFrame with DatetimeIndex and OHLCV columns.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    cache_file = _cache_path(ticker, start, end)

    if use_cache and os.path.exists(cache_file):
        print(f"[CACHE] Loading {cache_file}")
        df = pd.read_csv(cache_file, index_col="Date", parse_dates=True)
        return df

    print(f"[DOWNLOAD] {ticker} from {start} to {end}")
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = _validate(df, ticker, start, end)

    if use_cache:
        df.to_csv(cache_file)
        print(f"[CACHE] Saved to {cache_file}")

    return df
