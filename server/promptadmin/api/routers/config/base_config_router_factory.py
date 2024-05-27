from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin.api.service.user_data import UserData
from promptadmin.commons.dto.view_params import ViewParamsBuilder
from promptadmin.commons.dto.view_params_filter import ViewParamsFilter
from promptadmin.commons.dto.view_params_order import ViewParamsOrder
from promptadmin.commons.entity.base_entity import BaseEntity
from promptadmin.commons.error.unexpected_error import UnexpectedError
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


def bind_view(router: APIRouter,
              entity_data: type(BaseModel),
              entity: type(BaseEntity),
              service: AsyncBaseService):

    @router.get('/get/all', summary=f"Admin find page: {entity.__name__}", response_model=list[entity])
    async def get_all(request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        return await service.find_all()

    @router.get('/get/page/{page}', summary=f"Admin find page: {entity.__name__}", response_model=list[entity])
    async def get_page(page: int, request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        view_param = (ViewParamsBuilder()
                      .order(ViewParamsOrder(field=entity.id, desc=True))
                      .set_page(page)
                      .set_count(20)
                      .build())
        return await service.find_by_view_params(view_param)

    @router.get('/get/id/{_id}',
                summary=f"Admin find by id: {entity.__name__}",
                response_model=entity,
                responses={
                    401: {'description': "Can't find"},
                })
    async def get_by_id(_id: int, request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        _entity = await service.find_by_id(_id)
        if not _entity:
            raise UnexpectedError()
        return _entity

    @router.post('/get/ids',
                 summary=f"Admin find by ids: {entity.__name__}",
                 response_model=list[entity])
    async def get_by_ids(ids: IdsDto, request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        _entity = await service.find_by_ids(ids.ids)
        return _entity

    @router.post('/create', summary=f"Admin create: {entity.__name__}", response_model=entity)
    async def create(data: entity_data, request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        save_entity = entity(**data.dict())
        return await service.save(save_entity)

    @router.post('/change',
                 summary=f"Admin change: {entity.__name__}",
                 response_model=entity,
                 responses={
                     401: {'description': "Can't find"},
                 })
    async def change(_entity: entity, request: Request):
        change_entity = await service.find_by_id(_entity.id)
        if not change_entity:
            raise UnexpectedError()
        d = _entity.dict()
        d.pop('id')
        for k, v in d.items():
            setattr(change_entity, k, v)
        return await service.save(change_entity)

    @router.get('/remove/id/{id}',
                summary=f"Admin remove: {entity.__name__}",
                response_model=entity,
                responses={
                    401: {'description': "Can't find"},
                })
    async def remove(id: int, request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        remove_entity = await service.find_by_id(id)
        if not remove_entity:
            raise UnexpectedError()
        return await service.remove(remove_entity)

    @router.post('/get/query',
                 summary=f"Admin find by query: {entity.__name__}",
                 response_model=list[entity])
    async def get_by_query(query: QueryDto, request: Request):
        user_data: UserData = request.scope['user_data']
        if user_data.account is None:
            raise ValueError()
        builder = ViewParamsBuilder()
        for i in query.filters:
            field = getattr(entity, i.field, None)
            if field:
                if str(field.expression.type) == 'INTEGER':
                    builder.filter(ViewParamsFilter(field=field, value=int(i.value)))
                elif str(field.expression.type) == 'BOOLEAN':
                    builder.filter(ViewParamsFilter(field=field, value=bool(i.value)))
                elif str(field.expression.type) == 'VARCHAR':
                    builder.filter(ViewParamsFilter(field=field, value=i.value))
                elif str(field.expression.type) == 'DATETIME':
                    builder.filter(ViewParamsFilter(field=field, value=datetime.strptime(i.value, '%m/%d/%y %H:%M:%S')))
                elif str(field.expression.type) == 'FLOAT':
                    builder.filter(ViewParamsFilter(field=field, value=float(i.value)))

        for i in query.orders:
            field = getattr(entity, i.field, None)
            if field:
                builder.order(ViewParamsOrder(field=field, desc=i.desc))
        if query.count:
            builder.count(query.count)
        if query.page:
            builder.page(query.page)

        return await service.find_by_view_params(builder.build())
