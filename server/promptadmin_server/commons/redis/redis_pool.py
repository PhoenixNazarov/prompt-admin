from ..singleton_metaclass import Singleton
import redis.asyncio as redis
from settings import SETTINGS
import logging

logger = logging.getLogger(__name__)


class RedisPool(metaclass=Singleton):
    def __init__(self):
        if SETTINGS.redis_cache:
            self.redis = redis.Redis(
                host=SETTINGS.redis_cache.host,
                port=SETTINGS.redis_cache.port,
                password=SETTINGS.redis_cache.password,
                decode_responses=True,
            )
        else:
            raise
            logger.warning('Redis cache is not set')
            self.redis = None

    def get_redis(self):
        return self.redis
