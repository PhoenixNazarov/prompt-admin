from fastapi import APIRouter

from .test_result import router as test_result_router
from .test_case import router as test_case_router
from .test_case_info import router as test_case_info_router

router = APIRouter()

router.include_router(test_result_router, prefix='/test_result')
router.include_router(test_case_router, prefix='/test_case')
router.include_router(test_case_info_router, prefix='/test_case_info')
