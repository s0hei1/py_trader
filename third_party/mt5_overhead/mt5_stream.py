import asyncio
from more_itertools import last
from third_party.candlestic import Symbol, TimeFrame
import datetime as dt
from third_party.mt5_overhead.exception import MetaTraderStreamingException
from third_party.mt5_overhead.mt5_source import _mt5_initialize, mt5_last_error
import MetaTrader5 as mt5


async def stream_chart_data(
        symbol : Symbol,
        timeframe : TimeFrame,
        date_from : dt.datetime
):
    init_result = mt5.initialize()

    if not init_result:
        lasterror = mt5_last_error()
        raise MetaTraderStreamingException(message=lasterror.message,code=lasterror.result_code)

    data = mt5.copy_rates_range(
        symbol.symbol_name,
        timeframe.mt5_value,
        date_from,
        dt.datetime.now(dt.UTC),
    )

    last_error = mt5_last_error()
    if last_error.has_error:
        raise MetaTraderStreamingException(message=last_error.message,code=last_error.result_code)

    yield data

    get_current_minute = lambda: dt.datetime.now(dt.UTC).minute
    while True:
        await asyncio.sleep(1)

        current_minute = get_current_minute()
        if current_minute == get_current_minute():
            continue

        last_row = last(data)

        dt.datetime.fromtimestamp(last_row[0], dt.UTC)

        data = mt5.copy_rates_range(
            symbol.symbol_name,
            timeframe.mt5_value,
            date_from,
            dt.datetime.now(dt.UTC),
        )

        yield data





