import logging

import aioredis
import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import task
from src.core import config
from src.core.logger import LOGGING
from src.db import redis

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT
    )

app.include_router(task.router, prefix='/v1/task', tags=['task'])

if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
