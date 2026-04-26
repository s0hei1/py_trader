from httpx import Client

from apps.stremlit_ui.datasource.api_clients.market_data_client.api_client import MarketDataAPIClient,market_data_client_factory


class Container:

    @classmethod
    def market_data_api_client(cls, ) -> MarketDataAPIClient:
        return MarketDataAPIClient(
            client=market_data_client_factory()
        )