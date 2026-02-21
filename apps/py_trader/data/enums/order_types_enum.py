from enum import Enum
from third_party.mt5_overhead import OrderTypes
from third_party.mt5_overhead.ordertype import OrderType


class OrderTypeEnum(Enum):
    BUY_LIMIT = 1,
    SELL_LIMIT = 2,

    def to_order_type(self) -> OrderType:
        return OrderTypes.get_order_type_by_id(self.value[0])
