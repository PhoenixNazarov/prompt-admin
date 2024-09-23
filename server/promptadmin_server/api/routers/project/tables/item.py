from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.utlis import get_connection

router = APIRouter()


class LoadItemRequest(BaseModel):
    project: str

    table: str
    id: int


class Column(BaseModel):
    key: str
    value: Any


class SaveItemRequest(LoadItemRequest):
    id: int | None = None
    columns: list[Column]


@router.post('/load')
async def load_id(load_item_request: LoadItemRequest):
    connection = await get_connection(load_item_request.project)
    if not connection:
        return {}

    return dict(await connection.fetchrow(f'select * from {load_item_request.table} where id={load_item_request.id}'))


@router.post('/update')
async def update(save_item_request: SaveItemRequest):
    connection = await get_connection(save_item_request.project)
    if not connection:
        return

    sql_statement = ''
    values = []

    for i in range(len(save_item_request.columns)):
        if i > 0:
            sql_statement += ', '
        sql_statement += f'{save_item_request.columns[i].key} = ${i + 1}'
        values.append(save_item_request.columns[i].value)

    sql = f"""
        UPDATE {save_item_request.table}
        SET {sql_statement}
        WHERE id = {save_item_request.id}
        """

    await connection.fetch(sql, *values)


@router.post('/create')
async def create(save_item_request: SaveItemRequest):
    connection = await get_connection(save_item_request.project)
    if not connection:
        return

    sql_statement_columns = ''
    sql_statement_values = ''
    values = []

    for i in range(len(save_item_request.columns)):
        if i > 0:
            sql_statement_columns += ', '
            sql_statement_values += ', '
        sql_statement_columns += f'{save_item_request.columns[i].key}'
        sql_statement_values += f'${i + 1}'
        values.append(save_item_request.columns[i].value)

    sql = f"""
        insert into {save_item_request.table} ({sql_statement_columns})
        values ({sql_statement_values})
        returning id
        """
    return await connection.fetchrow(sql, *values)


@router.post('/delete')
async def delete(load_item_request: LoadItemRequest):
    connection = await get_connection(load_item_request.project)
    if not connection:
        return

    sql = f"""
        delete from {load_item_request.table} where id = $1
    """

    await connection.fetch(sql, load_item_request.id)
