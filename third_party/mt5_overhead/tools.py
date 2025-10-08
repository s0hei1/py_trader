import MetaTrader5._core as mt5
from toolz.curried import pipe, filter, map
import datetime as dt
from third_party.mt5_overhead.mt5_source import mt5_initialize_decor


def get_last_tick_datetime(symbol_name : str | None = None, as_timestamp : bool = False) -> dt.datetime | int:

    mt5.initialize()

    if symbol_name is None:
        symbols = mt5.symbols_get()

        if symbols is None or symbols == []:
            raise RuntimeError("There is no active trading symbol, please ad a symbol to your watch list")

        symbol_name = pipe(
            symbols,
            filter(lambda it: it.select),
            map(lambda it: it.name),
            next,
        )

    symbol_info_tick = mt5.symbol_info_tick(symbol_name)

    if symbol_info_tick is None:
        raise RuntimeError("There is a runtime error")

    server_now_tamp = symbol_info_tick.time

    if as_timestamp:
        return server_now_tamp

    return dt.datetime.fromtimestamp(server_now_tamp)

print(get_last_tick_datetime())
