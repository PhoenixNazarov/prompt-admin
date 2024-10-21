from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.data.entity.input import Input
from promptadmin_server.data.service.input_service import InputService

router = APIRouter()

config_service = BasePermissionConfigService(Input, InputService())
config_service.bind(router)
