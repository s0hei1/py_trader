from typing import Literal, TypeAlias
import talib
from third_party.auto_trader.strategy import BaseStrategy
import pandas as pd
from third_party.auto_trader.trade_signal import TradeSignal
from third_party.candlestic import Chart
from third_party.candlestic.indicator import Indicator
from third_party.mt5_overhead.ordertype import OrderType, OrderTypes

CloseStatus: TypeAlias = Literal['upper_ma', 'under_ma']


class SimpleMAStrategy(BaseStrategy):
    price_close_location: CloseStatus

    def __init__(self, chart: Chart):
        self.chart = chart

        opens, closes, highs, lows, times = chart.separate_ochl(to_ndarray=True)

        ma_indicator = Indicator(
            name="ma20",
            values=
        )

        atr_indicator = Indicator(
            name="atr21",

        )

    def check_signal(self, df: pd.DataFrame) -> TradeSignal | None:

        df['ma20'] = talib.MA(df['close'], timeperiod=21)
        df['atr21'] = values = talib.ATR(
            df['high'],
            df['low'],
            df['close'],
            timeperiod=24
        )

        def set_close_status(row):
            print(type(row))
            if row['close'] > row['ma20']:
                return 'upper'
            if row['close'] < row['ma20']:
                return 'under'

            return 'eq'

        df['close_status'] = df.apply(set_close_status, axis=1)

        if df.at[df.index[-2], 'close_status'] != df.at[df.index[-1], 'close_status']:
            current_status = df.at[df.index[-1], 'close_status']

            entry_price = df.at[df.index[-1], 'close']
            atr = df.at[df.index[-1], 'atr21']
            order_type: OrderType | None = None
            stop_loss: float | None = None
            take_profit: float | None = None

            if current_status == 'eq':
                return None

            if current_status == 'upper':
                order_type = OrderTypes.buy_limit.value
                stop_loss = entry_price - atr
                take_profit = entry_price + atr

            if current_status == 'under':
                order_type = OrderTypes.sell_limit.value
                stop_loss = entry_price + atr
                take_profit = entry_price - atr

            return TradeSignal(
                order_type=order_type,
                entry_price=entry_price,
                stop_loss_price=stop_loss,
                take_profit_price=take_profit,
            )

        return None
