from promptadmin_server.api.service.base import BasePermissionService
from promptadmin_server.api.service.healthcheck_service import HealthCheckService
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.data.entity.healthcheck.health_target import HealthTarget


class PermissionHealthCheckService(BasePermissionService):
    def __init__(
        self,
        *args,
        healthcheck_service: HealthCheckService | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.healthcheck_service = healthcheck_service or HealthCheckService()

    async def load_all_target(self, user_data: UserData):
        await self.require_permission("healthcheck", 1, user_data)
        return await self.healthcheck_service.load_all_target()

    async def load_last_days(
        self, targets_ids: list[int], user_data: UserData, days: int = 90
    ):
        await self.require_permission("healthcheck", 1, user_data)
        return await self.healthcheck_service.load_last_days(targets_ids, days)

    async def load_units(self, target_id: int, user_data: UserData):
        await self.require_permission("healthcheck", 1, user_data)
        return await self.healthcheck_service.load_units(target_id)

    async def create_target(
        self, url: str, label: str, user_data: UserData
    ) -> HealthTarget:
        await self.require_permission("healthcheck", 2, user_data)
        return await self.healthcheck_service.create_target(url, label)
