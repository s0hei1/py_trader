from sqlalchemy import select,func
from sqlalchemy.orm import Session
from src.data.core.models import PlaceOrder

class PlaceOrderRepo:

    def __init__(self, session : Session):
        self.session = session

    def create(self, place_order : PlaceOrder) -> PlaceOrder:
        self.session.add(place_order)
        self.session.refresh(place_order)
        return place_order

    def generate_place_order_code(self) -> str | None:

        result = self.session.execute(
            select(func.max(PlaceOrder.order_code))
        ).scalar_one_or_none()

        if result is None:
            start_code = 10000
            return str(start_code)

        try:
            generated_code = int(result) + 1
            return str(generated_code)
        except Exception:
            return None
