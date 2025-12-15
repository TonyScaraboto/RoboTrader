from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterable, Dict

class CSVLogger:
    def __init__(self, file_path: str | Path) -> None:
        self.path = Path(file_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write_rows(self, rows: Iterable[Dict]) -> None:
        rows = list(rows)
        if not rows:
            return
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
