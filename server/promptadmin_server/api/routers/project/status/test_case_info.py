from fastapi import APIRouter

from promptadmin_server.data.entity.status.test_case_info import TestCaseInfo
from promptadmin_server.data.service.status.test_case_info_service import TestCaseInfoService

router = APIRouter()

service = TestCaseInfoService()


@router.get('/load/test_case/{_id}')
async def load_test_case(_id: int):
    return await service.find_by_key_first(TestCaseInfo.test_case_id, _id)
