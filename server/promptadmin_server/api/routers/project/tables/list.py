from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.utlis import get_connection

import re

router = APIRouter()


class ProjectRequest(BaseModel):
    project: str

    table: str


class SortByColumn(BaseModel):
    key: str
    order: str


class FilterColumn(BaseModel):
    key: str
    value: str | int | bool | None = None
    operator: str


class LoadRequest(ProjectRequest):
    columns: list[str]

    count: int | None = None
    page: int | None = None
    order_by: list[SortByColumn] | None = None,
    filter: list[FilterColumn] | None = None


def build_filter(load_request: LoadRequest):
    statement = ''
    if load_request.filter:
        if len(load_request.filter) > 0:
            statement = 'where '
        for filter_ in load_request.filter:
            if filter_.value is None:
                value = 'null'
            elif filter_.operator == 'like%':
                value = re.escape("'" + str(filter_.value) + "%'")
                filter_.operator = 'like'
            elif filter_.operator == '%like':
                value = re.escape("'%" + str(filter_.value) + "'")
                filter_.operator = 'like'
            elif filter_.operator == '%like%':
                value = re.escape("'%" + str(filter_.value) + "%'")
                filter_.operator = 'like'
            else:
                value = re.escape(filter_.value)

            statement += f' {filter_.key} {filter_.operator} {value} and'
    return statement.removesuffix('and')


@router.post('/load')
async def load(load_request: LoadRequest):
    connection = await get_connection(load_request.project)
    if not connection:
        return []

    limit = f'limit {load_request.count}' if load_request.count else ''
    offset = f'offset {load_request.count * load_request.page}' if load_request.count and load_request.page else ''
    order_by = ''
    where = build_filter(load_request)

    if load_request.order_by:
        first_el = load_request.order_by[0]
        order_by = f'order by {first_el.key} {first_el.order}'

    statement = (
        f'select {",".join(load_request.columns)} from {load_request.table} '
        f'{where} '
        f'{order_by} '
        f'{limit} '
        f'{offset} '
    )
    print(statement)
    return await connection.fetch(statement)


@router.post('/count')
async def count(load_request: LoadRequest):
    connection = await get_connection(load_request.project)
    if not connection:
        return -1

    where = build_filter(load_request)
    return await connection.fetchrow(f'select count(*) from {load_request.table} {where}')


@router.post('/fetch_columns')
async def fetch_columns(project_request: ProjectRequest):
    connection = await get_connection(project_request.project)
    if not connection:
        return []
    statement = 'select column_name, data_type from information_schema.columns where table_name = $1'
    return await connection.fetch(statement, project_request.table)
