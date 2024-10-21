from promptadmin_server.commons.entity import BaseEntity


class Permission(BaseEntity, table=True):
    __tablename__ = 'pa_permission'

    account_id: int

    key: str
    value: int
    project: str | None
