# SMA Backtesting Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

A vectorized SMA crossover backtesting engine built in Python. Computes risk-adjusted performance metrics on historical OHLCV data and generates matplotlib visualizations.

## Features

- yfinance data loader with CSV caching
- Vectorized SMA signal generation (no `.iterrows()`)
- Look-ahead bias prevention via `shift(1)`
- Metrics: Sharpe Ratio, Max Drawdown, Cumulative Returns
- Charts: Price + SMA + trade markers, Cumulative Returns vs. Buy & Hold

## Project Structure

```
sma-backtesting-engine/
├── src/
│   ├── data_loader.py   # yfinance wrapper + CSV cache
│   ├── strategy.py      # SMA signal generation
│   ├── backtest.py      # Performance metrics
│   └── visualizer.py    # Matplotlib charts
├── tests/
├── data/                # CSV cache (gitignored)
├── output/              # Chart exports
├── main.py
└── requirements.txt
```

## Quickstart

```bash
git clone https://github.com/Diego-2510/sma-backtesting-engine.git
cd sma-backtesting-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Example Output (AAPL 2020–2024, SMA 20/50)

| Metric | Value |
|---|---|
| Strategy Return | 69.08% |
| Market Return | ~180% |
| Sharpe Ratio | ~0.45 |
| Max Drawdown | ~-18% |

## Design Rationale

**Vectorization:** All SMA and signal calculations use `pandas.rolling()` and boolean masking instead of row-by-row iteration, keeping computation O(n) and clean.

**Look-Ahead Bias:** Signals are shifted by one period (`shift(1)`) so a crossover detected on day N only triggers a position on day N+1 — as it would in live trading.

## Limitations

- Single asset, single strategy (SMA crossover only)
- No transaction costs or slippage modeled
- Risk-free rate assumed to be 0 for Sharpe calculation

## License

MIT License — see [LICENSE](LICENSE)
