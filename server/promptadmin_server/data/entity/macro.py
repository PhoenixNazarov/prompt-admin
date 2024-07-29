from pydantic import BaseModel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class MacroData(BaseModel):
    macro: str
    macro_value: str
    description: str


class Macro(BaseEntity, MacroData, table=True):
    __tablename__ = 'pa_macro'
