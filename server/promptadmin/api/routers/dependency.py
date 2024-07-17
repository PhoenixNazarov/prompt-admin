from typing import Annotated

from fastapi import Request, Depends

from promptadmin.api.service.user_data import UserData


def get_user_dependency(request: Request):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    return user_data


UserDepends = Depends(get_user_dependency)
UserDependsAnnotated = Annotated[UserData, UserDepends]
