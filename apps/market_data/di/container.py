from apps.market_data.data.config.settings import Settings
from fastapi import Depends
from apps.market_data.data.db.db import get_db
from apps.market_data.data.repository import BrokerRepo,CandleRepo,FlagsRepo,SymbolRepo,TimeFrameRepo



class Container(object):

    @classmethod
    def settings(cls):
        return Settings()

    @classmethod
    def flags_repo(cls, db=Depends(get_db)) -> FlagsRepo:
        return FlagsRepo(db)

    @classmethod
    def broker_repo(cls, db = Depends(get_db)) -> BrokerRepo:
        return BrokerRepo(db)

    @classmethod
    def candle_repo(cls, db = Depends(get_db)) -> CandleRepo:
        return CandleRepo(db)

    @classmethod
    def symbol_repo(cls, db = Depends(get_db)) -> SymbolRepo:
        return SymbolRepo(db)

    @classmethod
    def time_frame_repo(cls, db = Depends(get_db)) -> TimeFrameRepo:
        return TimeFrameRepo(db)
