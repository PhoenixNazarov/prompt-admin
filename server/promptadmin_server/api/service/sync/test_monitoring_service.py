import json
import logging

from promptadmin_server.api.service.sync.client_service import ClientService
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.data.entity.status.test_case import TestCase
from promptadmin_server.data.entity.status.test_case_info import TestCaseInfo
from promptadmin_server.data.entity.status.test_result import TestResult
from promptadmin_server.data.entity.status.test_result_raw import TestResultRaw
from promptadmin_server.data.service.status.test_case_info_service import TestCaseInfoService
from promptadmin_server.data.service.status.test_case_service import TestCaseService
from promptadmin_server.data.service.status.test_result_raw_service import TestResultRawService
from promptadmin_server.data.service.status.test_result_service import TestResultService

logger = logging.getLogger(__name__)


class TestMonitoringService:
    def __init__(
            self,
            test_result_service: TestResultService = None,
            test_result_raw_service: TestResultRawService = None,
            test_case_service: TestCaseService = None,
            test_case_info_service: TestCaseInfoService = None,
            client_service: ClientService = None
    ):
        self.test_result_service = test_result_service or TestResultService()
        self.test_result_raw_service = test_result_raw_service or TestResultRawService()
        self.test_case_service = test_case_service or TestCaseService()
        self.test_case_info_service = test_case_info_service or TestCaseInfoService()
        self.client_service = client_service or ClientService()

    async def sync_endpoint(self, connection: str):
        try:
            await self.sync(connection)
        except Exception as e:
            logger.error('Sync monitor status exception', exc_info=e)

    async def sync(self, connection: str):
        response_json_list = await self.client_service.request_json(connection, '/status/test_list')
        if response_json_list == {'detail': 'Not Found'}:
            return
        for k, created in response_json_list.items():
            if await self.find_already(connection, created):
                continue
            # try:
            response_json_resport = await self.client_service.request_json(connection, f'/status/test/{k}')
            report = response_json_resport.get('test_case')
            if report:
                await self.load_report(report, connection)
            # finally:
            #     pass

    async def find_already(self, connection_name: str, created: float):
        print(connection_name, created)
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=TestResult.connection_name, value=connection_name))
            .filter(ViewParamsFilter(field=TestResult.created, value=created))
            .build()
        )
        return await self.test_result_service.find_by_view_params_first(view_params)

    async def load_report(self, report: dict, connection: str):
        print(report)
        test_result = TestResult(
            connection_name=connection,
            created=report['created'],
            duration=report['duration'],
            passed=report['summary'].get('passed', 0),
            skipped=report['summary'].get('skipped', 0),
            error=report['summary'].get('error', 0),
            failed=report['summary'].get('failed', 0),
            total=report['summary'].get('total', 0),
            collected=report['summary'].get('collected', 0)
        )
        if await self.find_already(test_result.connection_name, test_result.created):
            return

        test_result = await self.test_result_service.save(test_result)

        for t in report['tests']:
            await self.load_testcase(t, test_result.id)

        await self.test_result_raw_service.save(TestResultRaw(
            test_result_id=test_result.id,
            raw_file=json.dumps(report)
        ))

    async def load_testcase(self, raw_testcase: dict, test_result_id: int):
        test_case = TestCase(
            test_result_id=test_result_id,
            nodeid=raw_testcase['nodeid'],
            lineno=raw_testcase['lineno'],
            outcome=raw_testcase['outcome'],
            metadata_url=raw_testcase.get('metadata', {}).get('url'),
            metadata_scenario=raw_testcase.get('metadata', {}).get('scenario'),
            setup_duration=raw_testcase['setup']['duration'],
            setup_outcome=raw_testcase['setup']['outcome'],
            call_duration=raw_testcase.get('call', {}).get('duration'),
            call_outcome=raw_testcase.get('call', {}).get('outcome'),
            teardown_duration=raw_testcase['teardown']['duration'],
            teardown_outcome=raw_testcase['teardown']['outcome'],
        )
        test_case = await self.test_case_service.save(test_case)
        await self.test_case_info_service.save(
            TestCaseInfo(
                test_case_id=test_case.id,
                setup_longrepr=raw_testcase['setup'].get('longrepr'),
                call_crash_path=raw_testcase.get('call', {}).get('crash', {}).get('path'),
                call_crash_lineno=raw_testcase.get('call', {}).get('crash', {}).get('lineno'),
                call_crash_message=raw_testcase.get('call', {}).get('crash', {}).get('message'),
                request=json.dumps(raw_testcase.get('metadata', {}).get('request', {}))[:9999],
                response=json.dumps(raw_testcase.get('metadata', {}).get('response', {}))[:9999]
            )
        )
