from backtrader import Analyzer,Trade
from backtrader import AutoOrderedDict
import pandas as pd

class EquityTracker(Analyzer):


    def __init__(self):
        self.trade_counter = 0
        self.rets = []


    def notify_trade(self, trade : Trade):
        if trade.isclosed:
            self.trade_counter += 1
            self.rets.append({"Index" : self.trade_counter,
                              "Equity" : self.strategy.broker.getvalue()})

        super(EquityTracker, self).notify_trade(trade)


    def get_analysis(self, as_dataframe : bool = False):
        if as_dataframe:
            return pd.DataFrame(self.rets,columns=['Index', 'Equity'])

        return self.rets






