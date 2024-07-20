from fastapi import APIRouter

from settings import SETTINGS

router = APIRouter()


@router.get('/get')
async def get():
    return list(SETTINGS.connections.keys())
