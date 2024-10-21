from typing import Any

from pydantic import BaseModel

from promptadmin_server.api.dto.project_request import ProjectRequest


class ProjectTableRequest(ProjectRequest):
    table: str


class LoadItemRequest(ProjectTableRequest):
    id: int


class TypeColumn(BaseModel):
    type: str
    value: Any


class Column(BaseModel):
    key: str
    value: TypeColumn | Any


class SaveItemRequest(ProjectTableRequest):
    id: int | None = None
    columns: list[Column]


class SortByColumn(BaseModel):
    key: str
    order: str


class FilterColumn(BaseModel):
    key: str
    value: str | int | bool | None = None
    operator: str


class JoinColumn(BaseModel):
    table: str
    pseudo: str | None = None
    condition: str
