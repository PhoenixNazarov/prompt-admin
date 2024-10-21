import datetime

from promptadmin_server.api.service.sync.test_monitoring_service import (
    TestMonitoringService,
)
from promptadmin_server.commons.dto import (
    ViewParamsBuilder,
    ViewParamsComparison,
    ViewParamsFilter,
)
from promptadmin_server.commons.dto.view_params_comparison import ComparisonType
from promptadmin_server.data.entity.status.test_case import TestCase
from promptadmin_server.data.entity.status.test_case_info import TestCaseInfo
from promptadmin_server.data.entity.status.test_result import TestResult
from promptadmin_server.data.service.status.test_case_info_service import (
    TestCaseInfoService,
)
from promptadmin_server.data.service.status.test_case_service import TestCaseService
from promptadmin_server.data.service.status.test_result_service import TestResultService


class StatusService:
    def __init__(
        self,
        test_case_service: TestCaseService | None = None,
        test_case_info_service: TestCaseInfoService | None = None,
        test_result_service: TestResultService | None = None,
        test_monitoring_service: TestMonitoringService | None = None,
    ):
        self.test_case_service = test_case_service or TestCaseService()
        self.test_case_info_service = test_case_info_service or TestCaseInfoService()
        self.test_result_service = test_result_service or TestResultService()
        self.test_monitoring_service = (
            test_monitoring_service or TestMonitoringService()
        )

    async def load_test_result(self, id_: int):
        return await self.test_case_service.find_by_key(TestCase.test_result_id, id_)

    async def load_test_case(self, id_: int):
        return self.test_case_info_service.find_by_key_first(
            TestCaseInfo.test_case_id, id_
        )

    async def load_30(self, project: str):
        now_date = datetime.datetime.now()
        ago_date = now_date - datetime.timedelta(
            days=30,
            hours=now_date.hour,
            minutes=now_date.minute,
            seconds=now_date.second,
        )

        view_params = (
            ViewParamsBuilder()
            .comparison(
                ViewParamsComparison(
                    field=TestResult.created,
                    value=ago_date.timestamp(),
                    comparison=ComparisonType.GE,
                )
            )
            .filter(ViewParamsFilter(field=TestResult.connection_name, value=project))
            .build()
        )

        return await self.test_result_service.find_by_view_params(view_params)

    async def start(self, project: str):
        return await self.test_monitoring_service.start_endpoint(project)
