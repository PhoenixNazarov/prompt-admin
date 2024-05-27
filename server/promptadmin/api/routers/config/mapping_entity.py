from fastapi import APIRouter

from promptadmin.api.routers.config.base_config_router_factory import bind_view
from promptadmin.data.entity.mapping_entity import MappingEntityData, MappingEntity
from promptadmin.data.service.mapping_entity_service import MappingEntityService

router = APIRouter()

mapping_entity_service = MappingEntityService()

bind_view(router, MappingEntityData, MappingEntity, mapping_entity_service)
