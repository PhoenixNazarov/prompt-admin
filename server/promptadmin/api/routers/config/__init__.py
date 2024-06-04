from fastapi import APIRouter

from .macro import router as macro_router
from .mapping import router as mapping_router
from .variable import router as variable_router
from .output import router as output_router
from .mapping_entity import router as mapping_entity_router
from .input import router as input_router
from .prompt_audit import router as prompt_audit_router
from .account import router as account_router

router = APIRouter()

router.include_router(macro_router, prefix='/macro')
router.include_router(mapping_router, prefix='/mapping')
router.include_router(variable_router, prefix='/variable')
router.include_router(output_router, prefix='/output')
router.include_router(mapping_entity_router, prefix='/mapping_entity')
router.include_router(input_router, prefix='/input')
router.include_router(prompt_audit_router, prefix='/prompt_audit')
router.include_router(account_router, prefix='/account')
