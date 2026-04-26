from dataclasses import dataclass
from typing import Literal,Callable

LineType = Literal['PRICE', 'MA', 'TRUE_RANGE']

@dataclass
class Line:
    id : int
    name : str
    line_type : LineType
    function : Callable | None
