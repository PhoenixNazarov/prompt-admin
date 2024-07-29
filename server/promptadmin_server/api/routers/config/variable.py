from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.variable import Variable, VariableData
from promptadmin_server.data.service.variable_service import VariableService

router = APIRouter()

variable_service = VariableService()

bind_view(router, VariableData, Variable, variable_service)
