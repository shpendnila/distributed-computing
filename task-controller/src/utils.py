from src.logger import get_logger
from src.config import configuration

import redis


logger = get_logger(log_level=configuration.LOG_LEVEL)


def get_redis_client():
    return redis.Redis(
        host=configuration.HOST,
        port=configuration.PORT
    )

