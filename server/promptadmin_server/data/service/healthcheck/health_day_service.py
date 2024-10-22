from promptadmin_server.commons.service import AsyncBaseService
from promptadmin_server.data.entity.healthcheck.health_day import HealthDay
from promptadmin_server.data.repository.healthcheck.health_day_repository import (
    HealthDayRepository,
)


class HealthDayService(AsyncBaseService[HealthDay]):
    def __init__(self, repository: HealthDayRepository | None = None):
        super().__init__(repository or HealthDayRepository())
