from fastapi import FastAPI

from apps.py_trader.api.flags_api import flags_router

app = FastAPI()

app.include_router(flags_router)