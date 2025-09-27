import talib
from third_party.auto_trader.strategy import BaseStrategy
import pandas as pd
from third_party.auto_trader.trade_signal import TradeSignal
from third_party.mt5_overhead.ordertype import OrderType, OrderTypes



class SimpleMAStrategy(BaseStrategy):


    def check_signal(self, chart: pd.DataFrame) -> TradeSignal | None:

        chart['ma20'] = talib.MA(chart['close'], timeperiod=21)
        chart['atr21'] = values = talib.ATR(
            chart['high'],
            chart['low'],
            chart['close'],
            timeperiod=24
        )

        def set_close_status(row):
            print(type(row))
            if row['close'] > row['ma20']:
                return 'upper'
            if row['close'] < row['ma20']:
                return 'under'

            return 'eq'

        chart['close_status'] = chart.apply(set_close_status, axis=1)

        if chart.at[chart.index[-2], 'close_status'] != chart.at[chart.index[-1], 'close_status']:
            current_status = chart.at[chart.index[-1], 'close_status']

            entry_price = chart.at[chart.index[-1], 'close']
            atr = chart.at[chart.index[-1], 'atr21']
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
