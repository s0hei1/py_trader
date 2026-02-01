from enum import Enum


class TimeFrameEnum(Enum):
    M1 = 'm1'
    M5 = 'm5'
    M15 = 'm15'
    H1 = 'H1'
    H4 = 'H4'
    Daily = 'daily'
    Weekly = 'weekly'
    Monthly = 'monthly'