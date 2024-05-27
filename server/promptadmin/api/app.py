from promptadmin.api.routers import router
from promptadmin.api.session_middleware import SessionMiddleware
from promptadmin.commons.fastapi.app import create_app

app = create_app(
    redoc_url='/api/redoc',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
)

app.add_middleware(SessionMiddleware,
                   secret_key='asdasdasdasd')

app.include_router(router)
