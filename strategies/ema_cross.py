from __future__ import annotations
import numpy as np

class EMACross:
    def __init__(self, fast: int = 12, slow: int = 26) -> None:
        self.fast = fast
        self.slow = slow

    def _ema(self, arr: np.ndarray, period: int) -> np.ndarray:
        k = 2 / (period + 1)
        ema = np.empty_like(arr)
        ema[0] = arr[0]
        for i in range(1, len(arr)):
            ema[i] = arr[i] * k + ema[i-1] * (1 - k)
        return ema

    def generate_signals(self, closes: list[float]) -> list[str]:
        arr = np.asarray(closes, dtype=float)
        if len(arr) < max(self.fast, self.slow):
            return ["hold"] * len(arr)
        f = self._ema(arr, self.fast)
        s = self._ema(arr, self.slow)
        signals = []
        for i in range(len(arr)):
            if i == 0:
                signals.append("hold")
                continue
            if f[i-1] <= s[i-1] and f[i] > s[i]:
                signals.append("buy")
            elif f[i-1] >= s[i-1] and f[i] < s[i]:
                signals.append("sell")
            else:
                signals.append("hold")
        return signals
