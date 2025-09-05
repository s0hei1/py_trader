from sqlalchemy.orm import Session
from src.data.repo.flags_repo import FlagsRepo
from src.data.repo.pattern_repo import PatternRepo
from src.tools.config.settings import Settings


class Container():

    @classmethod
    def settings(cls) -> Settings:
        return Settings()

    @classmethod
    def get_session(cls) -> Session:
        from src.data.core.db import get_session
        return get_session()

    @classmethod
    def flags_repo(cls) -> FlagsRepo:
        return FlagsRepo(session= Container.get_session())

    @classmethod
    def pattern_repo(cls) -> PatternRepo:
        return PatternRepo(session=Container.get_session())
