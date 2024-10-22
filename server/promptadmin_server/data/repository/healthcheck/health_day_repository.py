from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.healthcheck.health_day import HealthDay


class HealthDayRepository(AsyncBaseRepository[HealthDay]):
    def __init__(self):
        super().__init__(HealthDay)
