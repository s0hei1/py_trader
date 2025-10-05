


class StaticRiskManager:

    def __init__(self,balance : float, risk_size : float):
        if not 0 < risk_size <= 100:
            raise ValueError(f"The risk size must be between 0 and 100, {risk_size} is ut of range")

        self.risk_size = risk_size
        self.balance = balance
    def calculate_size(self, entry_price : float, stop_loss_price : float) -> tuple[float, float]:
        risk_per_unit = self.balance * (self.risk_size / 100)
        units = abs(entry_price - stop_loss_price)
        base_currency_vol = risk_per_unit / units
        quote_currency_vol = base_currency_vol * entry_price

        return base_currency_vol, quote_currency_vol

