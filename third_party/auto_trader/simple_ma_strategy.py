from typing import runtime_checkable
import talib
import pandas as pd
from third_party.candlestic import Chart

@runtime_checkable
class StrategyProtocol:

    def initialize(self,*args, **kwargs):...

    def next(self,data): ...

@runtime_checkable
class RiskManagerProtocol(StrategyProtocol):
    def calculate_size(self,*args)->float:...

class SimpleMAStrategy:

    candles_df : pd.DataFrame | None = None

    async def setup(self, data : Chart):
        if self.candles_df is None:
            await self.initialize(data)
        else:
            await self.next(data.to_dataframe())

    async def _calculate_indicators(self):

        atr = talib.ATR(
            self.candles_df['high'],
            self.candles_df['low'],
            self.candles_df['close'],
            timeperiod = 24
        )

        ma = talib.MA(
            self.candles_df['close'],
            timeperiod=20
        )

        self.candles_df['atr'] = atr
        self.candles_df['ma'] = ma


    async def initialize(self, data : Chart):
        self.candles_df = data.to_dataframe()
        await self._calculate_indicators()


    async def next(self, data : Chart):

        self.candles_df = pd.concat(
            [self.candles_df,
            data],
            ignore_index=True
        )
        await self._calculate_indicators()
