from promptadmin.data.entity.macro import Macro
from promptadmin.commons.repository import AsyncBaseRepository


class MacroRepository(AsyncBaseRepository[Macro]):
    def __init__(self):
        super().__init__(Macro)
