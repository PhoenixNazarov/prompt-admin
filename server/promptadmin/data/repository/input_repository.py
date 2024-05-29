from promptadmin.data.entity.input import Input
from promptadmin.commons.repository import AsyncBaseRepository


class InputRepository(AsyncBaseRepository[Input]):
    def __init__(self):
        super().__init__(Input)
