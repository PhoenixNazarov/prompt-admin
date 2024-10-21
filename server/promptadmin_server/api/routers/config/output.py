from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.data.entity.output import Output
from promptadmin_server.data.service.output_service import OutputService

router = APIRouter()

config_service = BasePermissionConfigService(Output, OutputService())
config_service.bind(router)
