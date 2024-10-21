import asyncpg

from promptadmin_server.api.exceptions import ProjectConnectionException
from settings import SETTINGS


class ConnectionMixin:
    @staticmethod
    async def get_connection(project: str):
        connection = SETTINGS.connections.get(project)
        if connection is None:
            raise ProjectConnectionException()
        return await asyncpg.connect(connection)

    @staticmethod
    def get_connection_dsn(project: str) -> str:
        connection = SETTINGS.connections.get(project)
        if connection is None:
            raise ProjectConnectionException()
        return connection
