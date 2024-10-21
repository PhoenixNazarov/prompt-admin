from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.api.service.user_manager_service import UserManagerService
from promptadmin_server.api.service.ws_manager import WsManager
from promptadmin_server.data.service.access_token_service import AccessTokenService

um_service = UserManagerService()
access_token_service = AccessTokenService()
ws_manager = WsManager()

router = APIRouter()


class LoginDto(BaseModel):
    login: str
    password: str


class WsTokenResponse(BaseModel):
    token: str


@router.get("/me")
async def me(request: Request):
    user_data: UserData = request.scope["user_data"]
    if user_data.account is None:
        return None
    return {**user_data.account.model_dump(), "password": None}


@router.post("/login")
async def login_view(request: Request, login_dto: LoginDto):
    user_data: UserData = request.scope["user_data"]
    return await um_service.authorize(login_dto.login, login_dto.password, user_data)


@router.get("/logout")
async def logout(user_data: UserDependsAnnotated):
    if user_data.access_token.id is None:
        raise TypeCheckException()
    access_token = await access_token_service.find_by_id(user_data.access_token.id)
    if access_token:
        await access_token_service.remove(access_token)


@router.get("/ws/token")
async def ws_token(user_data: UserDependsAnnotated):
    token = await ws_manager.generate_auth_token(user_data)
    return WsTokenResponse(token=token)
