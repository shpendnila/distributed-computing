from src.logger import get_logger
from src.config import configuration

import time
import json
import redis

logger = get_logger(log_level=configuration.LOG_LEVEL)
redis_host = configuration.HOST
redis_port = configuration.PORT


def get_redis_client():
    logger.debug(f"connecting to redis on {redis_host}:{redis_port}")
    return redis.Redis(
        host=redis_host,
        port=redis_port,
    )


def listen_to_channels(subscriber):
    logger.info("Listening for messages")
    while True:
        message = subscriber.get_message()
        if message and message['type'] == "message":
            channel = message['channel']
            data = json.loads(message['data'])
            logger.info(f"channel: {channel}")
            logger.info(f"data: {data}")
        time.sleep(0.1)