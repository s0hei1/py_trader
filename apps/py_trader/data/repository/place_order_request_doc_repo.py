from sqlalchemy.ext.asyncio import AsyncSession

from apps.py_trader.data.models.models import PlaceOrderRequestDoc


class PlaceOrderRequestDocRepo:

    def __init__(self, session : AsyncSession) -> None:
        self.session = session


    async def create_one(self, place_order_request_doc : PlaceOrderRequestDoc):

        self.session.add(place_order_request_doc)
        await self.session.commit()
        await self.session.refresh(place_order_request_doc)

        return place_order_request_doc

