from fastapi import APIRouter

from promptadmin.api.routers.config.base_config_router_factory import bind_view
from promptadmin.data.entity.variable import Variable, VariableData
from promptadmin.data.service.variable_service import VariableService

router = APIRouter()

variable_service = VariableService()

bind_view(router, VariableData, Variable, variable_service)
