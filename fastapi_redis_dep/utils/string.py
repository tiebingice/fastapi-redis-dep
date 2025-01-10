from typing import Any

from redis.asyncio import Redis
from ..cache import set_cache, get_cache
from pydantic import BaseModel

StringVal = str | bytes | int | float



class RedisString:
    def __init__(self, client: Redis):
        self._client = client

    async def set(self, key: str, value: StringVal, expire: int | None = None) -> bool:
        return await self._client.set(key, value, expire)

    async def get(self, key: str) -> StringVal | None:
        return await self._client.get(key)

    async def delete(self, *keys: str) -> int:
        return await self._client.delete(*keys)

    async def increase(self, key: str, step: int) -> int:
        return await self._client.incr(key, step)

    async def decrease(self, key: str, step: int) -> int:
        return await self._client.decr(key, step)

    async def exists(self, *keys: str) -> int:
        return await self._client.exists(*keys) > 0

    async def append(self, key: str, value: str) -> int:
        return await self._client.append(key, value)

    async def lens(self, key: str) -> int:
        return await self._client.strlen(key)

    async def set_or_get(self, key: str, value_default: StringVal | None = None) -> StringVal:
        if await self._client.exists(key):
            return await self._client.get(key)
        return await self._client.set(key, value_default)

    async def mset(self, key_value: dict[str, StringVal]) -> bool:
        return await self._client.mset(key_value)

    async def mget(self, *keys: str) -> list[str | None]:
        return await self._client.mget(*keys)

    async def set_cache(self, key: str, value: StringVal | type(BaseModel), expire: int | None = None) -> bool:
        return await set_cache(self._client, key, value, expire)

    async def get_cache(self, key: str, bind_pydantic_model: type(BaseModel) | None = None) -> Any:
        return await get_cache(self._client, key, bind_pydantic_model)
