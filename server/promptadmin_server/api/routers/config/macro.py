from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.data.entity.macro import Macro
from promptadmin_server.data.service.macro_service import MacroService

router = APIRouter()

config_service = BasePermissionConfigService(Macro, MacroService())
config_service.bind(router)
