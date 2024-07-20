from pydantic import BaseModel

from promptadmin.commons.entity.base_entity import BaseEntity


class MappingData(BaseModel):
    table: str
    field: str

    description: str
    field_name: str | None = None
    # field_order: str | None = None
    # desc: bool = False
    connection_name: str


class Mapping(BaseEntity, MappingData, table=True):
    __tablename__ = 'pa_mapping'
