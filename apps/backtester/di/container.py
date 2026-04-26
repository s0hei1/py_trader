from fastapi import Depends
from apps.backtester.data.config.settings import Settings
from apps.backtester.data.db.db import get_db
from apps.backtester.data.repository.risk_management_repo import RiskManagementRepo
from apps.backtester.data.repository.setup_repo import SetupRepo
from apps.backtester.data.repository.strategy_repo import StrategyRepo


class Container:

    @classmethod
    def settings(cls) -> Settings:
        return Settings()

    @classmethod
    def setup_repo(cls, db=Depends(get_db)) -> SetupRepo:
        return SetupRepo(db)

    @classmethod
    def strategy_repo(cls, db=Depends(get_db)) -> StrategyRepo:
        return StrategyRepo(db)

    @classmethod
    def risk_management_repo(cls, db=Depends(get_db)) -> RiskManagementRepo:
        return RiskManagementRepo(db)

