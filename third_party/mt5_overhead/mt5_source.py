import MetaTrader5 as mt5
from typing import Callable, TypeVar, ParamSpec
import datetime as dt
from third_party.candlestic.candle import Candle
from operator import itemgetter
from third_party.candlestic.chart import Chart
from third_party.candlestic.symbol import Symbol
from third_party.candlestic.time_frame import TimeFrame
from third_party.mt5_overhead.exception import MetaTraderIOException
from third_party.mt5_overhead.mt5_result import LastErrorResult, Mt5Result, LastTickResult
from third_party.mt5_overhead.ordertype import OrderType
from pandas import DataFrame
P = ParamSpec("P")
T = TypeVar("T")


def mt5_last_error() -> LastErrorResult:
    lasterror = mt5.last_error()
    return LastErrorResult(
        message=lasterror[1],
        result_code=lasterror[0],
    )


def mt5_initialize_docrator(func: Callable[P, Mt5Result[T | None]]) -> Callable[..., Mt5Result[T | None]]:
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
        except MetaTraderIOException as e:
            _last_error = mt5_last_error()
            return Mt5Result(
                has_error=True,
                message=f" mt5 msg :{_last_error.message} , exception : {str(e)}",
                result_code=_last_error.result_code,
                result=None,
            )

    return wrapper


@mt5_initialize_docrator
def get_historical_data(
        symbol: Symbol,
        timeframe: TimeFrame,
        date_from: dt.datetime,
        date_to: dt.datetime,
        date_to_le : bool = False,
        date_from_gt : bool = False,
) -> Mt5Result[Chart | None]:
    if date_to_le:
        date_to = date_to + dt.timedelta(minutes=timeframe.included_m1)

    if date_from_gt:
        date_from = date_to + dt.timedelta(minutes=timeframe.included_m1)

    result = mt5.copy_rates_range(
        symbol.symbol_name,
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
                date_time=dt.datetime.fromtimestamp(timestamp(i), dt.UTC),
            ) for i in result
        ],
        timeframe=timeframe.name
    )

    return Mt5Result(
        has_error=False,
        message=_last_error[0],
        result_code=_last_error[1],
        result=chart,
    )

@mt5_initialize_docrator
def get_last_n_historical_data(
        symbol: Symbol,
        timeframe: TimeFrame,
        n : int,
        as_dataframe : bool = False
) -> Mt5Result[Chart | DataFrame | None]:

    result = mt5.copy_rates_from_pos(
        symbol.symbol_name,
        timeframe.mt5_value,
        0,
        n
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
                date_time=dt.datetime.fromtimestamp(timestamp(i), dt.UTC),
            ) for i in result
        ],
        timeframe=timeframe.name
    )

    return Mt5Result(
        has_error=False,
        message=_last_error[0],
        result_code=_last_error[1],
        result=chart,
    )

@mt5_initialize_docrator
def get_last_n_historical_data_from_date(
        symbol: Symbol,
        timeframe: TimeFrame,
        date_from : dt.datetime,
        n : int,
) -> Mt5Result[Chart | None]:

    result = mt5.copy_rates_from_pos(
        symbol.symbol_name,
        timeframe.mt5_value,
        date_from,
        n
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
                date_time=dt.datetime.fromtimestamp(timestamp(i), dt.UTC),
            ) for i in result
        ],
        timeframe=timeframe.name
    )

    return Mt5Result(
        has_error=False,
        message=_last_error[0],
        result_code=_last_error[1],
        result=chart,
    )


@mt5_initialize_docrator
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


@mt5_initialize_docrator
def set_pending_order(
        order_type: OrderType,
        symbol: Symbol,
        volume: float,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        external_id : str,
) -> Mt5Result[mt5.OrderSendResult]:
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol.symbol_name,
        "volume": volume,
        "type": order_type.mt5_type,
        "price": entry_price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 20,
        "magic": 1000,
        "comment": "from python",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
        "retcode_external": external_id
    }

    order_send_result: mt5.OrderSendResult = mt5.order_send(request)

    if order_send_result.retcode != 10009:
        return Mt5Result(
            has_error=True,
            message=order_send_result.comment,
            result_code=order_send_result.retcode,
            result=order_send_result,
        )

    lasterror = mt5_last_error()
    return Mt5Result(
        has_error=lasterror.result_code != 1,
        message=lasterror.message,
        result_code=lasterror.result_code,
        result=order_send_result,
    )


@mt5_initialize_docrator
def get_account_info() -> Mt5Result[mt5.AccountInfo]:
    info = mt5.account_info()

    lasterror = mt5_last_error()
    return Mt5Result(
        has_error=lasterror.result_code != 1,
        message=lasterror.message,
        result_code=lasterror.result_code,
        result=info,
    )


@mt5_initialize_docrator
def get_orders() -> Mt5Result[list[mt5.TradeOrder]]:
    orders = mt5.orders_get()

    lasterror = mt5_last_error()

    orders= list(orders)

    return Mt5Result(
        has_error= lasterror.result_code != 1,
        result_code=lasterror.result_code,
        message=lasterror.message,
        result= orders
    )



@mt5_initialize_docrator
def get_positions() -> Mt5Result[list[mt5.TradePosition]]:
    positions = mt5.positions_get()

    lasterror = mt5_last_error()

    positions = list(positions)

    return Mt5Result(
        has_error= lasterror.result_code != 1,
        result_code=lasterror.result_code,
        message=lasterror.message,
        result= positions
    )


@mt5_initialize_docrator
def get_deals_history(
        from_date : dt.datetime = dt.datetime.now(dt.UTC) - dt.timedelta(days=365),
        to_date : dt.datetime = dt.datetime.now(dt.UTC) + dt.timedelta(days=1)
) -> Mt5Result[list[mt5.TradeDeal]]:

    deals = mt5.history_deals_get( from_date, to_date)

    lasterror = mt5_last_error()

    return Mt5Result(
        has_error= lasterror.result_code != 1,
        result_code= lasterror.result_code,
        message=lasterror.message,
        result=list(deals)
    )


@mt5_initialize_docrator
def get_orders_history() -> Mt5Result[list[mt5.TradeOrder]]:
    from_date = dt.datetime(2020, 1, 1)
    to_date = dt.datetime(2030, 1, 1)

    orders = mt5.history_orders_get(from_date, to_date)

    lasterror = mt5_last_error()

    return Mt5Result(
        has_error=lasterror.result_code != 1,
        result_code=lasterror.result_code,
        message=lasterror.message,
        result=list(orders)
    )


print()