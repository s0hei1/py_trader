from apps.py_trader.data.config.settings import Settings
from fastapi import Depends
from apps.py_trader.data.db.db import get_db
from apps.py_trader.data.repository.flags_repo import FlagsRepo

class Container(object):


    @classmethod
    def settings(cls):
        return Settings()

    @classmethod
    def flags_repo(cls, db=Depends(get_db)) -> FlagsRepo:
        return FlagsRepo(db)

