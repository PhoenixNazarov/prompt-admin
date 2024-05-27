from pydantic import BaseModel

from promptadmin.commons.entity.base_entity import BaseEntity


class MappingEntityData(BaseModel):
    connection_name: str | None
    table: str | None
    field: str | None
    name: str | None

    mapping_id: int | None

    entity: str
    entity_id: int


class MappingEntity(BaseEntity, MappingEntityData, table=True):
    __tablename__ = 'pa_mapping_entity'
