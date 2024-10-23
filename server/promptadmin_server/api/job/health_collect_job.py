import asyncio
import datetime
import logging

import pytz

from promptadmin_server.commons.dto import (
    ViewParamsBuilder,
    ViewParamsFilter,
    ViewParamsComparison,
)
from promptadmin_server.commons.dto.view_params_comparison import ComparisonType
from promptadmin_server.commons.fastapi.background_task import BackgroundTask
from promptadmin_server.data.entity.healthcheck.health_day import HealthDay
from promptadmin_server.data.entity.healthcheck.health_target import HealthTarget
from promptadmin_server.data.entity.healthcheck.health_unit import HealthUnit
from promptadmin_server.data.service.healthcheck import (
    HealthTargetService,
    HealthUnitService,
    HealthDayService,
)


logger = logging.getLogger(__name__)


class HealthCollectJob(BackgroundTask):
    """
    1. Collect non-collected health_unit to unit days
    2. Remove health_unit older 12 hours

    """

    def __init__(
        self,
        health_target_service: HealthTargetService | None = None,
        health_unit_service: HealthUnitService | None = None,
        health_day_service: HealthDayService | None = None,
    ):
        self.health_target_service = health_target_service or HealthTargetService()
        self.health_unit_service = health_unit_service or HealthUnitService()
        self.health_day_service = health_day_service or HealthDayService()

    async def start(self):
        while True:
            try:
                await self.polling()
            except Exception as e:
                logger.error("Health Job exception", exc_info=e)

    async def stop(self):
        pass

    async def polling(self):
        now_seconds = datetime.datetime.now().second
        await asyncio.sleep(60 - now_seconds)
        while True:
            targets = await self.health_target_service.find_all()
            await asyncio.gather(*[self.process(t) for t in targets])
            await asyncio.sleep(60 * 5)

    async def find_day(self, health_target: HealthTarget, date: datetime.date):
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=HealthDay.date, value=date))
            .filter(
                ViewParamsFilter(
                    field=HealthDay.health_target_id, value=health_target.id
                )
            )
            .build()
        )
        return await self.health_day_service.find_by_view_params_first(view_params)

    async def find_units(self, health_target: HealthTarget):
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=HealthUnit.collect, value=False))
            .filter(
                ViewParamsFilter(
                    field=HealthUnit.health_target_id, value=health_target.id
                )
            )
            .build()
        )
        return await self.health_unit_service.find_by_view_params(view_params)

    async def find_old_units(self, health_target: HealthTarget):
        old_date = datetime.datetime.now(pytz.utc) - datetime.timedelta(hours=12)
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=HealthUnit.collect, value=True))
            .comparison(
                ViewParamsComparison(
                    field=HealthUnit.collect,
                    value=old_date,
                    comparison=ComparisonType.LT,
                )
            )
            .filter(
                ViewParamsFilter(
                    field=HealthUnit.health_target_id, value=health_target.id
                )
            )
            .build()
        )
        return await self.health_unit_service.find_by_view_params(view_params)

    async def process(self, health_target: HealthTarget):
        await self.collect(health_target)

    async def collect(self, health_target: HealthTarget):
        if health_target.id is None:
            return
        health_units = await self.find_units(health_target)
        health_units_by_dates: dict[datetime.date, list[HealthUnit]] = {}
        for unit in health_units:
            date = unit.request_datetime.date()
            group = health_units_by_dates.get(date)
            if group is None:
                new_group: list[HealthUnit] = []
                health_units_by_dates[date] = new_group
            else:
                new_group = group
            new_group.append(unit)

        for date, group in health_units_by_dates.items():
            health_day = await self.find_day(health_target, date)
            provide_health_day = health_day or HealthDay(
                date=date,
                count_response_time=0,
                sum_response_time=0,
                fall_times=0,
                health_target_id=health_target.id,
            )

            for unit in group:
                provide_health_day.count_response_time += 1
                provide_health_day.sum_response_time += unit.response_time
                if not unit.status:
                    provide_health_day.fall_times += 1
                unit.collect = True
            await self.health_day_service.save(provide_health_day)
            await self.health_unit_service.save_all(group)

    async def remove(self, health_target: HealthTarget):
        old_units = await self.find_old_units(health_target)
        await self.health_unit_service.remove_all(old_units)
