from src.logger import get_logger
from src.config import configuration

import time
import sys
import json
import redis

logger = get_logger(log_level=configuration.LOG_LEVEL)
redis_host = configuration.HOST
redis_port = configuration.PORT
channels = configuration.CHANNELS


def exit_handler(signum, frame):
    logger.info(f"exited gracefully with signal:{signum}")
    sys.exit()


def get_redis_client():
    logger.debug(f"connecting to redis on {redis_host}:{redis_port}")
    return redis.Redis(
        host=redis_host,
        port=redis_port,
    )


def listen_to_channels(subscriber):
    logger.info(f"listening for messages from {', '.join(channels)}")
    while True:
        message = subscriber.get_message(ignore_subscribe_messages=True)
        if message:
            channel = message['channel']
            data = json.loads(message['data'])
            logger.info(f"channel: {channel}")
            logger.info(f"data: {data}")
        time.sleep(0.1)
