from pydantic import BaseModel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class TestResultData(BaseModel):
    connection_name: str

    created: float
    duration: float

    passed: int
    skipped: int
    error: int
    failed: int
    total: int
    collected: int


class TestResult(BaseEntity, TestResultData, table=True):
    __tablename__ = 'pa_test_result'
