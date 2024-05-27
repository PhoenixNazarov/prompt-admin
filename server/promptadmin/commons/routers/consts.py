import asyncio


def exchange(name: str) -> str:
    return f'ctl.{name}'


def queue(app_name: str, name: str) -> str:
    return f'{app_name}.{name}'


def index_queue(app_name: str, index: int, name: str) -> str:
    return f'{app_name}-{index}.{name}'


RESPONSE_QUEUE = 'response'


def get_timeout(timeout: int) -> asyncio.Timeout:
    loop = asyncio.get_running_loop()
    return asyncio.Timeout(loop.time() + timeout)
