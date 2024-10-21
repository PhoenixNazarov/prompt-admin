from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.service.base import BasePermissionService
from promptadmin_server.api.service.status_service import StatusService
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.data.service.status.test_case_service import TestCaseService
from promptadmin_server.data.service.status.test_result_service import TestResultService


class PermissionStatusService(BasePermissionService):
    def __init__(
        self,
        *args,
        status_service: StatusService | None = None,
        test_result_service: TestResultService | None = None,
        test_case_service: TestCaseService | None = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.status_service = status_service or StatusService()
        self.test_result_service = test_result_service or TestResultService()
        self.test_case_service = test_case_service or TestCaseService()

    async def load_test_result(self, id_: int, user_data: UserData):
        test_result = await self.test_result_service.find_by_id(id_)
        if test_result is None:
            raise TypeCheckException()
        await self.require_project_permission(
            test_result.connection_name, "project_status", 1, user_data
        )
        return await self.status_service.load_test_result(id_)

    async def load_test_case(self, id_: int, user_data: UserData):
        test_case = await self.test_case_service.find_by_id(id_)
        if test_case is None:
            raise TypeCheckException()
        test_result = await self.test_result_service.find_by_id(
            test_case.test_result_id
        )
        if test_result is None:
            raise TypeCheckException()
        await self.require_project_permission(
            test_result.connection_name, "project_status", 1, user_data
        )
        return await self.status_service.load_test_case(id_)

    async def load_30(self, project: str, user_data: UserData):
        await self.require_project_permission(project, "project_status", 1, user_data)
        return await self.status_service.load_30(project)

    async def start(self, project: str, user_data: UserData):
        await self.require_project_permission(project, "project_status", 2, user_data)
        return await self.status_service.start(project)
