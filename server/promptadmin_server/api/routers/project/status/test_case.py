from fastapi import APIRouter

from promptadmin_server.data.entity.status.test_case import TestCase
from promptadmin_server.data.service.status.test_case_service import TestCaseService

router = APIRouter()

service = TestCaseService()


@router.get('/load/test_result/{_id}')
async def load_test_result(_id: int):
    return await service.find_by_key(TestCase.test_result_id, _id)
