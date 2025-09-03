from dataclasses import dataclass
from datetime import datetime


@dataclass
class Volume:
    volume: float
    date: datetime