from fastapi import APIRouter, Depends

from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.data.repository.pattern_repo import PatternRepo
from apps.py_trader.di import Container
from apps.py_trader.service.pattern.pattern_group_schema import PatternRead, PatternCreate, PatternGroupRead, \
    PatternGroupCreate

pattern_api = APIRouter(prefix= Routes.Pattern.PREFIX, tags=['Pattern'])

@pattern_api.post(path=Routes.Pattern.Create, response_model=PatternRead)
async def create_pattern(pattern_create : PatternCreate, pattern_repo : PatternRepo = Depends(Container.pattern_repo)):
    pattern = await pattern_repo.create_one(pattern_create.to_pattern())
    return pattern

@pattern_api.post(path=Routes.Pattern.CreateGroup, response_model=PatternGroupRead)
async def create_pattern(pattern_group_create : PatternGroupCreate, pattern_repo : PatternRepo = Depends(Container.pattern_repo)):
    pattern_group = await pattern_repo.create_one_group(pattern_group_create.to_pattern_group())
    return pattern_group

@pattern_api.get(path=Routes.Pattern.ReadManyGroups, response_model=list[PatternGroupRead])
async def read_many_groups(pattern_repo : PatternRepo = Depends(Container.pattern_repo)):
    result = await pattern_repo.read_many_groups()

    return result

# @pattern_api.post(path=Routes.Pattern.ReadOneGroup, response_model=PatternGroupRead)
# def _():
#     pass
#
# @pattern_api.get(path=Routes.Pattern.ReadManyGroups, response_model=list[PatternGroupRead])
# def _():
#     pass
