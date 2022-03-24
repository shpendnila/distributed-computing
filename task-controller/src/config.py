from functools import lru_cache
import os

from yaml import full_load


class Config(object):
    # redis config
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", 6379)
    CHANNELS = full_load(
        os.getenv("CHANNELS", ["test-channel"])
    )

    LOG_LEVEL = int(os.getenv("LOG_LEVEL", 10))


@lru_cache
def get_config():
    return Config()


configuration: Config = get_config()
