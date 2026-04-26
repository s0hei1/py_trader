from fastapi import APIRouter
from fastapi import Depends

from apps.backtester.api.router.routes import Routes
from apps.backtester.data.repository.strategy_repo import StrategyRepo
from apps.backtester.di.container import Container
from apps.backtester.service.strategy.strategy_schema import StrategyRead, StrategyCreate

strategy_api = APIRouter(prefix = Routes.Strategy.PREFIX)

@strategy_api.post(Routes.Strategy.CreateOne, response_model=StrategyRead)
async def create_one_Strategy(strategy_create: StrategyCreate, strategy_repo : StrategyRepo = Depends(Container.strategy_repo)):
    return await strategy_repo.create_one(strategy_create.to_strategy())

@strategy_api.post(Routes.Strategy.ReadMany, response_model=list[StrategyRead])
async def read_many_Strategys(strategy_repo : StrategyRepo = Depends(Container.strategy_repo)):
    return await strategy_repo.read_many()
