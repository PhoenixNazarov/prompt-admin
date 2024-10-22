from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.healthcheck.health_target import HealthTarget


class HealthTargetRepository(AsyncBaseRepository[HealthTarget]):
    def __init__(self):
        super().__init__(HealthTarget)
