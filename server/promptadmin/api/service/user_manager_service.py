import logging

from promptadmin.api.service.user_data import UserData
from promptadmin.data.entity.access_token import AccessToken
from promptadmin.data.entity.account import Account
from promptadmin.data.service.access_token_service import AccessTokenService
from promptadmin.data.service.account_service import AccountService

logger = logging.getLogger(__name__)


def secure(password):
    return password


class UserManagerService:
    def __init__(self,
                 access_token_service: AccessTokenService = None,
                 account_service: AccountService = None,
                 ):
        self.access_token_service = access_token_service or AccessTokenService()
        self.account_service = account_service or AccountService()

    async def __generate_token(self) -> UserData:
        access_token = AccessToken()
        access_token = await self.access_token_service.save(access_token)
        return UserData(
            access_token=access_token
        )

    async def load_user_data(self, token: str) -> UserData:
        if token is None:
            return await self.__generate_token()
        access_token = await self.access_token_service.find_by_key(AccessToken.token, token)
        if len(access_token) == 0:
            return await self.__generate_token()
        access_token = access_token[0]
        ud = UserData(
            access_token=access_token,
        )
        if access_token.account_id:
            account = await self.account_service.find_by_id(access_token.account_id)
            ud.account = account
        return ud

    async def authorize(self, login: str, password: str, user_data: UserData) -> Account:
        if user_data.account:
            raise ValueError('You already authorize')

        account = await self.account_service.find_by_key_first(Account.login, login)
        if account is None:
            account = await self.account_service.find_by_key_first(Account.email, login)
            if account is None:
                raise ValueError('Account not find')
        if account.password and account.password != secure(password):
            raise ValueError('Password incorrect')

        access_token = await self.access_token_service.find_by_id(user_data.access_token.id)
        access_token.account_id = account.id
        await self.access_token_service.save(access_token)

        user_data.account = account
        return account
