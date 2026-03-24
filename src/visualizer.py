"""Visualization module for SMA strategy results."""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def plot_sma_signals(data: pd.DataFrame, ticker: str = "") -> None:
    """Plot price chart with SMA lines and trade entry/exit markers."""
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(data.index, data["Close"], label="Close", linewidth=1.2, color="#333333")
    ax.plot(data.index, data["sma_short"], label=f"SMA Short", linewidth=1.2,
            color="#1f77b4", linestyle="--")
    ax.plot(data.index, data["sma_long"], label=f"SMA Long", linewidth=1.2,
            color="#ff7f0e", linestyle="--")

    entries = data[data["position_change"] == 1]
    exits = data[data["position_change"] == -1]

    ax.scatter(entries.index, entries["Close"], marker="^", color="green",
               zorder=5, s=80, label="Entry")
    ax.scatter(exits.index, exits["Close"], marker="v", color="red",
               zorder=5, s=80, label="Exit")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)

    title = f"{ticker} — SMA Crossover Strategy" if ticker else "SMA Crossover Strategy"
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"output/{ticker}_sma_chart.png", dpi=150)
    plt.show()


def plot_cumulative_returns(metrics: dict, ticker: str = "") -> None:
    """Plot cumulative returns: strategy vs. buy-and-hold."""
    fig, ax = plt.subplots(figsize=(14, 5))

    cum_strategy = metrics["cum_strategy"]
    cum_market = metrics["cum_market"]

    ax.plot(cum_strategy.index, cum_strategy, label="SMA Strategy",
            linewidth=1.5, color="#1f77b4")
    ax.plot(cum_market.index, cum_market, label="Buy & Hold",
            linewidth=1.5, color="#ff7f0e", linestyle="--")

    ax.axhline(1, color="grey", linewidth=0.8, linestyle=":")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)

    title = f"{ticker} — Cumulative Returns" if ticker else "Cumulative Returns"
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("Cumulative Return (1 = 100%)")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"output/{ticker}_returns_chart.png", dpi=150)
    plt.show()
