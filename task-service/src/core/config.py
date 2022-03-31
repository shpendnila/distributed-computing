import os
from logging import config as logging_config

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'task-service')

REDIS_HOST = os.getenv('REDIS_HOST', '10.96.185.105')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
CHANNEL = os.getenv("CHANNEL", "task-channel")
