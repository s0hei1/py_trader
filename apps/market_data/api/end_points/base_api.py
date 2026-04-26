from fastapi import APIRouter, Depends
from apps.market_data.api.routes.routes import Routes

base_api_router = APIRouter(prefix=Routes.Base.PREFIX, tags=["Base"])

# @base_api.get(Routes.Base.FlagsRead, response_model=FlagsRead)
# async def read_flags(flags_repo: FlagsRepo = Depends(Container.flags_repo)):
#     return await flags_repo.get_or_config_flags()
#
# @base_api.put(Routes.Base.FlagsUpdate, response_model=FlagsRead)
# async def update_flags(
#     payload: FlagsCreate,
#     flags_repo: FlagsRepo = Depends(Container.flags_repo)
# ):
#     return await flags_repo.update(payload)