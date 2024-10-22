from promptadmin_server.api.exceptions_handlers import bind_exception_handlers
from promptadmin_server.api.job.health_collect_job import HealthCollectJob
from promptadmin_server.api.job.health_request_job import HealthRequestJob
from promptadmin_server.api.job.monitor_status_job import MonitorStatusJob
from promptadmin_server.api.job.sync_job import SyncJob
from promptadmin_server.api.job.unit_test_job import UnitTestJob
from promptadmin_server.api.routers import router
from promptadmin_server.api.session_middleware import SessionMiddleware
from promptadmin_server.commons.fastapi.app import create_app

jobs = [
    UnitTestJob(),
    SyncJob(),
    MonitorStatusJob(),
    HealthRequestJob(),
    HealthCollectJob(),
]

app = create_app(
    background_tasks=jobs,
    redoc_url="/api/redoc",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(SessionMiddleware, secret_key="asdasdasdasd")

app.include_router(router)

bind_exception_handlers(app)
