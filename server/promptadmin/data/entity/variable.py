from pydantic import BaseModel

from promptadmin.commons.entity.base_entity import BaseEntity


class VariableData(BaseModel):
    name: str
    description: str
    value: str
    template: bool = False


class Variable(BaseEntity, VariableData, table=True):
    __tablename__ = 'pa_variable'
