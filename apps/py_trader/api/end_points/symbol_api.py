from fastapi import APIRouter, Depends
from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.data.repository.symbol_repo import SymbolRepo
from apps.py_trader.di import Container
from apps.py_trader.service.symbol.symbol_schema import SymbolCreate, SymbolRead

symbol_api = APIRouter(prefix= Routes.Symbol.PREFIX, tags=['Symbol'])

@symbol_api.post(path=Routes.Symbol.CreateOne, response_model=SymbolRead)
async def create_symbol(
        symbol_create : SymbolCreate,
        symbol_repo : SymbolRepo = Depends(Container.symbol_repo)
):
    symbol = await symbol_repo.create_one(symbol_create.to_symbol())
    return symbol

@symbol_api.get(path=Routes.Symbol.ReadMany, response_model=list[SymbolRead])
async def read_many_symbols(symbol_repo : SymbolRepo = Depends(Container.symbol_repo)):
    symbols = await symbol_repo.read_many()
    return symbols
