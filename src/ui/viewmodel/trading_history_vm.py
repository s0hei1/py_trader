from third_party import mt5_overhead as mt5_source
import MetaTrader5 as mt5
import pandas as pd

class TradingHistoryVM():

    _orders_history : list[mt5.TradeOrder]
    _deals_history : pd.DataFrame

    def __init__(self):

        deals_history_result = mt5_source.get_deals_history()
        if not deals_history_result.has_error:
            deals_history = [i._asdict() for i in deals_history_result.result]

            self._set_deals_history(pd.DataFrame(deals_history))

    def _set_orders_history(self):
        orders_history = mt5_source.get_orders_history()
        self._orders_history = [] if orders_history.has_error else orders_history.result

    def _set_deals_history(self, value : pd.DataFrame):
        self._deals_history = value

    @property
    def orders_history(self):
        return self._orders_history

    @property
    def deals_history(self):
        return self._deals_history