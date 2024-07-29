from functools import wraps
import threading

from .local_blocking import LocalBlocking


def blocking(func):
    fname = func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        thread_ident = threading.get_ident()
        LocalBlocking.register_thread(thread_ident, fname)
        out = None
        error = None
        try:
            out = func(*args, **kwargs)
        except Exception as e:
            error = e
        finally:
            LocalBlocking.unregister_thread(thread_ident)
        if error:
            raise error
        return out

    return wrapper
