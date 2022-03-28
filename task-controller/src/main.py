import signal
from src.config import configuration
from src.utils import get_redis_client, listen_to_channels, exit_handler


def main():
    redis_client = get_redis_client()
    sub = redis_client.pubsub()
    sub.subscribe(
        configuration.CHANNELS
    )
    signal.signal(signal.SIGTERM, exit_handler)
    listen_to_channels(sub)


if __name__ == '__main__':
    main()
