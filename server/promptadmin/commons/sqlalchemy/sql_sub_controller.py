from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Select
from sqlmodel import SQLModel, create_engine, func

from ..dto.view_params import ViewParams

from .sql_utils import SqlUtils

from settings import SETTINGS


class SqlSubController:
    def __init__(self, dsn: str):
        self.engine = create_engine(dsn, connect_args={'application_name': SETTINGS.app})
        self.session = sessionmaker(bind=self.engine)

    def __find_all(self, statement):
        with self.session() as session:
            rows = session.execute(statement).all()
            return SqlUtils.unpack(rows)

    def __find_first(self, statement):
        with self.session() as session:
            model = session.execute(statement).first()
            if model:
                return model[0]
            return

    def __find_count(self, statement):
        statement = select(func.count()).select_from(statement)
        with self.session() as session:
            return session.execute(statement).scalar()

    def execute(self, statement, params):
        with self.engine.begin() as conn:
            return conn.execute(statement, params)

    def find_by_view_params_all(self, model: type(SQLModel), view_params: ViewParams):
        statement = SqlUtils.build_statement_by_view_params(model, view_params)
        return self.__find_all(statement)

    def find_by_view_params_first(self, model: type(SQLModel), view_params: ViewParams):
        statement = SqlUtils.build_statement_by_view_params(model, view_params)
        return self.__find_first(statement)

    def find_by_view_params_count(self, model: type(SQLModel), view_params: ViewParams):
        statement = SqlUtils.build_statement_by_view_params(model, view_params)
        return self.__find_count(statement)

    def find_with_filter_first(self, model: type(SQLModel), field, value):
        statement = SqlUtils.build_filter(model, field, value)
        return self.__find_first(statement)

    def find_with_filter_all(self, model: type(SQLModel), field, value):
        statement = SqlUtils.build_filter(model, field, value)
        return self.__find_all(statement)

    def find_with_filter_count(self, model: type(SQLModel), field, value):
        statement = SqlUtils.build_filter(model, field, value)
        return self.__find_count(statement.select_from(model))

    def find_with_sql_api_first(self, statement: Select):
        return self.__find_first(statement)

    def find_with_sql_api_all(self, statement: Select):
        return self.__find_all(statement)

    def find_with_sql_api_count(self, statement: Select):
        return self.__find_count(statement)

    def save(self, model: type(SQLModel)):
        with self.session() as session:
            session.add(model)
            session.flush()
            session.expunge(model)
            session.commit()
            return model

    def save_all(self, models: list[type(SQLModel)]):
        with self.session() as session:
            session.add_all(models)
            session.flush()
            session.expunge_all()
            session.commit()
        return models

    def remove(self, model: type(SQLModel)):
        with self.session() as session:
            session.delete(model)
            session.commit()
        return model

    def remove_all(self, models: list[type(SQLModel)]):
        with self.session() as session:
            for i in models:
                session.delete(i)
            session.commit()
        return models
