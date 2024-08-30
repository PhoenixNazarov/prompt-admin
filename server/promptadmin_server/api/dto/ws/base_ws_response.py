from pydantic import BaseModel


class BaseWsResponse(BaseModel):
    type: str
