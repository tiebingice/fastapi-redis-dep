from typing import Any, cast

from redis.asyncio import Redis
from pydantic import BaseModel
import orjson


class RedisHash:
    def __init__(self, client: Redis):
        self._client = client


    async def set_hash(self, key: str, data: dict[str, Any] | BaseModel) -> None:
        if isinstance(data, BaseModel):
            data = data.model_dump()

        serialized_data = {
            k: orjson.dumps(v) if not isinstance(v, bytes) else v 
            for k, v in data.items()
        }
        await cast(Any, self._client).hset(name=key, mapping=serialized_data)



    async def get_hash(self, key: str, bind_pydantic_model: type[BaseModel] | None = None) -> dict[str, Any]|BaseModel:
        data = await cast(Any, self._client).hgetall(name=key)
        if not data:
            raise KeyError(f"Key '{key}' does not exist.")

        deserialized_data = {
            k.decode() if isinstance(k, bytes) else k: orjson.loads(v) if isinstance(v, bytes) else v
            for k, v in data.items()
        }
        if bind_pydantic_model:
            return bind_pydantic_model.model_validate(deserialized_data)

        return deserialized_data

    async def delete_field(self, key: str, *field: str) -> int:
        return await cast(Any, self._client).hdel(key, *field)

    async def exists_field(self, key: str, field: str) -> bool:
        return await cast(Any, self._client).hexists(key, field)
