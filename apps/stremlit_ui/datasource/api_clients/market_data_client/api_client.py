import pandas as pd
from httpx import Client
from apps.stremlit_ui.datasource.api_clients.market_data_client.client_models import BrokerModel, SymbolModel, \
    TimeFrameModel, CandleModel, \
    ReadManyCandlesRequest
from apps.stremlit_ui.datasource.api_clients.market_data_client.routes import Routes
import json


def market_data_client_factory(
        base_url: str = 'http://127.0.0.1:8000',
):
    return Client(
        base_url=base_url,
        timeout=5
    )


class MarketDataAPIClient():

    def __init__(self, client: Client):
        self.client = client

    def create_broker(self, broker: BrokerModel) -> BrokerModel:
        request = json.dumps(broker.to_dict(without_id=True))
        response = self.client.post(Routes.Broker.PREFIX + Routes.Broker.CreateOne, data=request)
        return BrokerModel(**response.json())

    def get_brokers(self) -> list[BrokerModel]:
        response = self.client.get(Routes.Broker.PREFIX + Routes.Broker.ReadMany)
        return [BrokerModel.from_dict(d) for d in response.json()]

    def create_symbol(self, symbol: SymbolModel) -> SymbolModel:
        request = json.dumps(symbol.to_dict(without_id=True))
        response = self.client.post(Routes.Symbol.PREFIX + Routes.Symbol.CreateOne, data=request)
        return SymbolModel(**response.json())

    def get_symbols(self) -> list[SymbolModel]:
        response = self.client.get(Routes.Symbol.PREFIX + Routes.Symbol.ReadMany)
        return [SymbolModel.from_dict(d) for d in response.json()]

    def create_time_frame(self, time_frame: TimeFrameModel) -> TimeFrameModel:
        request = json.dumps(time_frame.to_dict(without_id=True))
        response = self.client.post(Routes.TimeFrame.PREFIX + Routes.TimeFrame.CreateOne, data=request)
        return TimeFrameModel(**response.json())

    def get_time_frames(self) -> list[TimeFrameModel]:
        response = self.client.get(Routes.TimeFrame.PREFIX + Routes.TimeFrame.ReadMany)
        return [TimeFrameModel.from_dict(d) for d in response.json()]

    def get_candles(self, request: ReadManyCandlesRequest, to_dataframe: bool = False) -> list[
                                                                                              CandleModel] | pd.DataFrame:
        response = self.client.get(Routes.Candle.PREFIX + Routes.Candle.ReadMany, params=request.to_dict())


        if to_dataframe:
            return pd.DataFrame(response.json())
        return [CandleModel.from_dict(d) for d in response.json()]
