from promptadmin_server.api.exceptions import ProjectConnectionException
from settings import SETTINGS


class ConnectionMixin:
    @staticmethod
    def get_connection(project: str):
        connection = SETTINGS.connections.get(project)
        if connection is None:
            raise ProjectConnectionException()
