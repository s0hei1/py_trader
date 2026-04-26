from backtrader.indicators import CrossOver, AverageTrueRange, AdaptiveMovingAverage, MovingAverageSimple
from backtrader import Strategy, Trade
from backtrader import Order

class KamaBuyV2Strategy(Strategy):

    @staticmethod
    def get_params(as_tuple: bool = False) -> dict | tuple:
        p_ = {
            'ma_period': 24,
            'structure_ma_period': 240,
            'atr_period': 24,
            'risk_size': 1,
            'max_parallel_trades': 5,
            'tp_size': 6,
            'sl_size': 2,
        }
        if as_tuple:
            result_ = [(i, p_[i]) for i in p_]
            return tuple(result_)

        return p_

    params = get_params(as_tuple=True)

    def __init__(self):
        self.ma = AdaptiveMovingAverage(period=self.p.ma_period)
        self.cross_over = CrossOver(self.data.close, self.ma)
        self.atr = AverageTrueRange(period=self.p.atr_period)
        self.sma240 = MovingAverageSimple(period=self.p.structure_ma_period)
        self.trade_id = 1
        self.open_trades_counter = 0

    def generate_trade_id(self):
        self.trade_id += 1
        return self.trade_id

    def next(self):
        if self.cross_over[0] > 0 and self.sma240[0] < self.data.close[
            0] and self.open_trades_counter <= self.p.max_parallel_trades:
            entry = self.data.close[0]
            atr = self.atr[0]
            tp = entry + (atr * self.p.tp_size)

            tp = round(tp, 5)

            stop = entry - (atr * self.p.sl_size)
            stop = round(stop, 5)

            trade_size = self._get_size(entry, stop)

            self.buy_bracket(
                exectype=Order.Market,
                stopprice=stop,
                limitprice=tp,
                size=trade_size,
                tradeid=self.generate_trade_id(),
            )

    def _get_size(
            self,
            entry_price: float,
            stop_price: float,
            balance: int = 10000,
            risk: float = 1,
    ):
        risk_amount = balance * (risk / 100)
        stop_size = abs(entry_price - stop_price)
        units = risk_amount / stop_size
        return int(units)

    def notify_trade(self, trade: Trade):
        if trade.justopened:
            self.open_trades_counter += 1
        if trade.isclosed:
            self.open_trades_counter -= 1



"""brute force_ top results"""
# {'settings': {'tp_size': 6, 'sl_size': 2, 'max_parallel_trades': 5},'value': 1019208.3248100006}
# {'settings': {'tp_size': 6, 'sl_size': 2, 'max_parallel_trades': 4},'value': 1017432.6203400004}