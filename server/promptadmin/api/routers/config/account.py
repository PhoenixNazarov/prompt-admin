from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin.data.service.account_service import AccountService

router = APIRouter()

account_service = AccountService()


class AccountData(BaseModel):
    id: int
    time_create: datetime
    login: str


@router.get('/get/all')
async def get():
    accounts = await account_service.find_all()

    return [
        AccountData(id=acc.id, time_create=acc.time_create, login=acc.login) for acc in accounts
    ]
