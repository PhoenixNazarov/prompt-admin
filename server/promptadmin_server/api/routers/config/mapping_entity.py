from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_prompt_service import (
    PermissionPromptService,
)
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService

router = APIRouter()

mapping_entity_service = MappingEntityService()
permission_prompt_service = PermissionPromptService()

config_service = BasePermissionConfigService(MappingEntity, mapping_entity_service)
config_service.bind(router)


class MappingEntityDto(BaseModel):
    connection_name: str
    table: str
    field: str
    name: str


@router.get("/disable/get/all")
async def disable_get_all(user_data: UserDependsAnnotated):
    return permission_prompt_service.get_disable(user_data)


@router.post("/disable/create")
async def disable_create(
    mapping_entity_dto: MappingEntityDto, user_data: UserDependsAnnotated
):
    return permission_prompt_service.create_disable(
        mapping_entity_dto.connection_name,
        mapping_entity_dto.table,
        mapping_entity_dto.field,
        mapping_entity_dto.name,
        user_data,
    )
