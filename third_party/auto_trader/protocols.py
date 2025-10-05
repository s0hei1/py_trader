from typing import runtime_checkable
from typing import Protocol

from third_party.auto_trader.models import TradeSignal


@runtime_checkable
class StrategyProtocol(Protocol):

    def initialize(self,*args, **kwargs):...

    def next(self,data) -> TradeSignal | None: ...

@runtime_checkable
class RiskManagerProtocol(Protocol):
    def calculate_size(self,*args)->float:...
