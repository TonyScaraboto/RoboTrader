from __future__ import annotations
from typing import Protocol, Sequence

class Strategy(Protocol):
    def generate_signals(self, closes: Sequence[float]) -> list[str]:
        ...
