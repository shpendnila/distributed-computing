from src.logger import get_logger
from src.config import configuration
from src.job_controller.spawn_job import kube_create_job

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


async def listen_to_channels(subscriber, queue):
    """
    listen for messages from multiple channels
    :param queue:
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
                queue.put_nowait(data)


async def job_worker(executor, queue):
    while True:
        job_configs = await queue.get()
        logger.info(job_configs)
        loop = asyncio.get_event_loop()
        job_creation_tasks = [
            loop.run_in_executor(
                executor, kube_create_job,
                job_conf['name'],
                job_conf['image'],
                job_conf['env_vars'],
                job_conf['namespace']
            ) for job_conf in job_configs
        ]
        completed, pending = await asyncio.wait(job_creation_tasks)
        results = [t.result() for t in completed]
        logger.info(f'job created: {", ".join(results)}')
        queue.task_done()
