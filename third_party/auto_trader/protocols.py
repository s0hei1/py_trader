from typing import runtime_checkable
from typing import Protocol

from third_party.auto_trader.models import TradeSignal
from third_party.candlestic import Chart


@runtime_checkable
class StrategyProtocol(Protocol):

    def initialize(self,*args, **kwargs) -> None:...

    def next(self, data: Chart) -> TradeSignal | None: ...

    @property
    def is_initialized(self) -> bool: ...

@runtime_checkable
class RiskManagerProtocol(Protocol):
    def calculate_size(self,*args)->float:...
