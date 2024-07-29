import logging

from promptadmin_server.commons.error.base_error import BaseError

logger = logging.getLogger(__name__)


def error_handler(app):
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    app: FastAPI

    @app.exception_handler(BaseError)
    async def unicorn_exception_handler(request: Request, exc: BaseError):
        request_json = ''
        try:
            request_json = await request.json()
            request_json = str(request_json)
        except Exception:
            request_json = ''

        logger.error('BaseError', exc_info=exc,
                     extra={
                         'request-url': request.url,
                         'request-query-params': request.query_params,
                         'request-data': request_json
                     }
                     )
        return JSONResponse(
            status_code=500,
            content={
                'message': f'Oops! {exc.code()} did something. {exc.message}',
                'error': str(exc),
                'description': exc.description()
            },
        )
