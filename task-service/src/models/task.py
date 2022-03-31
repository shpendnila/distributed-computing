import orjson
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


def _orjson_dumps(val, *, default):
    return orjson.dumps(val, default=default).decode()


class Task(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str = "task"
    image: str = 'test'
    env_vars: Optional[dict]
    namespace: str = "default"
    data: Optional[dict]

    class Config:
        json_loads = orjson.loads
        json_dumps = _orjson_dumps
