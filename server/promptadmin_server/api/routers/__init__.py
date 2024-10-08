from fastapi import APIRouter

from promptadmin_server.api.routers.prompts import router as prompts_router
from .config import router as config_router
from .auth import router as auth_router
from .dependency import UserDepends
from .format import router as format_router
from .project import router as project_router
from .vars import router as vars_router
from .ws import router as ws_router

router = APIRouter(prefix='/api')

protect_router = APIRouter(dependencies=[UserDepends])

router.include_router(auth_router, prefix='/auth')

protect_router.include_router(prompts_router, prefix='/prompts')
protect_router.include_router(config_router, prefix='/config')
protect_router.include_router(format_router, prefix='/format')
protect_router.include_router(project_router, prefix='/project')
protect_router.include_router(vars_router, prefix='/vars')

router.include_router(protect_router)
router.include_router(ws_router, prefix='/ws')
