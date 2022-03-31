from functools import lru_cache
from typing import Optional

from aioredis import Redis
from fastapi import Depends
from dataclasses import dataclass, field

from src.db.redis import get_redis
from src.models.task import Task
from src.core.config import CHANNEL


@dataclass
class TaskService:
    redis: Redis = field(default_factory=Redis)

    async def publish_task_config(self, task: Task) -> str:
        if not task:
            return "Task is empty"
        await self._publish_to_channel(task)
        return f"task config was published into {CHANNEL}"

    async def store_task_data_to_cache(self, task: Task) -> Optional[str]:
        if not task:
            return
        await self._put_task_data_to_cache(task)
        return str(task.uid)[:8]

    async def _put_task_data_to_cache(self, task: Task):
        await self.redis.set(
            str(task.uid)[:8], task.json(), ex=120
        )

    async def _publish_to_channel(self, task: Task):
        await self.redis.publish(
            CHANNEL,
            task.json()
        )


@lru_cache()
def get_task_service(
        redis: Redis = Depends(get_redis),
) -> TaskService:
    return TaskService(redis)
