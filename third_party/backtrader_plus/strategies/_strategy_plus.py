from third_party.backtrader_plus.indicators.atr_tpsl import ATR_TPSL
from backtrader import Trade,Strategy

class StrategyPlus(Strategy):

    params = (
        ('tp_size' , 1),
        ('sl_size' , 1),
        ('max_parallel_trades' , 3),
        ('sizer' , None)
    )


    def get_current_trades_count(self):
        if not hasattr('_current_trades_counter'):
            raise ValueError('_current_trades_counter has not been initialized')

        return self._current_trades_counter


    def notify_trade(self, trade : Trade):
        if not hasattr('_current_trades_counter'):
            self._current_trades_counter = 0
        else:
            if trade.justopened:
                self._current_trades_counter += 1
            if trade.isclosed:
                self._current_trades_counter -= 1

        super(StrategyPlus, self).notify_trade(trade)




