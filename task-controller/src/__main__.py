import signal
import asyncio
import concurrent.futures

from src.config import configuration
from src.utils import (
    get_redis_client,
    listen_to_channels,
    exit_handler,
    job_worker,
)


async def main():
    executor = concurrent.futures.ThreadPoolExecutor()
    queue = asyncio.Queue()
    redis_client = get_redis_client()
    sub = redis_client.pubsub()
    await sub.subscribe(
        *configuration.CHANNELS
    )

    signal.signal(signal.SIGTERM, exit_handler)

    message_listener = asyncio.create_task(listen_to_channels(sub, queue))
    message_worker = asyncio.create_task(job_worker(executor, queue))

    await message_listener
    await message_worker
    await queue.join()


if __name__ == '__main__':
    asyncio.run(main())
