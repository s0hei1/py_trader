from enum import Enum


class PlaceOrderStatus(Enum):
    PENDING = 0
    CANCELLED = 1
    FAILED = 2
    SUCCESS = 3
