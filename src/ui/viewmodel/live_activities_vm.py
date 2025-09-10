import asyncio
from typing import AsyncGenerator
from third_party.mt5_overhead import mt5_source
import MetaTrader5 as mt5

class LiveActivitiesVM():

    _account_info : mt5.AccountInfo | None
    _positions : list
    _orders : list

    @property
    def account_info(self):
        return self._account_info

    def __init__(self):
        info = mt5_source.get_account_info()
        if not info.has_error:
            self._account_info = info.result
            print(info.result)

    # async def value_stream(self) -> None:
    #     while True:
    #         await asyncio.sleep(5)
    #         info: mt5.AccountInfo = mt5_source.get_account_info().result
    #         self._account_info =