import datetime

from fastapi import APIRouter

from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsComparison, ViewParamsFilter
from promptadmin_server.commons.dto.view_params_comparison import ComparisonType
from promptadmin_server.data.entity.status.test_result import TestResult
from promptadmin_server.data.service.status.test_result_service import TestResultService

router = APIRouter()

service = TestResultService()


@router.get('/load_30/{project}')
async def load_30(project: str):
    now_date = datetime.datetime.now()
    ago_date = now_date - datetime.timedelta(days=30, hours=now_date.hour, minutes=now_date.minute,
                                             seconds=now_date.second)

    view_params = (
        ViewParamsBuilder()
        .comparison(
            ViewParamsComparison(field=TestResult.created, value=ago_date.timestamp(), comparison=ComparisonType.GE)
        )
        .filter(
            ViewParamsFilter(field=TestResult.connection_name, value=project)
        )
        .build()
    )

    return await service.find_by_view_params(view_params)
