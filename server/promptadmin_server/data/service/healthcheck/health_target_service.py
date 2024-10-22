from promptadmin_server.commons.service import AsyncBaseService
from promptadmin_server.data.entity.healthcheck.health_target import HealthTarget
from promptadmin_server.data.repository.healthcheck.health_target_repository import (
    HealthTargetRepository,
)


class HealthTargetService(AsyncBaseService[HealthTarget]):
    def __init__(self, repository: HealthTargetRepository | None = None):
        super().__init__(repository or HealthTargetRepository())
