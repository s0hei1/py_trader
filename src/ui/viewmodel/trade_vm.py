from third_party.candlestic.enums import Symbols, TimeFrames
from third_party.mt5_overhead import set_pending_order
from third_party.mt5_overhead import OrderTypes
from third_party.mt5_overhead.mt5_result import Mt5Result
import MetaTrader5 as mt5

class TradeVM:
    _risk_percentage: float = 1
    _balance: float = 1000
    _currency: str
    _time_frame: str
    _entry_price: float = 0.0
    _sl: int = 0
    _tp: int = 0
    _order_type: str

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

    def calculate_volume(self):
        risk_amount = self.balance * (self.risk_percentage / 100)

        if self.currency == "EURUSD":
            pip_value_per_lot = 10
        else:
            raise ValueError("This function currently only supports EURUSD.")

        lot_size = risk_amount / (self.sl * pip_value_per_lot)

        return round(lot_size, 2)

    def set_order(self) -> Mt5Result[mt5.OrderSendResult]:
        lot_size = self.calculate_volume()
        symbol = Symbols.get_symbol_by_name(self.currency)

        order_type = OrderTypes.get_type_by_name(self.order_type)

        sl_value = self.sl * symbol.decimal_places
        tp_value = self.sl * symbol.decimal_places

        sl_price = self.entry_price - sl_value if order_type.is_buy() else self.entry_price + sl_value
        tp_price = self.entry_price + tp_value if order_type.is_buy() else self.entry_price - tp_value

        sl_price = round(sl_price,5)
        tp_price = round(tp_price,5)

        result = set_pending_order(
            order_type=order_type,
            symbol=symbol,
            volume=lot_size,
            entry_price=self.entry_price,
            stop_loss=sl_price,
            take_profit=tp_price,
        )

        return result

    def get_order_types(self) -> list[str]:
        return OrderTypes.get_type_names()

    def get_symbols(self) -> list[str]:
        return Symbols.get_symbols_name()

    def get_time_frames(self) -> list[str]:
        return TimeFrames.get_time_frame_names()
