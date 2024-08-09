from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.mapping_entity import MappingEntityData, MappingEntity
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService

router = APIRouter()

mapping_entity_service = MappingEntityService()

bind_view(router, MappingEntityData, MappingEntity, mapping_entity_service)


class MappingEntityDto(BaseModel):
    connection_name: str
    table: str
    field: str
    name: str


@router.get('/disable/get/all')
async def disable_get_all():
    return await mapping_entity_service.find_by_key(MappingEntity.entity, 'disable')


@router.post('/disable/create')
async def disable_create(mapping_entity_dto: MappingEntityDto):
    mapping_entity = MappingEntity(
        connection_name=mapping_entity_dto.connection_name,
        table=mapping_entity_dto.table,
        field=mapping_entity_dto.field,
        name=mapping_entity_dto.name,
        entity='disable',
        entity_id=1
    )
    return await mapping_entity_service.save(mapping_entity)
