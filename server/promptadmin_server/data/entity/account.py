from promptadmin_server.commons.entity import BaseEntity


class Account(BaseEntity, table=True):
    __tablename__ = 'pa_account'

    login: str
    password: str
