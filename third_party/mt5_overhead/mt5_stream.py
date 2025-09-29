import asyncio
from typing import Iterator
from more_itertools import last
from numpy._typing import NDArray

from third_party.candlestic import Symbol, TimeFrame, Chart
import datetime as dt
from third_party.mt5_overhead.mt5_source import mt5_initialize_docrator, mt5_last_error
import MetaTrader5 as mt5


@mt5_initialize_docrator
async def stream_chart_data(
        symbol: Symbol,
        timeframe: TimeFrame,
        date_from: dt.datetime,
        as_chart: bool = False
) -> Iterator[Chart] | Iterator[NDArray[tuple]]:
    data = mt5.copy_rates_range(
        symbol.symbol_name,
        timeframe.mt5_value,
        date_from,
        dt.datetime.now(dt.UTC),
    )


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
            symbol.symbol_name,
            timeframe.mt5_value,
            dt.datetime.fromtimestamp(last_row[0], dt.UTC),
            dt.datetime.now(dt.UTC),
        )
        data = data[1:]

        yield Chart.from_mt5_data(data, timeframe) if as_chart else data


