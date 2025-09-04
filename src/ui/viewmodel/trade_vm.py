from third_party.mt5_overhead import set_pending_order

class TradeVM():
    _risk_percentage: float = 1
    _balance: float = 1000
    _currency: str
    _time_frame: str
    _entry_price: float
    _sl: float
    _tp: float

    @property
    def balance(self): return self._balance

    @property
    def risk_percentage(self): return self._risk_percentage

    @property
    def currency(self): return self._currency

    @property
    def time_frame(self): return self._time_frame

    @property
    def entry_price(self): return self._entry_price

    @property
    def sl(self): return self._sl

    @property
    def tp(self): return self._tp

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

    def set_sl(self, new_value: str | float):
        self._sl = float(new_value)

    def set_tp(self, new_value: str | float):
        self._tp = float(new_value)

    def calculate_volume(self):
        risk_amount = self.balance * (self.risk_percentage / 100)

        if self.currency == "EURUSD":
            pip_value_per_lot = 10
        else:
            raise ValueError("This function currently only supports EURUSD.")

        lot_size = risk_amount / (self.sl * pip_value_per_lot)

        return round(lot_size, 2)

    def set_order(self):
        set_pending_order(

        )


