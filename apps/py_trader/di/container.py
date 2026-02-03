from apps.py_trader.data.config.settings import Settings
from fastapi import Depends
from apps.py_trader.data.db.db import get_db
from apps.py_trader.data.repository.config_repo import ConfigRepo
from apps.py_trader.data.repository.flags_repo import FlagsRepo
from apps.py_trader.data.repository.strategy_repo import StrategyRepo
from apps.py_trader.data.repository.symbol_repo import SymbolRepo


class Container(object):

    @classmethod
    def settings(cls):
        return Settings()

    @classmethod
    def flags_repo(cls, db=Depends(get_db)) -> FlagsRepo:
        return FlagsRepo(db)

    @classmethod
    def configs_repo(cls, db = Depends(get_db)) -> ConfigRepo:
        return ConfigRepo(db)

    @classmethod
    def strategy_repo(cls, db = Depends(get_db)) -> StrategyRepo:
        return StrategyRepo(db)

    @classmethod
    def symbol_repo(cls, db = Depends(get_db)) -> SymbolRepo:
        return SymbolRepo(db)

