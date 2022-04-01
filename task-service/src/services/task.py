from functools import lru_cache
from typing import Optional

from aioredis import Redis
from fastapi import Depends
from dataclasses import dataclass, field
from uuid import uuid4

from src.db.redis import get_redis
from src.models.task import Task
from src.core.config import CHANNEL


@dataclass
class TaskService:
    redis: Redis = field(default_factory=Redis)

    async def publish_task_config(self, task: Task, data_key:str):
        if data_key:
            task.env_vars = {"data_key": data_key}
        await self._publish_to_channel(task)

    async def store_task_data_to_cache(self, task_data: str) -> Optional[str]:
        if task_data in {'{"data":null}', '{"data":{}}'}:
            return
        return await self._put_task_data_to_cache(task_data)

    async def _put_task_data_to_cache(self, task_data: str) -> str:
        data_key = str(uuid4())[:8]
        await self.redis.set(
            data_key, task_data, ex=120
        )
        return data_key

    async def _publish_to_channel(self, task: Task):
        await self.redis.publish(
            CHANNEL,
            task.json(
                exclude_none=True,
                exclude={"data"},
            )
        )


@lru_cache()
def get_task_service(
        redis: Redis = Depends(get_redis),
) -> TaskService:
    return TaskService(redis)
