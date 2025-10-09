import asyncio
from typing import Iterator

import numpy as np
from more_itertools import last
from numpy._typing import NDArray
from third_party.candlestic import Symbol, TimeFrame, Chart
import datetime as dt
from third_party.mt5_overhead.tools import get_last_tick_datetime
from third_party.mt5_overhead.mt5_source import mt5_initialize_decor
import MetaTrader5._core as mt5
import pipe

@mt5_initialize_decor
async def stream_chart_data(
        symbol: Symbol,
        timeframe: TimeFrame,
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


    while True:

        await asyncio.sleep(5)

        last_row = last(data)
        last_time = last_row[0]

        data = mt5.copy_rates_from_pos(
            symbol.symbol_fullname,
            timeframe.mt5_value,
            1,
            5,
        )

        new_data = np.array([i for i in data if i[0] > last_time])

        if new_data.size == 0:
            continue

        print('new_data is:' ,new_data)

        yield Chart.from_mt5_data(new_data, timeframe) if as_chart else data


