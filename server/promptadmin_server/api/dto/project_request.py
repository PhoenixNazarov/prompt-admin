from pydantic import BaseModel


class ProjectRequest(BaseModel):
    project: str
