import pandas as pd
import talib
from third_party.auto_trader.models import TradeSignal
from third_party.candlestic import Chart
from third_party.mt5_overhead import OrderTypes


class SimpleMACrossStrategy:
    chart_data: pd.DataFrame | None = None

    def __init__(self, ma_time_period : int = 24, atr_time_period : int = 24):
        self.ma_time_period = ma_time_period
        self.atr_time_period = atr_time_period

    @property
    def settings(self) -> dict:
        return {
            'atr' : self.atr_time_period,
            'ma' : self.ma_time_period
        }

    def initialize(self, chart_data: Chart) -> None:
        self.chart_data = chart_data.to_dataframe()

    @property
    def is_initialized(self) -> bool:
        return self.chart_data is not None

    def transform_data(self):
        self.chart_data['atr'] = talib.ATR(
            high=self.chart_data['high'],
            low=self.chart_data['low'],
            close=self.chart_data['close'],
            timeperiod=self.atr_time_period
        )
        self.chart_data['ma'] = talib.MA(
            real=self.chart_data['close'],
            timeperiod=self.ma_time_period
        )

        def set_ma_status(row):
            if row['close'] > row['ma']:
                return 'upper'
            if row['close'] < row['ma']:
                return 'under'
            return 'eq'

        self.chart_data['ma_status'] = self.chart_data.apply(set_ma_status, axis=1)

    def clean_memory(self):
        if len(self.chart_data) < 500:
            return

        self.chart_data = self.chart_data.iloc[-500:-1].reset_index(drop=True)

    def next(self, data: Chart) -> TradeSignal | None:
        self.chart_data = pd.concat([self.chart_data, data], ignore_index=True)
        self.transform_data()
        self.clean_memory()

        last_ma_status = self.chart_data.iloc[-1]['ma_status']
        pre_last_ma_status = self.chart_data.iloc[-2]['ma_status']

        if last_ma_status == pre_last_ma_status:
            return None

        order_type = OrderTypes.buy_limit if last_ma_status == 'upper' else OrderTypes.sell_limit

        last_close = self.chart_data.iloc[-1]['close']
        last_atr = self.chart_data.iloc[-1]['atr']
        stop_loss_units = last_atr * 2.4
        tp_units = last_atr*4.8

        stop_loss = last_close - stop_loss_units if order_type.base_type == "BUY" else last_close + stop_loss_units
        take_profit = last_close + tp_units if order_type.base_type == "BUY" else last_close - tp_units

        return TradeSignal(
            order_type=order_type,
            entry_price= self.chart_data.iloc[-1]['close'],
            stop_loss_price= stop_loss,
            take_profit_price= take_profit
        )
