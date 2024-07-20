from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin.commons.dto import ViewParamsBuilder, ViewParamsOrder
from promptadmin.commons.entity.base_entity import BaseEntity
from promptadmin.commons.service.async_base_service import AsyncBaseService


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


def bind_view(
        router: APIRouter,
        entity_data: type(BaseModel),
        entity: type(BaseEntity),
        service: AsyncBaseService
):
    @router.get('/get/all', response_model=list[entity])
    async def get_all():
        view_params = ViewParamsBuilder().order(ViewParamsOrder(field=entity.id)).build()
        return await service.find_by_view_params(view_params)

    @router.post('/save', response_model=entity)
    async def save(_entity: entity):
        if _entity.id:
            change_entity = await service.find_by_id(_entity.id)
            if not change_entity:
                raise ValueError()
            d = _entity.dict()
            d.pop('id')
            for k, v in d.items():
                if k == 'time_create':
                    continue
                change_entity.__setattr__(k, v)
            return await service.save(change_entity)
        else:
            return await service.save(_entity)

    @router.get('/remove/{_id}', response_model=entity)
    async def remove(_id: int):
        remove_entity = await service.find_by_id(_id)
        if not remove_entity:
            raise ValueError()
        return await service.remove(remove_entity)
