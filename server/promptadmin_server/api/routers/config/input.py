from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.input import Input, InputData
from promptadmin_server.data.service.input_service import InputService

router = APIRouter()

macro_service = InputService()

bind_view(router, InputData, Input, macro_service)
