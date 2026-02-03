from fastapi import APIRouter, Depends

from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.data.repository.strategy_repo import StrategyRepo
from apps.py_trader.di import Container
from apps.py_trader.service.strategy.strategy_schema import StrategyCreate, StrategyRead

strategy_api = APIRouter(prefix= Routes.Strategy.PREFIX, tags=['Strategy'])


@strategy_api.post(path=Routes.Strategy.Create, response_model=StrategyRead)
async def create_strategy(
        strategy_create : StrategyCreate,
        strategy_repo : StrategyRepo = Depends(Container.strategy_repo)
):
    strategy = await strategy_repo.create(strategy_create.to_strategy())
    return strategy

@strategy_api.get(path=Routes.Strategy.ReadMany, response_model=list[StrategyRead])
async def create_strategy(strategy_repo : StrategyRepo = Depends(Container.strategy_repo)):
    strategies = await strategy_repo.read_many()
    return strategies
