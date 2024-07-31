from promptadmin_server.commons.entity import BaseEntity


class SyncData(BaseEntity, table=True):
    __tablename__ = 'pa_sync_data'

    service_model_info: str
    template_context_type: str
    template_context_default: str
    history_context_default: str
    parsed_model_type: str | None
    parsed_model_default: str | None
    fail_parse_model_strategy: str | None

    test_status: str = 'wait'
    test_preview: str | None = None
    test_response_model: str | None = None  # json
    test_exception: str | None = None
