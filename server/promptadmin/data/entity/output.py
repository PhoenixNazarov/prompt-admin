from pydantic import BaseModel

from promptadmin.commons.entity.base_entity import BaseEntity


class OutputData(BaseModel):
    output: str


class Output(BaseEntity, OutputData, table=True):
    __tablename__ = 'pa_output'
