from fastapi import APIRouter

from promptadmin.api.routers.config.base_config_router_factory import bind_view
from promptadmin.data.entity.mapping import MappingData, Mapping
from promptadmin.data.service.mapping_service import MappingService

router = APIRouter()

mapping_service = MappingService()

bind_view(router, MappingData, Mapping, mapping_service)
