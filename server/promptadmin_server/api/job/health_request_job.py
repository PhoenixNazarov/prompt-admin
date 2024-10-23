import asyncio
import datetime
import pytz
import logging
import time

import httpx

from promptadmin_server.commons.fastapi.background_task import BackgroundTask
from promptadmin_server.data.entity.healthcheck.health_target import HealthTarget
from promptadmin_server.data.entity.healthcheck.health_unit import HealthUnit
from promptadmin_server.data.service.healthcheck import (
    HealthTargetService,
    HealthUnitService,
)

logger = logging.getLogger(__name__)


class HealthRequestJob(BackgroundTask):
    def __init__(
        self,
        health_target_service: HealthTargetService | None = None,
        health_unit_service: HealthUnitService | None = None,
    ):
        self.health_target_service = health_target_service or HealthTargetService()
        self.health_unit_service = health_unit_service or HealthUnitService()

    async def start(self):
        while True:
            try:
                await self.polling()
            except Exception as e:
                logger.error("Health Job exception", exc_info=e)

    async def stop(self):
        pass

    async def polling(self):
        while True:
            targets = await self.health_target_service.find_all()
            now_seconds = datetime.datetime.now().second
            await asyncio.sleep(60 - now_seconds)
            await asyncio.gather(*[self.status_target(t) for t in targets])

    async def status_target(self, target: HealthTarget):
        t_start = time.time()
        status = False
        for i in range(3):
            t_start = time.time()
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(target.url)
                status = r.is_success
                break
            except Exception as e:
                status = False
                continue

        health_unit = HealthUnit(
            request_datetime=datetime.datetime.now(pytz.utc),
            status=status,
            response_time=time.time() - t_start,
            health_target_id=target.id,
        )

        return await self.health_unit_service.save(health_unit)
