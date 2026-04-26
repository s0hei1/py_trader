from fastapi import APIRouter, Depends
from apps.market_data.api.routes.routes import Routes
from apps.market_data.di import Container
from apps.market_data.data.repository import  SymbolRepo
from apps.market_data.service.symbol_schema import SymbolRead, SymbolCreate

symbol_api_router = APIRouter(prefix=Routes.Symbol.PREFIX, tags=["Symbols"])

@symbol_api_router.post(Routes.Symbol.CreateOne, response_model=SymbolRead)
async def create_symbol(
    payload: SymbolCreate,
    symbol_repo: SymbolRepo = Depends(Container.symbol_repo)
):
    return await symbol_repo.create_one(payload.to_symbol())

@symbol_api_router.get(Routes.Symbol.ReadMany, response_model=list[SymbolRead])
async def read_many_symbols(symbol_repo: SymbolRepo = Depends(Container.symbol_repo)):
    return await symbol_repo.read_many()
