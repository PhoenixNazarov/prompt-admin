from typing import Any

from promptadmin_server.api.service.base import ConnectionMixin
from promptadmin_server.api.service.tables.dto import Column, TypeColumn


class TableItemService(ConnectionMixin):
    def __init__(self):
        pass

    async def load(self, project: str, table: str, id_: int):
        connection = self.get_connection(project)
        return dict(await connection.fetchrow(f"select * from {table} where id={id_}"))

    async def update(self, project: str, table: str, id_: int, columns: list[Column]):
        connection = self.get_connection(project)
        sql_statement = ""
        values: list[Any] = []

        for i in range(len(columns)):
            if i > 0:
                sql_statement += ", "
            sql_statement += f"{columns[i].key} = ${i + 1}"
            if isinstance(columns[i].value, TypeColumn):
                if columns[i].value.type == "bytes":
                    values.append(str(columns[i].value.value).encode())
                continue
            values.append(columns[i].value)
        sql = f"update {table} set {sql_statement} where id = {id_}"
        await connection.fetch(sql, *values)

    async def create(self, project: str, table: str, columns: list[Column]):
        connection = self.get_connection(project)
        sql_statement_columns = ""
        sql_statement_values = ""
        values: list[Any] = []

        for i in range(len(columns)):
            if i > 0:
                sql_statement_columns += ", "
                sql_statement_values += ", "
            sql_statement_columns += f"{columns[i].key}"
            sql_statement_values += f"${i + 1}"
            if isinstance(columns[i].value, TypeColumn):
                if columns[i].value.type == "bytes":
                    values.append(str(columns[i].value.value).encode())
                continue
            values.append(columns[i].value)

        sql = f"""
                insert into {table} ({sql_statement_columns})
                values ({sql_statement_values})
                returning id
                """
        return await connection.fetchrow(sql, *values)

    async def delete(self, project: str, table: str, id_: int):
        connection = self.get_connection(project)
        sql = f"delete from {table} where id = $1"
        await connection.fetch(sql, id_)
