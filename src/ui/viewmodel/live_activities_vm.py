import asyncio
from typing import AsyncGenerator
from third_party.mt5_overhead import mt5_source
import MetaTrader5 as mt5
import pandas as pd


class LiveActivitiesVM():
    _account_info: mt5.AccountInfo | None
    _orders: list[mt5.TradeOrder] | None
    _positions: list[mt5.TradePosition] | None

    @property
    def account_info(self):
        return self._account_info

    @property
    def orders(self):
        return self._orders

    @property
    def positions(self):
        return self._positions

    def __init__(self):
        self.fetch_data_from_mt5()

    def fetch_data_from_mt5(self) -> None:
        info = mt5_source.get_account_info()
        orders = mt5_source.get_orders()
        positions = mt5_source.get_positions()

        print(orders.result)

        self._account_info = info.result if not info.has_error else None
        self._orders = orders.result if not orders.has_error else None
        self._positions = positions.result if not positions.has_error else None

    def get_orders_df(self):
        return pd.DataFrame(
            [
                (i.symbol, i.time_setup, round(i.price_open, 5), round(i.sl, 5), round(i.tp, 5), i.volume_initial,
                 i.volume_current)
                for i in self._orders
            ],
            columns=("Symbol", "Time setup", "Price open", "Stop loss", "Take profit", "Volume init", "Volume Current")
        )

    def get_positions_df(self):
        return pd.DataFrame(
            [
                (
                    i.symbol, i.time_setup,
                    round(i.price_open, 5), round(i.sl, 5), round(i.tp, 5), i.profit,
                    i.volume_initial,i.volume_current
                )
                for i in self._positions
            ],
            columns=(
            "Symbol", "Time setup", "Price open", "Stop loss", "Take profit", "Profit", "Volume init", "Volume Current")
        )
