import talib
from numpy._typing import NDArray

from third_party.auto_trader.strategy import BaseStrategy
import pandas as pd
from third_party.auto_trader.trade_signal import TradeSignal
from third_party.candlestic import Chart
from third_party.mt5_overhead.ordertype import OrderType, OrderTypes


class StrategyProtocol:

    def init_history(self, *args, **kwargs): ...

    def check_signal(self, data): ...


class SimpleMAStrategy:
    candles_df: pd.DataFrame | None = None

    async def setup(self, data: Chart):
        if self.candles_df is None:
            self.candles_df = await self.trasnform(data.to_dataframe())
        else:
            self.candles_df = pd.concat([
                self.candles_df,
                data.to_dataframe()
            ])
            self.candles_df = await self.trasnform(self.candles_df)
            self.candles_df = await self.clean_memory(self.candles_df)
            await self.next(self.candles_df)

    async def clean_memory(self, df: pd.DataFrame):
        if len(df) < 500:
            return

        df = df.iloc[-500:-1]
        return df

    async def trasnform(self, df: pd.DataFrame):

        df['atr'] = talib.ATR(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            timeperiod=21
        )
        df['ma'] = talib.MA(
            real=df['close'],
            timeperiod=21
        )

        def set_ma_status(row):
            if row['close'] > row['ma']:
                return 'upper'
            if row['close'] < row['ma']:
                return 'under'
            return 'eq'

        df['ma_status'] = df.apply(set_ma_status, axis=1)

        return df

    async def next(self, data: pd.DataFrame):

        last_ma_status = data.iloc[-1]['ma_status']
        pre_last_ma_status = data.iloc[-2]['ma_status']

        if last_ma_status == pre_last_ma_status:
            return None




        return TradeSignal(
            order_type: ,
            entry_price:,
            stop_loss_price:,
            take_profit_price:,
        )
