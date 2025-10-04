from typing import runtime_checkable
from typing import Protocol
@runtime_checkable
class StrategyProtocol(Protocol):

    def initialize(self,*args, **kwargs):...

    def next(self,data): ...

@runtime_checkable
class RiskManagerProtocol(Protocol):
    def calculate_size(self,*args)->float:...
