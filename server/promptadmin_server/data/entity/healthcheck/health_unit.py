import datetime

import sqlmodel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class HealthUnit(BaseEntity, table=True):
    __tablename__ = "pa_health_unit"

    request_datetime: datetime.datetime = sqlmodel.Field(
        sa_column=sqlmodel.Column(sqlmodel.DateTime(timezone=True), nullable=False),
    )
    status: bool
    response_time: float

    health_target_id: int
    collect: bool = False
