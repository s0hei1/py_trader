from dataclasses import dataclass

@dataclass(frozen=True)
class TimeFrame:
    name : str
    mt5_value : int
    included_m1 : int
