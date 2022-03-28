import signal
import asyncio
from src.config import configuration
from src.utils import get_redis_client, listen_to_channels, exit_handler


async def main():
    redis_client = get_redis_client()
    sub = redis_client.pubsub()
    await sub.subscribe(
        'test-channel'
    )
    # signal.signal(signal.SIGTERM, exit_handler)
    future = asyncio.create_task(listen_to_channels(sub))
    await future

if __name__ == '__main__':
    asyncio.run(main())
