from fastapi import APIRouter

from .list import router as list_router
from .item import router as item_router
from .main import router as main_router
from .execute import router as execute_router

router = APIRouter()

router.include_router(list_router, prefix='/list')
router.include_router(item_router, prefix='/item')
router.include_router(main_router, prefix='/main')
router.include_router(execute_router, prefix='/execute')
