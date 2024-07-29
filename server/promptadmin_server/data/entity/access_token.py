import datetime
import random
import string
from typing import Optional

from sqlmodel import Field

from promptadmin_server.commons.entity import BaseEntity


def get_random_string(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))  # noqa "S311"
    return result_str


class AccessToken(BaseEntity, table=True):
    __tablename__ = 'pa_access_token'

    token: str = Field(default_factory=lambda: get_random_string(45))

    account_id: Optional[int] = None

    time_active: datetime.datetime = Field(default_factory=datetime.datetime.now)
