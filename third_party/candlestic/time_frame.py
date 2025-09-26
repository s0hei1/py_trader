from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TimeFrame:
    name: str
    mt5_value: int
    included_m1: int
    fractal_value: int | None = None
