import re

from promptadmin_server.api.service.base import ConnectionMixin
from promptadmin_server.api.service.tables.dto import (
    FilterColumn,
    JoinColumn,
    SortByColumn,
)


class TableListService(ConnectionMixin):
    @staticmethod
    def _build_filter(filters: list[FilterColumn]):
        statement = "where "
        for filter_ in filters:
            if filter_.value is None:
                value = "null"
            elif filter_.operator == "like%":
                value = re.escape("'" + str(filter_.value) + "%'")
                filter_.operator = "like"
            elif filter_.operator == "%like":
                value = re.escape("'%" + str(filter_.value) + "'")
                filter_.operator = "like"
            elif filter_.operator == "%like%":
                value = re.escape("'%" + str(filter_.value) + "%'")
                filter_.operator = "like"
            else:
                value = re.escape(filter_.value)

            statement += f" {filter_.key} {filter_.operator} {value} and"
        return statement.removesuffix("and")

    @staticmethod
    def _build_join(joins: list[JoinColumn]):
        statement = ""
        for join in joins:
            statement += f'join {join.table} {join.pseudo if join.pseudo else ""} on {join.condition} '
        return statement

    @staticmethod
    def _build_orders(sorts: list[SortByColumn]):
        first_el = sorts[0]
        return f"order by {first_el.key} {first_el.order}"

    async def load(
        self,
        project: str,
        table: str,
        columns: list[str],
        count: int | None,
        page: int | None,
        order_by: list[SortByColumn] | None,
        filters: list[FilterColumn] | None,
        joins: list[JoinColumn] | None,
    ):
        connection = await self.get_connection(project)

        limit = f"limit {count}" if count else ""
        offset = f"offset {count * page}" if count and page else ""
        orders = self._build_orders(order_by) if order_by else ""
        where = self._build_filter(filters) if filters else ""
        join = self._build_join(joins) if joins else ""

        statement = (
            f'select {",".join(columns)} from {table} '
            f"{join} "
            f"{where} "
            f"{orders} "
            f"{limit} "
            f"{offset} "
        )
        return await connection.fetch(statement)

    async def count(
        self,
        project: str,
        table: str,
        filters: list[FilterColumn] | None,
        joins: list[JoinColumn] | None,
    ):
        connection = await self.get_connection(project)
        where = self._build_filter(filters) if filters else ""
        join = self._build_join(joins) if joins else ""
        return await connection.fetchrow(f"select count(*) from {table} {join} {where}")

    async def fetch_columns(self, project: str, table: str):
        connection = await self.get_connection(project)
        statement = "select column_name, data_type from information_schema.columns where table_name = $1"
        return await connection.fetch(statement, table)
