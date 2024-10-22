from promptadmin_server.commons.service import AsyncBaseService
from promptadmin_server.data.entity.healthcheck.health_unit import HealthUnit
from promptadmin_server.data.repository.healthcheck.health_unit_repository import (
    HealthUnitRepository,
)


class HealthUnitService(AsyncBaseService[HealthUnit]):
    def __init__(self, repository: HealthUnitRepository | None = None):
        super().__init__(repository or HealthUnitRepository())
