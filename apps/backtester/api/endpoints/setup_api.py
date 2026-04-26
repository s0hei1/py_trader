from fastapi import APIRouter
from apps.backtester.api.routes import Routes

setup_api = APIRouter(prefix = Routes.MABacktesting.PREFIX)

