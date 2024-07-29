from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlmodel import SQLModel, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import SETTINGS
from ..dto.view_params import ViewParams
from .sql_utils import SqlUtils

from logging import getLogger

logger = getLogger(__name__)


class AsyncSqlSubController:
    def __init__(self, dsn: str):
        if not dsn:
            logger.warning('AsyncSqlSubController not import. Dsn is None.')
            return
        self.engine = create_async_engine(dsn, connect_args={
            'server_settings': {'application_name': 'Async ' + SETTINGS.app}
        })
        self.async_session = async_sessionmaker(self.engine)

    async def __find_all(self, statement):
        async with self.async_session() as session:
            rows = (await session.execute(statement)).all()
            return SqlUtils.unpack(rows)

    async def __find_first(self, statement):
        async with self.async_session() as session:
            model = (await session.execute(statement)).first()
            if model:
                return model[0]
            return

    async def __find_count(self, statement):
        statement = select(func.count()).select_from(statement)
        async with self.async_session() as session:
            return (await session.execute(statement)).scalar()

    async def execute(self, statement, params):
        async with self.engine.begin() as conn:
            return await conn.execute(statement, params)

    async def find_by_view_params_all(self, model: type(SQLModel), view_params: ViewParams):
        statement = SqlUtils.build_statement_by_view_params(model, view_params)
        return await self.__find_all(statement)

    async def find_by_view_params_first(self, model: type(SQLModel), view_params: ViewParams):
        statement = SqlUtils.build_statement_by_view_params(model, view_params)
        return await self.__find_first(statement)

    async def find_by_view_params_count(self, model: type(SQLModel), view_params: ViewParams):
        statement = SqlUtils.build_statement_by_view_params(model, view_params)
        return await self.__find_count(statement)

    async def find_with_filter_first(self, model: type(SQLModel), field, value):
        statement = SqlUtils.build_filter(model, field, value)
        return await self.__find_first(statement)

    async def find_with_filter_all(self, model: type(SQLModel), field, value):
        statement = SqlUtils.build_filter(model, field, value)
        return await self.__find_all(statement)

    async def find_with_filter_count(self, model: type(SQLModel), field, value):
        statement = SqlUtils.build_filter(model, field, value)
        return await self.__find_count(statement.select_from(model))

    async def find_with_sql_api_first(self, statement: Select):
        return await self.__find_first(statement)

    async def find_with_sql_api_all(self, statement: Select):
        return await self.__find_all(statement)

    async def find_with_sql_api_count(self, statement: Select):
        return await self.__find_count(statement)

    async def save(self, model: type(SQLModel)):
        async with self.async_session() as session:
            session.add(model)
            await session.flush()
            session.expunge(model)
            await session.commit()
            return model

    async def save_all(self, models: list[type(SQLModel)]):
        async with self.async_session() as session:
            session.add_all(models)
            await session.flush()
            session.expunge_all()
            await session.commit()
        return models

    async def remove(self, model: type(SQLModel)):
        async with self.async_session() as session:
            await session.delete(model)
            await session.commit()
        return model

    async def remove_all(self, models: list[type(SQLModel)]):
        async with self.async_session() as session:
            for i in models:
                await session.delete(i)
            await session.commit()
        return models
