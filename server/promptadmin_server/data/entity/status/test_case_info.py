from pydantic import BaseModel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class TestCaseInfoData(BaseModel):
    test_case_id: int

    setup_longrepr: str | None = None

    call_crash_path: str | None = None
    call_crash_lineno: int | None = None
    call_crash_message: str | None = None

    request: str | None = None
    response: str | None = None


class TestCaseInfo(BaseEntity, TestCaseInfoData, table=True):
    __tablename__ = 'pa_test_case_info'
