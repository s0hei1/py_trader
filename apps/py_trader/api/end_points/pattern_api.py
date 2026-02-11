from fastapi import APIRouter, Depends

from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.data.repository.pattern_repo import PatternRepo
from apps.py_trader.di import Container
from apps.py_trader.service.pattern.pattern_group_schema import PatternRead, PatternCreate
from apps.py_trader.service.pattern.pattern_schema import PatternGroupRead

pattern_api = APIRouter(prefix= Routes.Pattern.PREFIX, tags=['Pattern'])

@pattern_api.post(path=Routes.Pattern.Create, response_model=PatternRead)
def create_pattern(pattern_create : PatternCreate, pattern_repo : PatternRepo = Depends(Container.pattern_repo)):
    pattern = pattern_repo.create(pattern_create.to_pattern())
    return pattern

@pattern_api.get(path=Routes.Pattern.ReadOne, response_model=PatternRead)
def _():
    pass
@pattern_api.get(path=Routes.Pattern.ReadMany, response_model=list[PatternRead])
def _():
    pass

@pattern_api.post(path=Routes.Pattern.ReadOneGroup, response_model=PatternGroupRead)
def _():
    pass

@pattern_api.get(path=Routes.Pattern.ReadManyGroups, response_model=list[PatternGroupRead])
def _():
    pass
