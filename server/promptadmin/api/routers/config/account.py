from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin.api.service.user_data import UserData
from promptadmin.data.service.account_service import AccountService

router = APIRouter()

account_service = AccountService()


class AccountData(BaseModel):
    id: int
    time_create: datetime
    login: str


@router.get('/get/all')
async def get(request: Request):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    accounts = await account_service.find_all()

    return [
        AccountData(id=acc.id, time_create=acc.time_create, login=acc.login) for acc in accounts
    ]
