from src.data.core.models import Pattern, PlaceOrder
from src.data.repo.pattern_repo import PatternRepo
from src.tools.di.container import Container
from src.ui.viewmodel.vm_result import VMResult
from third_party.candlestic import TimeFrame
from third_party.candlestic.defaults import DefaultSymbols, ClassicFractalTimeFrames
from third_party.mt5_overhead import set_pending_order,get_last_n_historical_data
from third_party.mt5_overhead import OrderTypes
from third_party.mt5_overhead.mt5_result import Mt5Result
import MetaTrader5 as mt5
from datetime import date,time,datetime
import pandas as pd
import talib


class PatternTradingVM:
    _risk_percentage: float = 1
    _balance: float = 1000
    _currency: str
    _time_frame: str
    _entry_price: float = 0.0
    _sl: int = 0
    _tp: int = 0
    _order_type: str

    _ATRs : dict[str, int] = {}
    _pattern_time_frame: str
    _pattern_symbol: str
    _pattern_start_date: date
    _pattern_end_date: date
    _pattern_start_time: time
    _pattern_end_time: time

    _patterns_df : pd.DataFrame
    _selected_pattern : int | None = None

    def __init__(self,
                 pattern_repo: PatternRepo = Container.pattern_repo(),
                 place_order_repo = Container.place_order_repo()):
        self.pattern_repo = pattern_repo
        self._set_patterns_df()
        self.place_order_repo = place_order_repo

        self._set_atr()

    @property
    def balance(self):
        return self._balance

    @property
    def risk_percentage(self):
        return self._risk_percentage

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def time_frame(self):
        return self._time_frame

    @property
    def entry_price(self):
        return self._entry_price

    @property
    def sl(self):
        return self._sl

    @property
    def tp(self):
        return self._tp

    @property
    def order_type(self):
        return self._order_type

    @property
    def pattern_time_frame(self):
        return self._pattern_time_frame

    @property
    def pattern_symbol(self):
        return self._pattern_symbol

    @property
    def pattern_start_date(self):
        return self._pattern_start_date

    @property
    def pattern_end_date(self):
        return self._pattern_end_date

    @property
    def pattern_start_time(self):
        return self._pattern_start_time

    @property
    def pattern_end_time(self):
        return self._pattern_end_time

    @property
    def patterns_df(self):
        return self._patterns_df

    @property
    def selected_pattern(self):
        return self._selected_pattern

    @property
    def ATRs(self):
        return self._ATRs

    def set_risk_percentage(self, new_value: str | float):
        self._risk_percentage = float(new_value)

    def set_balance(self, new_value: str | float):
        self._balance = float(new_value)

    def set_currency(self, new_value: str):
        self._currency = new_value

    def set_time_frame(self, new_value: str):
        self._time_frame = new_value

    def set_entry_price(self, new_value: str | float):
        self._entry_price = float(new_value)

    def set_sl(self, new_value: str):
        self._sl = int(new_value)

    def set_tp(self, new_value: str):
        self._tp = int(new_value)

    def set_order_type(self, new_value: str):
        self._order_type = new_value

    def set_pattern_time_frame(self, new_value: str):
        self._pattern_time_frame = new_value

    def set_pattern_symbol(self, new_value: str):
        self._pattern_symbol = new_value

    def set_pattern_start_date(self, new_value : date):
        print("start date is ", new_value)
        self._pattern_start_date = new_value

    def set_pattern_end_date(self, new_value : date):
        self._pattern_end_date = new_value

    def set_pattern_start_time(self, new_value : time):
        self._pattern_start_time = new_value

    def set_pattern_end_time(self, new_value : time):
        self._pattern_end_time = new_value

    def set_selected_pattern(self, selected_pattern_id: int | None):
        self._selected_pattern = int(selected_pattern_id) if selected_pattern_id is not None else None

    def _set_atr(self):
        for time_frame in ClassicFractalTimeFrames.get_time_frames():

            symbol = DefaultSymbols.eur_usd
            result = get_last_n_historical_data(
                symbol = symbol,
                timeframe = time_frame,
                n = time_frame.fractal_value +1
            )

            if result.has_error:
                continue


            opens, closes, highs, lows, times = result.result.separate_ochl(to_ndarray=True)

            atr_array = talib.ATR(
                highs,
                lows,
                closes,
                timeperiod = time_frame.fractal_value
            )
            atr = float(atr_array[-1])
            self._ATRs[time_frame.name] = symbol.price_dif_to_pips(atr)

    def calculate_volume(self):
        risk_amount = self.balance * (self.risk_percentage / 100)

        if self.currency == "EURUSD":
            pip_value_per_lot = 10
        else:
            raise ValueError("This function currently only supports EURUSD.")

        lot_size = risk_amount / (self.sl * pip_value_per_lot)

        return round(lot_size, 2)

    def _set_patterns_df(self):
        self._patterns_df = self.pattern_repo.get_patterns_df()

    def set_order(self) -> Mt5Result[mt5.OrderSendResult]:

        if self.selected_pattern is None:
            raise Exception("select a pattern For Trading !")

        lot_size = self.calculate_volume()
        symbol = DefaultSymbols.get_symbol_by_name(self.currency)

        order_type = OrderTypes.get_type_by_name(self.order_type)

        sl_value = self.sl * symbol.decimal_places_value
        tp_value = self.sl * symbol.decimal_places_value

        sl_price = self.entry_price - sl_value if order_type.is_buy() else self.entry_price + sl_value
        tp_price = self.entry_price + tp_value if order_type.is_buy() else self.entry_price - tp_value

        sl_price = round(sl_price, 5)
        tp_price = round(tp_price, 5)



        place_order = PlaceOrder()
        generated_order_code = self.place_order_repo.generate_place_order_code()

        result = set_pending_order(
            order_type=order_type,
            symbol=symbol,
            volume=lot_size,
            entry_price=self.entry_price,
            stop_loss=sl_price,
            take_profit=tp_price,
            external_id = generated_order_code
        )
        print(result)
        place_order.order_code = generated_order_code
        place_order.pattern_id = self.selected_pattern
        place_order.order_ticket = int(result.result.order)

        self.place_order_repo.create(place_order)

        return result

    def get_order_types(self) -> list[str]:
        return OrderTypes.get_type_names()

    def get_symbols(self) -> list[str]:
        return DefaultSymbols.get_symbols_name()

    def get_time_frames(self) -> list[str]:
        return ClassicFractalTimeFrames.get_time_frame_names()

    def add_pattern(self) -> VMResult:
        try:
            pattern = self.pattern_repo.create(
                Pattern(
                    pattern_start_date_time= datetime.combine(self._pattern_start_date, self._pattern_end_time),
                    pattern_end_date_time= datetime.combine(self._pattern_end_date, self._pattern_end_time),
                    pattern_time_frame= self._pattern_time_frame,
                    symbol_name= self._pattern_symbol,
                )
            )
            if pattern is not None:
                self._set_patterns_df()
                return VMResult(message=f"Pattern Added Successful \n{pattern.__dict__}")
            else:
                raise Exception("an exception occured while pattern adding")
        except Exception as e:
            return VMResult(has_error=True, message=str(e))

