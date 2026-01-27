from fastapi import Depends
from fastapi.routing import APIRouter

from apps.py_trader.data.repository.flags_repo import FlagsRepo
from apps.py_trader.di import Container
from apps.py_trader.service.schema.flags_schema import FlagsRead

base_api = APIRouter(tags=['Config'])

@base_api.get(path='/read_flags', response_model=FlagsRead)
async def read_flags(flags_repo : FlagsRepo = Depends(Container.flags_repo)) -> FlagsRead:

    response = await flags_repo.get_or_config_flags()

    return response

