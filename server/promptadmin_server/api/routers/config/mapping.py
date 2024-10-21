from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.service.mapping_service import MappingService

router = APIRouter()

config_service = BasePermissionConfigService(Mapping, MappingService())
config_service.bind(router)
