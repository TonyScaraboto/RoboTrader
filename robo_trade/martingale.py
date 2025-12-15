from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Sequence
from .config import settings

Direction = Literal["green", "red"]

@dataclass
class MartingaleConfig:
    stakes_brl: List[float] = None

    def __post_init__(self):
        if self.stakes_brl is None:
            self.stakes_brl = [2, 4, 10, 20, 50, 100, 200, 400]
        if len(self.stakes_brl) != 8:
            raise ValueError("stakes_brl must have 8 values")

@dataclass
class MartingaleResult:
    total_profit_brl: float
    sequence_results: List[dict]

class MartingaleManager:
    def __init__(self, config: MartingaleConfig | None = None) -> None:
        self.config = config or MartingaleConfig()

    @staticmethod
    def candle_direction(open_: float, close: float) -> Direction:
        return "green" if close >= open_ else "red"

    def run(self, opens: Sequence[float], closes: Sequence[float]) -> MartingaleResult:
        if len(opens) != len(closes):
            raise ValueError("opens and closes must be same length")
        if len(opens) < 2:
            return MartingaleResult(total_profit_brl=0.0, sequence_results=[])

        results: List[dict] = []
        total_profit = 0.0

        # We define a 'victory' when next candle direction equals the previous candle direction.
        # Entry direction is the previous candle's color.
        stake_index = 0
        current_direction: Direction | None = None

        for i in range(1, len(opens)):
            prev_dir = self.candle_direction(opens[i-1], closes[i-1])
            this_dir = self.candle_direction(opens[i], closes[i])

            # If this is a new sequence or we had a victory, reset to base stake.
            if current_direction is None:
                current_direction = prev_dir
                stake_index = 0

            stake = self.config.stakes_brl[stake_index]
            win = (this_dir == current_direction)

            # Profit model:
            # - On win: payout equals stake * payout_ratio (configurable via .env).
            # - On loss: we lose the stake.
            profit = (stake * settings.payout_ratio) if win else -stake
            total_profit += profit
            results.append({
                "index": i,
                "entry_direction": current_direction,
                "candle_direction": this_dir,
                "stake_brl": stake,
                "win": win,
                "profit_brl": profit,
            })

            if win:
                # Reset sequence on victory per user rules
                current_direction = None
                stake_index = 0
            else:
                # Loss: advance stake. If maxed out (8 operations), reset afterwards
                stake_index += 1
                if stake_index >= len(self.config.stakes_brl):
                    # Sequence ended with 8 losses; reset stake and start fresh next candle
                    current_direction = None
                    stake_index = 0
                else:
                    # Continue same entry direction until a win or sequence ends
                    pass

        return MartingaleResult(total_profit_brl=total_profit, sequence_results=results)
