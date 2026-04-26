from fastapi import APIRouter
from fastapi import Depends

from apps.backtester.api.router.routes import Routes
from apps.backtester.data.repository.risk_management_repo import RiskManagementRepo
from apps.backtester.di.container import Container
from apps.backtester.service.risk_management.risk_management_schema import RiskManagementRead, RiskManagementCreate

risk_management_api = APIRouter(prefix = Routes.RiskManagement.PREFIX)

@risk_management_api.post(Routes.RiskManagement.CreateOne, response_model=RiskManagementRead)
async def create_one_setup(risk_management_create: RiskManagementCreate, setup_repo : RiskManagementRepo = Depends(Container.risk_management_repo)):
    return await setup_repo.create_one(risk_management_create.to_risk_management())

@risk_management_api.post(Routes.RiskManagement.ReadMany, response_model=list[RiskManagementRead])
async def read_many_setups(risk_management_repo : RiskManagementRepo = Depends(Container.risk_management_repo)):
    return await risk_management_repo.read_many()

