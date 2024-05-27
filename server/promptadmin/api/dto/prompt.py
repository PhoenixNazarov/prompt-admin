from pydantic import BaseModel


class Prompt(BaseModel):
    mapping_id: int
    table: str
    field: str
    id: int
    value: str
    name: str | None
