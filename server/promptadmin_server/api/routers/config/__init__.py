from fastapi import APIRouter

from .macro import router as macro_router
from .mapping import router as mapping_router
from .output import router as output_router
from .mapping_entity import router as mapping_entity_router
from .input import router as input_router
from .prompt_audit import router as prompt_audit_router
from .account import router as account_router
from .sync_data import router as sync_data_router
from .unit_test import router as unit_test_router

router = APIRouter()

router.include_router(macro_router, prefix='/macro')
router.include_router(mapping_router, prefix='/mapping')
router.include_router(output_router, prefix='/output')
router.include_router(mapping_entity_router, prefix='/mapping_entity')
router.include_router(input_router, prefix='/input')
router.include_router(prompt_audit_router, prefix='/prompt_audit')
router.include_router(account_router, prefix='/account')
router.include_router(sync_data_router, prefix='/sync_data')
router.include_router(unit_test_router, prefix='/unit_test')
