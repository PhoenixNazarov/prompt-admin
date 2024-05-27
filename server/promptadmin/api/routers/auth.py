from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin.api.service.user_data import UserData
from promptadmin.api.service.user_manager_service import UserManagerService

um_service = UserManagerService()

router = APIRouter()


class LoginDto(BaseModel):
    login: str
    password: str


@router.get('/me')
async def me(request: Request):
    user_data: UserData = request.scope['user_data']
    return user_data.account


@router.post('/login')
async def login_view(request: Request, login_dto: LoginDto):
    user_data: UserData = request.scope['user_data']
    return await um_service.authorize(login_dto.login, login_dto.password, user_data)
