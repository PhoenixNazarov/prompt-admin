from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.service.sync.client_service import ClientService

router = APIRouter()


class BaseRequest(BaseModel):
    project: str
    url: str


class GetRequest(BaseRequest):
    pass


class PostRequest(BaseRequest):
    data: dict[str, Any] | None = None


client_service = ClientService()


@router.post('/get')
async def get(get_request: GetRequest):
    return (await client_service.get_request(get_request.project, get_request.url)).status_code


@router.post('/post')
async def post(post_request: PostRequest):
    return (await client_service.post_request(post_request.project, post_request.url, post_request.data)).status_code
