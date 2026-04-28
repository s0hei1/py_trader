from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    url : str
    method : str
