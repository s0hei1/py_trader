from fastapi import Depends
from fastapi.routing import APIRouter
from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.data.repository.config_repo import ConfigRepo
from apps.py_trader.data.repository.flags_repo import FlagsRepo
from apps.py_trader.di import Container
from apps.py_trader.service.base.config_schema import ConfigRead, ConfigCreate
from apps.py_trader.service.base.flags_schema import FlagsRead

base_api = APIRouter(prefix= Routes.Base.PREFIX, tags=['Base'])

@base_api.get(path=Routes.Base.FlagsRead, response_model=FlagsRead)
async def read_flags(flags_repo : FlagsRepo = Depends(Container.flags_repo)):

    response = await flags_repo.get_or_config_flags()

    return response


@base_api.post(path=Routes.Base.ConfigCreate, response_model=ConfigRead)
async def create_config(config : ConfigCreate, config_repo : ConfigRepo = Depends(Container.configs_repo)):

    response = await config_repo.create_config(config.to_config())

    return response


@base_api.get(path=Routes.Base.ConfigReadLast, response_model=ConfigRead)
async def read_last_config(config_repo: ConfigRepo = Depends(Container.configs_repo)):

    config = await config_repo.read_last_config()

    return config

@base_api.get(path=Routes.Base.ConfigReadHistory, response_model=list[ConfigRead])
async def read_configs_history(config_repo: ConfigRepo = Depends(Container.configs_repo)):

    configs = await config_repo.read_configs_history()

    return configs