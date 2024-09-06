from pydantic import BaseModel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class TestResultRawData(BaseModel):
    test_result_id: int
    raw_file: str


class TestResultRaw(BaseEntity, TestResultRawData, table=True):
    __tablename__ = 'pa_test_result_raw'
