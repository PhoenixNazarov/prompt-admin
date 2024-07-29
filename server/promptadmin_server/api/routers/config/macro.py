from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.macro import Macro, MacroData
from promptadmin_server.data.service.macro_service import MacroService

router = APIRouter()

macro_service = MacroService()

bind_view(router, MacroData, Macro, macro_service)
