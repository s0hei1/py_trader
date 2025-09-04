import MetaTrader5 as mt5
from typing import Callable, TypeVar, ParamSpec
from functools import wraps
import datetime as dt
from third_party.candlestic.candle import Candle
from operator import itemgetter
from third_party.candlestic.chart import Chart
from third_party.candlestic.symbol import Symbol
from third_party.candlestic.time_frame import TimeFrame
from third_party.mt5_overhead.exception import MetaTraderIOException
from third_party.mt5_overhead.mt5_result import LastErrorResult, Mt5Result, LastTickResult
from third_party.mt5_overhead.mt5_rquest import ActionEnum, Action

P = ParamSpec("P")
T = TypeVar("T")


def mt5_last_error() -> LastErrorResult:
    lasterror = mt5.last_error()
    return LastErrorResult(
        message=lasterror[1],
        result_code=lasterror[0]
    )


def _mt5_initialize(func: Callable[P, Mt5Result[T | None]]) -> Callable[P, Mt5Result[T | None]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Mt5Result[T | None]:
        init_result = mt5.initialize()
        if not init_result:
            _last_error = mt5_last_error()
            return Mt5Result(
                has_error=True,
                message=_last_error.message,
                result_code=_last_error.result_code,
                result=None,
            )

        try:
            return func(*args, **kwargs)
        except MetaTraderIOException:
            _last_error = mt5_last_error()
            return Mt5Result(
                has_error=True,
                message=_last_error.message,
                result_code=_last_error.result_code,
                result=None,
            )

    return wrapper


@_mt5_initialize
def get_market_historical_data(
        symbol: Symbol,
        timeframe: TimeFrame,
        date_from: dt.datetime,
        date_to: dt.datetime,
) -> Mt5Result[Chart | None]:
    result = mt5.copy_rates_range(
        symbol.symbol_fullname,
        timeframe.mt5_value,
        date_from,
        date_to,
    )
    _last_error = mt5.last_error()
    if result is None and mt5.last_error()[0] != 1:
        raise MetaTraderIOException(message=_last_error[1], code=_last_error[0], )

    o = itemgetter(1)
    h = itemgetter(2)
    l = itemgetter(3)
    c = itemgetter(4)
    timestamp = itemgetter(0)

    chart = Chart(
        candles=[
            Candle(
                open=o(i),
                high=h(i),
                low=l(i),
                close=c(i),
                datetime=dt.datetime.fromtimestamp(timestamp(i), dt.UTC),
            ) for i in result
        ],
        time_frame=timeframe.name
    )

    return Mt5Result(
        has_error=False,
        message=_last_error[0],
        result_code=_last_error[1],
        result=chart,
    )


@_mt5_initialize
def get_symbol_current_price(symbol: Symbol) -> Mt5Result[float]:
    result = mt5.symbol_info_tick(symbol.symbol_fullname)
    _last_error = mt5_last_error()

    bid = itemgetter(1)
    ask = itemgetter(2)

    last_tick_result = LastTickResult(
        bid=bid(result),
        ask=ask(result)
    )

    return Mt5Result(
        has_error=False,
        message=_last_error.message,
        result_code=_last_error.result_code,
        result=last_tick_result
    )


@_mt5_initialize
def set_pending_order(
        action : Action,
        symbol: Symbol,
        volume : float,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
) -> Mt5Result[tuple]:

    request : mt5.TradeRequest = mt5.TradeRequest(
        action = mt5.TRADE_ACTION_PENDING,
        symbol = symbol.symbol_fullname,
        volume = volume,
        type = action.mt5_type,
        price = entry_price,
        sl = stop_loss,
        tp = take_profit,
        devition = 10,
        magic = 1000,
        type_time = mt5.ORDER_TIME_GTC,
        type_filling = mt5.ORDER_FILLING_RETURN
    )


    trade_request_result = mt5.order_send(request,)

    lasterror = mt5_last_error()
    return Mt5Result(
        has_error=lasterror.result_code == 1,
        message = lasterror.message,
        result_code = lasterror.result_code,
        result = trade_request_result,
    )
