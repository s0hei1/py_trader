from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

T = TypeVar('T')

@dataclass
class LastErrorResult:
    message : str
    result_code : int

    @property
    def has_error(self) -> bool:
        return self.result_code != 1

@dataclass
class Mt5Result(Generic[T]):
    has_error : bool
    message : str
    result_code : int
    result : T | None

@dataclass
class LastTickResult():
    bid : float
    ask : float

