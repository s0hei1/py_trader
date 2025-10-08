import asyncio
from typing import Iterator

import numpy as np
from more_itertools import last
from numpy._typing import NDArray
from sqlalchemy.sql.functions import concat

from third_party.candlestic import Symbol, TimeFrame, Chart
import datetime as dt

from third_party.mt5_overhead.tools import get_last_tick_datetime
from third_party.mt5_overhead.mt5_source import mt5_initialize_decor, mt5_last_error
import MetaTrader5._core as mt5


@mt5_initialize_decor
async def stream_chart_data(
        symbol: Symbol,
        timeframe: TimeFrame,
        date_from: dt.datetime,
        as_chart: bool = False
) -> Iterator[Chart] | Iterator[NDArray[tuple]] | None:
    data = mt5.copy_rates_from_pos(
        symbol.symbol_fullname,
        timeframe.mt5_value,
        1,
        100,
    )

    print(data)


    yield Chart.from_mt5_data(data, timeframe) if as_chart else data

    get_current_minute = lambda: dt.datetime.now(dt.UTC).minute
    current_minute = get_current_minute()
    while True:

        await asyncio.sleep(1)
        if current_minute == get_current_minute():
            continue
        current_minute = get_current_minute()

        last_row = last(data)

        data = mt5.copy_rates_range(
            symbol.symbol_fullname,
            timeframe.mt5_value,
            dt.datetime.fromtimestamp(last_row[0]),
            get_last_tick_datetime() + dt.timedelta(minutes=timeframe.included_m1),
        )
        new_data = data
        if new_data.size == 0:
            continue

        print('new_data is:' ,new_data)

        yield Chart.from_mt5_data(new_data, timeframe) if as_chart else data


