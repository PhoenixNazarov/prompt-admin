import datetime

from promptadmin_server.commons.entity.base_entity import BaseEntity


class HealthUnit(BaseEntity, table=True):
    __tablename__ = "pa_health_unit"

    datetime: datetime.datetime
    status: bool
    response_time: float

    health_target_id: int
    collect: bool = False
