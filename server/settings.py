import os
from promptadmin_server.commons.dto.base_settings import (
    BaseSettings,
    BaseRouter,
    DatabaseCred
)


class _Settings(BaseSettings):
    app: str = 'prompt-admin'

    database: list[DatabaseCred] = [
        DatabaseCred(
            username=os.environ['PA_DATABASE_USERNAME'],
            password=os.environ['PA_DATABASE_PASSWORD'],
            host=os.environ['PA_DATABASE_HOST'],
            port=int(os.environ['PA_DATABASE_PORT']),
            database=os.environ['PA_DATABASE_DATABASE']
        )
    ]

    message_routers: list[BaseRouter] = []

    connections: dict[str, str] = {}

    projects: dict[str, ProjectInfo] = {
        'fundmarket': ProjectInfo(
            connection='',
            sync_endpoint='http://0.0.0.0:8081/api/prompt-admin/collect',
            sync_secret='test'
        )
    }


SETTINGS = _Settings()

for k, v in os.environ.items():
    if k.startswith('PA_CONNECTION_'):
        name = k.removeprefix('PA_CONNECTION_').lower()
        SETTINGS.connections[name] = v
