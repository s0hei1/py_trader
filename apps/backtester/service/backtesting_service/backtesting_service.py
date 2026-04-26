from sqlalchemy.ext.asyncio import AsyncSession
from apps.backtester.data.models.models import Strategy
from third_party.candlestic import Chart
import backtrader as bt

class BacktestingService(bt.Strategy):

    def __init__(self, session : AsyncSession):
        self.session = session


    def backtest_using_backtrader(self, strategy : Strategy, chart : Chart):

        pass



class CustomPandasData(bt.feeds.PandasData):
    lines = ('atr', 'ma')  # add new lines
    params = (
        ('atr', -1),
        ('ma', -1),
    )

class MAStrategy1(bt.Strategy):

    def __init__(self):
        self.trades = []
        self.orders = []
        self._open_trades = {}

        self.call_counter = 0

    def calculate_volume(
            self,
            entry_price: float,
            stop_price: float,
            balance: int = 10000,
            risk: int = 1,
    ):
        self.call_counter += 1
        risk_amount = balance * (risk / 100)
        per_unit_risk = abs(entry_price - stop_price)
        units = risk_amount / per_unit_risk
        return int(units)

    def next(self):
        cal_ma_status = lambda close, ma: 'upper' if close > ma else 'under'

        ma = cal_ma_status(self.data.close[0], self.data.kama[0])

        if ma == "upper":
            price = self.data.close[0]
            entry_price = price
            stop_loss = entry_price - self.data.atr[0] * 4.8
            take_profit = entry_price + self.data.atr[0] * 2.4
            size = self.calculate_volume(
                entry_price,
                stop_loss,
                risk=2
            )
            self.buy_bracket(
                price=entry_price,
                stopprice=stop_loss,
                limitprice=take_profit,
                size=size,
                tradeid=1
            )

        # if current_ma_status == "under":
        #     price = self.data.close[0]
        #     entry_price = price
        #     stop_loss = entry_price + self.data.atr[0] * 2.4
        #     take_profit = entry_price - self.data.atr[0] * 4.8
        #     size = self.calculate_volume(
        #             entry_price,
        #             stop_loss,
        #             risk=2
        #         )
        #     self.sell_bracket(
        #         price=entry_price,
        #         stopprice=stop_loss,
        #         limitprice=take_profit,
        #         size=size
        #     )

    def notify_trade(self, trade: bt.trade.Trade):
        self.trades.append(trade)

    def notify_order(self, order):
        self.orders.append(order)






