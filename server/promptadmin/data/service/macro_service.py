from promptadmin.commons.service.async_base_service import AsyncBaseService
from promptadmin.data.entity.macro import Macro
from promptadmin.data.repository.macro_repository import MacroRepository


class MacroService(AsyncBaseService[Macro]):
    def __init__(self, repository: MacroRepository = None):
        super().__init__(repository or MacroRepository())
