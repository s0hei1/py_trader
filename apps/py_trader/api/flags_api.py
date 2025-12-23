from fastapi.routing import APIRouter

from apps.py_trader.service.schema.flags_schema import FlagsRead

flags_router = APIRouter(tags=['Config'])

@flags_router.get(path='read_config', response_model=FlagsRead)
def get_config() -> FlagsRead:

    response = FlagsRead()

    return response




