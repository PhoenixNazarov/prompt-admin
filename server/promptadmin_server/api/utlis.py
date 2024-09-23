import asyncpg

from settings import SETTINGS


async def get_connection(project: str):
    try:
        if project in SETTINGS.connections:
            return await asyncpg.connect(SETTINGS.connections[project])
    except Exception:
        pass
