from datetime import timedelta
from typing import Any, Awaitable, cast, Optional,TypeAlias

from redis.asyncio import Redis
from ..cache import set_cache, get_cache,T


StringType: TypeAlias = str | bytes | int | float



class RedisString:
    def __init__(self, client: Redis):
        self._client: Redis = client

    async def set(self, key: str, value: StringType, expire: Optional[int | timedelta] = None) -> bool:
        return await cast(Awaitable[bool], self._client.set(key, value, expire))

    async def get(self, key: str) -> Optional[StringType]:
        return await cast(Awaitable[Optional[StringType]], self._client.get(key))

    async def delete(self, *keys: str) -> int:
        return await cast(Awaitable[int], self._client.delete(*keys))

    async def increase(self, key: str, step: int = 1) -> int:
        return await cast(Awaitable[int], self._client.incr(key, step))

    async def decrease(self, key: str, step: int = 1) -> int:
        return await cast(Awaitable[int], self._client.decr(key, step))

    async def exists(self, *keys: str) -> bool:
        return await cast(Awaitable[bool], self._client.exists(*keys)) > 0

    async def append(self, key: str, value: str) -> int:
        return await cast(Awaitable[int], self._client.append(key, value))

    async def lens(self, key: str) -> int:
        return await cast(Awaitable[int], self._client.strlen(key))

    async def set_or_get(self, key: str,
                         value_default: StringType | None = None) -> StringType | None:
        if await cast(Awaitable[bool], self._client.exists(key)):
            return await cast(Awaitable[Optional[StringType]], self._client.get(key))

        if value_default is None:
            return None
        await cast(Awaitable[bool], self._client.set(key, value_default))

        return value_default

    async def mset(self, key_value: dict[str, StringType]) -> bool:
        return await cast(Awaitable[bool], self._client.mset(key_value))

    async def mget(self, *keys: str) -> list[str | None]:
        return await cast(Awaitable[list[str | None]], self._client.mget(*keys))

    async def set_cache(self, key: str, value: Any,
                        expire: Optional[int | timedelta] = None) -> bool:
        return await set_cache(self._client, key, value, expire)

    async def get_cache(self, key: str, bind_pydantic_model: Optional[type[T]]  = None) ->T|None :
        return await get_cache(self._client, key, bind_pydantic_model)
