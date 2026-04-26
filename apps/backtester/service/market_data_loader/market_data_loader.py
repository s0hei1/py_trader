from third_party.candlestic import Symbol


class MarketDataLoader:

    def __init__(self,
                 use_offline_data : bool = True
                 ):
        self.use_offline_data = use_offline_data


    def load_market_data(self, symbol : Symbol):
        pass
