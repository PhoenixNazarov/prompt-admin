from promptadmin.commons.service.async_base_service import AsyncBaseService
from promptadmin.data.entity.input import Input
from promptadmin.data.repository.input_repository import InputRepository


class InputService(AsyncBaseService[Input]):
    def __init__(self, repository: InputRepository = None):
        super().__init__(repository or InputRepository())
