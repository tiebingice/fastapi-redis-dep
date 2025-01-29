from typing import AsyncGenerator, Any,cast

from redis.asyncio import Redis


class RedisList:

    def __init__(self, client: Redis):
        self._client: Redis = client

    async def lpush(self, key: str, *value: str) -> int:
        return await cast(Any, self._client).lpush(key, *value)

    async def lindex(self, key: str, index: int) -> str | None:
        return await cast(Any, self._client).lindex(key, index)

    async def linsert(self, name: str, where: str, refvalue: str, value: str) -> int:
        return await cast(Any, self._client).linsert(name, where, refvalue, value)

    async def llen(self, key: str) -> int:
        return await cast(Any, self._client).llen(key)

    async def lpop(self, key: str, count: int | None = None) -> str | list[str] | None:
        return await cast(Any, self._client).lpop(key, count)

    async def lset(self, key: str, index: int, value: str) -> str:
        return await cast(Any, self._client).lset(key, index, value)

    async def rpush(self, key: str, *value: str) -> int:
        return await cast(Any, self._client).rpush(key, *value)

    async def rpop(self, key: str, count: int | None = None) -> str | list[str]:
        return await cast(Any, self._client).rpop(key, count)

    async def lrange(self, key: str, start: int, stop: int) -> list[str]:
        return await cast(Any, self._client).lrange(key, start, stop)

    async def ltrim(self, key: str, start: int, stop: int) -> str:
        return await cast(Any, self._client).ltrim(key, start, stop)

    async def lrem(self, key: str, count: int, value: str) -> int:
        return await cast(Any, self._client).lrem(key, count, value)

    async def list_iterator(self, key: str) -> AsyncGenerator[str, None]:
        length = await cast(Any, self._client).llen(key)
        for i in range(length):
            value = await cast(Any, self._client).lindex(key, i)
            yield value
