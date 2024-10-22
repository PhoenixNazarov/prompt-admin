import datetime

from promptadmin_server.commons.entity.base_entity import BaseEntity


class HealthDay(BaseEntity, table=True):
    __tablename__ = "pa_health_day"

    date: datetime.date
    count_response_time: int
    sum_response_time: float
    fall_times: int

    health_target_id: int
