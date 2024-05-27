from typing import Optional

from ..entity.account import Account
from ..repository.account_repository import AccountRepository
from ...commons.service import AsyncBaseService


class AccountService(AsyncBaseService[Account]):
    def __init__(self, repository: AccountRepository = None):
        super().__init__(repository or AccountRepository())

    async def find_by_login(self, login: str) -> Optional[Account]:
        return await self.find_by_key_first(Account.login, login)
