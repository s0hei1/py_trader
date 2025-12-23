from src.ui.pages.other import chart
import asyncio

class LikeMarket:

    def __init__(self, chart : Chart):
        self.chart = chart


    async def open_market(self):

        for i in chart:
            asyncio.sleep(1)

            yield i


market = LikeMarket()

asyncio.run(market.open_market())