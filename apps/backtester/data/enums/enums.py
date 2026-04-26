from enum import Enum


class TriggerType(Enum):
    CROSS = 1
    PREDICTION = 2
    CLOSE_IF = 3
    CLOSE = 4
    PATTERN = 5

class StoplossType(Enum):
    PIP = 1
    ATR = 2
    PRICE_RATIO = 3
