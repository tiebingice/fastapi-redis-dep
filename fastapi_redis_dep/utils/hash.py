from typing import Any

from redis.asyncio import Redis
from pydantic import BaseModel
import orjson



class RedisHash:
    def __init__(self, client: Redis):
        self._client = client

    async def set_hash(self, key: str, data: dict[str, Any] | type(BaseModel)):
        if isinstance(data, BaseModel):
            data = data.model_dump()

        serialized_data = {k: orjson.dumps(v) for k, v in data.items()}
        await self._client.hset(key, mapping=serialized_data)

    async def get_hash(self, key: str, bind_pydantic_model: type(BaseModel) | None = None) -> dict[str, Any] | type(
        BaseModel):

        data = await self._client.hgetall(key)
        if not data:
            raise KeyError(f"Key '{key}' does not exist.")

        deserialized_data = {k: orjson.loads(v) for k, v in data.items()}
        if bind_pydantic_model:
            return bind_pydantic_model.model_validate(deserialized_data)

        return deserialized_data

    async def delete_field(self, key: str, *field: str) -> int:
        return await self._client.hdel(key, *field)

    async def exists_field(self, key: str, field: str) -> bool:
        return await self._client.hexists(key, field)
