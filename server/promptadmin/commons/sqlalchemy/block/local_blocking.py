from .block_entity import BlockEntity
import logging

from ...error.unexpected_error import UnexpectedError

_blocks = {

}

logger = logging.getLogger(__name__)


class LocalBlocking:
    @staticmethod
    def register_thread(thread_ident: int, call_name: str):
        if thread_ident not in _blocks:
            _blocks[thread_ident] = {
                'call_name': call_name,
                'blocks': []
            }

    @staticmethod
    def check_register(thread_ident: int):
        if thread_ident not in _blocks:
            raise UnexpectedError("Thread don't register")

    @staticmethod
    def unregister_thread(thread_ident: int):
        if thread_ident not in _blocks:
            return
        blocks = _blocks.pop(thread_ident)
        for i in blocks['blocks']:
            i['repository'].remove(i['entity'])

    @staticmethod
    def get_info_about_thread(thread_ident: int) -> dict[str, str]:
        if thread_ident in _blocks:
            return {
                'call_name': _blocks[thread_ident]['call_name']
            }
        return {
            'call_name': ''
        }

    @staticmethod
    def create_block(thread_ident: int, block_entity: BlockEntity, block_entity_repository):
        LocalBlocking.check_register(thread_ident)
        _blocks[thread_ident]['blocks'].append({'entity': block_entity, 'repository': block_entity_repository})
