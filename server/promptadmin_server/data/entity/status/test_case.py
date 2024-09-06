from pydantic import BaseModel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class TestCaseData(BaseModel):
    test_result_id: int

    nodeid: str
    lineno: int
    outcome: str

    metadata_url: str
    metadata_scenario: str | None = None

    setup_duration: float
    setup_outcome: str

    call_duration: float | None = None
    call_outcome: str | None = None

    teardown_duration: float
    teardown_outcome: str


class TestCase(BaseEntity, TestCaseData, table=True):
    __tablename__ = 'pa_test_case'
