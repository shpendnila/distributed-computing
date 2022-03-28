from src.logger import get_logger
from src.config import configuration

import time
import sys
import asyncio
import async_timeout
import json
import aioredis

logger = get_logger(log_level=configuration.LOG_LEVEL)
redis_host = configuration.HOST
redis_port = configuration.PORT
channels = configuration.CHANNELS


def exit_handler(*args):
    """
    exit_handler receives a signal number and a frame where the signal was received from
    :param args: signum,frame
    :return:
    """
    signum = args[0]
    logger.info(f"exited gracefully with signal:{signum}")
    sys.exit()


def get_redis_client():
    """
    create redis client from host and port received as environment variables
    :return: redis client
    """
    logger.debug(f"connecting to redis on {redis_host}:{redis_port}")
    return aioredis.Redis(
        host=redis_host,
        port=redis_port,
    )


async def listen_to_channels(subscriber):
    """
    listen for messages from multiple channels
    :param subscriber:
    :return:
    """
    logger.info(f"listening for messages from: {', '.join(channels)}")
    while True:
        async with async_timeout.timeout(10):
            message = await subscriber.get_message(
                ignore_subscribe_messages=True
            )
            if message:
                channel = message['channel']
                data = json.loads(message['data'])
                logger.info(f"channel: {channel}")
                logger.info(f"data: {data}")
