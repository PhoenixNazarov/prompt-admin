from fastapi import APIRouter

from .main import router as main_router

from .blog_group import router as blog_group_router
from .blog_post import router as blog_post_router
from .status import router as status_router

router = APIRouter()

router.include_router(main_router, prefix='/main')
router.include_router(blog_group_router, prefix='/blog_group')
router.include_router(blog_post_router, prefix='/blog_post')
router.include_router(status_router, prefix='/status')
