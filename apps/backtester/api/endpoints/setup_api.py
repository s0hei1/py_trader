from fastapi import APIRouter
from fastapi import Depends

from apps.backtester.api.router.routes import Routes
from apps.backtester.data.repository.setup_repo import SetupRepo
from apps.backtester.di.container import Container
from apps.backtester.service.setup.setup_schema import SetupRead, SetupCreate

setup_api = APIRouter(prefix = Routes.Setup.PREFIX)

@setup_api.post(Routes.Setup.CreateOne, response_model=SetupRead)
async def create_one_setup(setup_create: SetupCreate, setup_repo : SetupRepo = Depends(Container.setup_repo)):
    return await setup_repo.create_one(setup_create.to_setup())

@setup_api.post(Routes.Setup.ReadMany, response_model=list[SetupRead])
async def read_many_setups(setup_repo : SetupRepo = Depends(Container.setup_repo)):
    return await setup_repo.read_many()

