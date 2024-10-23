import datetime

from promptadmin_server.commons.dto import (
    ViewParamsBuilder,
    ViewParamsFilter,
    ViewParamsComparison,
)
from promptadmin_server.commons.dto.view_params_comparison import ComparisonType
from promptadmin_server.data.entity.healthcheck.health_day import HealthDay
from promptadmin_server.data.entity.healthcheck.health_target import HealthTarget
from promptadmin_server.data.entity.healthcheck.health_unit import HealthUnit
from promptadmin_server.data.service.healthcheck import (
    HealthDayService,
    HealthUnitService,
    HealthTargetService,
)


class HealthCheckService:
    def __init__(
        self,
        health_target_service: HealthTargetService | None = None,
        health_unit_service: HealthUnitService | None = None,
        health_day_service: HealthDayService | None = None,
    ):
        self.health_target_service = health_target_service or HealthTargetService()
        self.health_unit_service = health_unit_service or HealthUnitService()
        self.health_day_service = health_day_service or HealthDayService()

    async def load_all_target(self):
        return await self.health_target_service.find_all()

    async def load_last_days(self, targets_ids: list[int], days: int = 90):
        old_date = datetime.datetime.now() - datetime.timedelta(days=days)
        view_params = (
            ViewParamsBuilder()
            .comparison(
                ViewParamsComparison(
                    field=HealthDay.date,
                    value=old_date,
                    comparison=ComparisonType.GE,
                )
            )
            .filter(
                ViewParamsFilter(field=HealthDay.health_target_id, value=targets_ids)
            )
            .build()
        )
        return await self.health_day_service.find_by_view_params(view_params)

    async def load_units(self, target_id: int) -> list[tuple[float, bool, float]]:
        old_date = datetime.datetime.now() - datetime.timedelta(hours=12)
        view_params = (
            ViewParamsBuilder()
            .comparison(
                ViewParamsComparison(
                    field=HealthUnit.request_datetime,
                    value=old_date,
                    comparison=ComparisonType.GT,
                )
            )
            .filter(
                ViewParamsFilter(field=HealthUnit.health_target_id, value=target_id)
            )
            .build()
        )
        return [
            (i.response_time, i.status, i.request_datetime.timestamp())
            for i in await self.health_unit_service.find_by_view_params(view_params)
        ]

    async def create_target(self, url: str, label: str) -> HealthTarget:
        pass
