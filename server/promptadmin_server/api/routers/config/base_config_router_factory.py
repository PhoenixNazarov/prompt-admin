from datetime import datetime
from typing import Optional, Generic, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.base import (
    BasePermissionService,
    AbstractConfigService,
)
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsOrder
from promptadmin_server.commons.entity.base_entity import BaseEntity
from promptadmin_server.commons.service.async_base_service import AsyncBaseService


class FilterDto(BaseModel):
    field: str
    value: str | int | datetime | bool | float


class OrderDto(BaseModel):
    field: str
    desc: bool = False


class QueryDto(BaseModel):
    filters: list[FilterDto] = []
    orders: list[OrderDto] = []
    count: Optional[int]
    page: Optional[int]


class IdsDto(BaseModel):
    ids: list[int]


class FindByKeyRequest(BaseModel):
    key: str
    value: str | int | bool


Entity = TypeVar("Entity", bound=BaseEntity)


def bind_service(
    service: AbstractConfigService, entity: type[BaseEntity], router: APIRouter
):
    @router.get("/get/all")
    async def get_all(user_data: UserDependsAnnotated):
        return await service.get_all(user_data)

    @router.post("/save", response_model=entity)
    async def save(entity_: Entity, user_data: UserDependsAnnotated):
        return await service.save(entity_, user_data)

    @router.get("/remove/{_id}", response_model=entity)
    async def remove(id_: int, user_data: UserDependsAnnotated):
        return await service.remove(id_, user_data)

    @router.post("/find_by_key")
    async def find_by_key(
        find_by_key_request: FindByKeyRequest, user_data: UserDependsAnnotated
    ):
        return await service.find_by_key(
            find_by_key_request.key, find_by_key_request.value, user_data
        )


class BaseConfigService(Generic[Entity], AbstractConfigService[Entity]):
    def __init__(self, entity: type[Entity], service: AsyncBaseService):
        self.entity = entity
        self.service = service

    async def get_all(self, user_data: UserData):
        view_params = (
            ViewParamsBuilder().order(ViewParamsOrder(field=self.entity.id)).build()
        )
        return await self.service.find_by_view_params(view_params)

    async def save(self, _entity: Entity, user_data: UserData):
        if _entity.id:
            change_entity = await self.service.find_by_id(_entity.id)
            if not change_entity:
                raise TypeCheckException()
            d = _entity.dict()
            d.pop("id")
            for k, v in d.items():
                if k == "time_create":
                    continue
                change_entity.__setattr__(k, v)
            return await self.service.save(change_entity)
        else:
            return await self.service.save(_entity)

    async def remove(self, id_: int, user_data: UserData):
        remove_entity = await self.service.find_by_id(id_)
        if not remove_entity:
            raise TypeCheckException()
        return await self.service.remove(remove_entity)

    async def find_by_key(
        self, key: str, val: str | int | bool, user_data: UserData
    ) -> list[Entity]:
        return await self.service.find_by_key(getattr(self.entity, key, None), val)

    def bind(self, router: APIRouter):
        bind_service(self, self.entity, router)


class BasePermissionConfigService(BasePermissionService, BaseConfigService):
    def __init__(self, entity: type[Entity], service: AsyncBaseService):
        super().__init__(entity, service)

    async def get_all(self, user_data: UserData):
        await self.require_permission("config_tables", 1, user_data)
        return await super().get_all(user_data)

    async def save(self, _entity: Entity, user_data: UserData):
        await self.require_permission("config_tables", 2, user_data)
        return await super().save(_entity, user_data)

    async def remove(self, id_: int, user_data: UserData):
        await self.require_permission("config_tables", 2, user_data)
        return await super().remove(id_, user_data)

    async def find_by_key(
        self, key: str, val: str | int | bool, user_data: UserData
    ) -> list[Entity]:
        await self.require_permission("config_tables", 2, user_data)
        return await super().find_by_key(key, val, user_data)
