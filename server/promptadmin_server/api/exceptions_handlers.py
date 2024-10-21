import logging

from asyncpg import ForeignKeyViolationError
from fastapi import FastAPI, Request

from promptadmin_server.api.exceptions import SQLDBException

logger = logging.getLogger(__name__)


async def log_request(request: Request, exc: Exception):
    request_json = ""
    try:
        request_json = await request.json()
        request_json = str(request_json)
    except Exception:
        request_json = ""

    logger.error(
        "ForeignKeyViolationError",
        exc_info=exc,
        extra={
            "request-url": request.url,
            "request-query-params": request.query_params,
            "request-data": request_json,
        },
    )


def bind_exception_handlers(app: FastAPI):

    @app.exception_handler(ForeignKeyViolationError)
    async def unicorn_exception_handler(
        request: Request, exc: ForeignKeyViolationError
    ):
        await log_request(request, exc)
        raise SQLDBException(headers={"Error-Message": exc.detail})
