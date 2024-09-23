from promptadmin_server.commons.entity import BaseEntity
from sqlmodel import JSON, Field, Column


class TableSchema(BaseEntity, table=True):
    __tablename__ = 'pa_table_schema'

    project: str
    table_schema: dict = Field(default_factory=dict, sa_column=Column(JSON))
