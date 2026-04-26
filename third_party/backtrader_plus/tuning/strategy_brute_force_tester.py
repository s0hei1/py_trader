from backtrader import Cerebro
from backtrader.feeds import DataBase
from typing import Sequence

def strategy_brute_force_test(
        data: DataBase,
        strategy_type: type,
        TPs: Sequence,
        SLs: Sequence,
        maximum_parallel_trades: Sequence,
        **strategy_other_params) -> dict:
    broker_values = []
    various_settings = []
    for tp in TPs:
        for sl in SLs:
            for _max in maximum_parallel_trades:
                d = {
                    'tp_size': tp,
                    'sl_size': sl,
                    'max_parallel_trades': _max,
                }
                various_settings.append(d)
    for settings in various_settings:
        cerebro = Cerebro()
        cerebro.adddata(data)
        cerebro.addstrategy(strategy_type, **settings, **strategy_other_params)
        cerebro.broker.setcash(1000000)
        cerebro.broker.set_coo(True)
        cerebro.run()
        broker_values.append({
            'settings': settings,
            'value': cerebro.broker.getvalue()
        })

    return broker_values