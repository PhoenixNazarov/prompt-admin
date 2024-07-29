from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.input import Input
from promptadmin_server.data.repository.input_repository import InputRepository


class InputService(AsyncBaseService[Input]):
    def __init__(self, repository: InputRepository = None):
        super().__init__(repository or InputRepository())
