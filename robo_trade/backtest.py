from __future__ import annotations
from typing import Sequence

class Backtester:
    def run(self, closes: Sequence[float], signals: Sequence[str], initial_cash: float = 1000.0):
        cash = initial_cash
        position = 0.0
        equity_curve = []
        for price, sig in zip(closes, signals):
            if sig == "buy" and cash > 0:
                position = cash / price
                cash = 0.0
            elif sig == "sell" and position > 0:
                cash = position * price
                position = 0.0
            equity = cash + position * price
            equity_curve.append(equity)
        return {
            "final_equity": equity_curve[-1] if equity_curve else initial_cash,
            "equity_curve": equity_curve,
        }
