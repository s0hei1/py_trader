import talib
from numpy._typing import NDArray

from third_party.auto_trader.strategy import BaseStrategy
import pandas as pd
from third_party.auto_trader.trade_signal import TradeSignal
from third_party.candlestic import Chart
from third_party.mt5_overhead.ordertype import OrderType, OrderTypes


class StrategyProtocol:

    def init_history(self,*args, **kwargs):...

    def check_signal(self,data): ...

class SimpleMAStrategy:

    candles_df : pd.DataFrame | None = None

    async def setup(self, data : Chart):
        if self.candles_df is None:
            self.candles_df = data.to_dataframe()
        # else:
        #     await self.next(data.to_dataframe())

    async def next(self, data : pd.DataFrame):
        self.candles_df = pd.concat(
            [self.candles_df,
            data]
        )
        print(self.candles_df)

