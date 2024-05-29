from pydantic import BaseModel

from promptadmin.commons.entity.base_entity import BaseEntity


class InputData(BaseModel):
    macro: str
    macro_value: str
    description: str

    default_type: str
    default: str


class Input(BaseEntity, InputData, table=True):
    __tablename__ = 'pa_input'
