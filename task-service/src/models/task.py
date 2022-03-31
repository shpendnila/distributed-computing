import orjson
from pydantic import BaseModel


class Task(BaseModel):
    name: str
    image: str
    env_vars: dict
    namespace: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
