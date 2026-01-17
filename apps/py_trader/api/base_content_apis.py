from fastapi.routing import APIRouter
from apps.py_trader.service.schema.flags_schema import FlagsRead

base_content_apis = APIRouter(tags=['Config'])

@base_content_apis.get(path='/read_flags', response_model=FlagsRead)
def read_flags() -> FlagsRead:

    response = FlagsRead()

    return response

