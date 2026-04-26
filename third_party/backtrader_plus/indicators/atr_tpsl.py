from backtrader.indicators import Indicator,AverageTrueRange

class ATR_TPSL(Indicator):
    params = (
        ('atr_period', 16),
        ('tp_size', 1),
        ('sl_size', 1),
        ('is_buy', True),
    )

    lines = ('tp', 'sl')

    def __init__(self):
        atr = AverageTrueRange(period=self.p.atr_period)
        if self.p.is_buy:
            self.lines.tp = self.data.close + (atr * self.p.tp_size)
            self.lines.sl = self.data.close - (atr * self.p.sl_size)
        else:
            self.lines.tp = self.data.close - (atr * self.p.tp_size)
            self.lines.sl = self.data.close + (atr * self.p.sl_size)