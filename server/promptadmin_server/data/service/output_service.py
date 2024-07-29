from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.output import Output
from promptadmin_server.data.repository.output_repository import OutputRepository


class OutputService(AsyncBaseService[Output]):
    def __init__(self, repository: OutputRepository = None):
        super().__init__(repository or OutputRepository())
