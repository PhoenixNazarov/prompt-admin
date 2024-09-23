from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.utlis import get_connection

import re

router = APIRouter()


class SortByColumn(BaseModel):
    key: str
    order: str


class FilterColumn(BaseModel):
    key: str
    value: str | None = None
    like: bool | None = None


class LoadRequest(BaseModel):
    project: str

    table: str
    columns: list[str]

    count: int | None = None
    page: int | None = None
    order_by: list[SortByColumn] | None = None,
    filter: FilterColumn | None = None


def build_filter(load_request: LoadRequest):
    filter = ''
    if load_request.filter:
        if load_request.filter.value is None:
            filter = f"where {load_request.filter.key} is null  "
        elif load_request.filter.like:
            filter = f"where {load_request.filter.key} like E'{re.escape(load_request.filter.value + '%')}' "
        else:
            filter = f"where {load_request.filter.key} = E'{re.escape(load_request.filter.value)}' "
    return filter


@router.post('/load')
async def load(load_request: LoadRequest):
    connection = await get_connection(load_request.project)
    if not connection:
        return []

    limit = f'limit {load_request.count}' if load_request.count else ''
    offset = f'offset {load_request.count * load_request.page}' if load_request.count and load_request.page else ''
    order_by = ''
    filter = build_filter(load_request)

    if load_request.order_by:
        first_el = load_request.order_by[0]
        order_by = f'order by {first_el.key} {first_el.order}'

    statement = (
        f'select {",".join(load_request.columns)} from {load_request.table} '
        f'{filter} '
        f'{order_by} '
        f'{limit} '
        f'{offset} '
    )
    return await connection.fetch(statement)


@router.post('/count')
async def count(load_request: LoadRequest):
    connection = await get_connection(load_request.project)
    if not connection:
        return -1

    filter = build_filter(load_request)
    return await connection.fetchrow(f'select count(*) from {load_request.table} {filter}')
