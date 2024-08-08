from promptadmin_server.commons.entity import BaseEntity


class UnitTest(BaseEntity, table=True):
    __tablename__ = 'pa_unit_test'

    sync_data_id: int
    name: str

    test_status: str = 'wait'
    test_preview: str | None = None
    test_response_model: str | None = None  # json
    test_exception: str | None = None
