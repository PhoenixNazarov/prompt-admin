from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.mapping import MappingData, Mapping
from promptadmin_server.data.service.mapping_service import MappingService

router = APIRouter()

mapping_service = MappingService()

bind_view(router, MappingData, Mapping, mapping_service)
