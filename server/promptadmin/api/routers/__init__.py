from fastapi import APIRouter

from promptadmin.api.routers.prompts import router as prompts_router
from .config import router as config_router
from .auth import router as auth_router

router = APIRouter(prefix='/api')

router.include_router(prompts_router, prefix='/prompts')
router.include_router(config_router, prefix='/config')
router.include_router(auth_router, prefix='/auth')
