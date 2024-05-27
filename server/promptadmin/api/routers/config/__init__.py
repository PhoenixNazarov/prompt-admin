from fastapi import APIRouter

from .macro import router as macro_router
from .mapping import router as mapping_router
from .variable import router as variable_router
from .output import router as output_router
from .mapping_entity import router as mapping_entity_router

router = APIRouter()

router.include_router(macro_router, prefix='/macro')
router.include_router(mapping_router, prefix='/mapping')
router.include_router(variable_router, prefix='/variable')
router.include_router(output_router, prefix='/output')
router.include_router(mapping_entity_router, prefix='/mapping_entity')
