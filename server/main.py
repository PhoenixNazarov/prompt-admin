import asyncio

from promptadmin_server.api.app import app
import uvicorn

from promptadmin_server.api.job.health_collect_job import HealthCollectJob
from promptadmin_server.api.job.health_request_job import HealthRequestJob
from settings import SETTINGS


# async def main():
#     await asyncio.gather(HealthRequestJob().start(), HealthCollectJob().start())


# asyncio.run(main())

if __name__ == "__main__":
    uvicorn.run(app, host=SETTINGS.host, port=SETTINGS.port)  # , log_config=None
