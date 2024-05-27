from typing import Optional

from pydantic import BaseModel

from promptadmin.data.entity.access_token import AccessToken
from promptadmin.data.entity.account import Account


class UserData(BaseModel):
    access_token: AccessToken
    account: Optional[Account] = None

    @property
    def is_authorize(self):
        return self.account is not None

    @property
    def is_anonim(self):
        return self.account is None



