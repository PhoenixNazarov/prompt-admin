from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.healthcheck.health_unit import HealthUnit


class HealthUnitRepository(AsyncBaseRepository[HealthUnit]):
    def __init__(self):
        super().__init__(HealthUnit)
