from typing import AsyncGenerator, Any,cast,Awaitable

from redis.asyncio import Redis


class RedisList:

    def __init__(self, client: Redis):
        self._client: Redis = client

    async def lpush(self, key: str, *value: str) -> int:
        return await cast(Awaitable[int], self._client.lpush(key, *value))

    async def lindex(self, key: str, index: int) -> str | None:
        return await cast(Awaitable[str | None], self._client.lindex(key, index))

    async def linsert_before(self, name: str, refvalue: str, value: str) -> int:
        return await cast(Awaitable[int], self._client.linsert(name, 'BEFORE', refvalue, value))

    async def linsert_after(self, name: str, refvalue: str, value: str) -> int:
        return await cast(Awaitable[int], self._client.linsert(name, 'AFTER', refvalue, value))

    async def llen(self, key: str) -> int:
        return await cast(Awaitable[int], self._client.llen(key))

    async def lpop(self, key: str, count: int | None = None) -> str | list[str] | None:
        return await cast(Awaitable[str | list[str] | None], self._client.lpop(key, count))

    async def lset(self, key: str, index: int, value: str) -> str:
        return await cast(Awaitable[str], self._client.lset(key, index, value))

    async def rpush(self, key: str, *value: str) -> int:
        return await cast(Awaitable[int], self._client.rpush(key, *value))

    async def rpop(self, key: str, count: int | None = None) -> str | list[str] | None:
        return await cast(Awaitable[str | list[str] | None], self._client.rpop(key, count))

    async def lrange(self, key: str, start: int, stop: int) -> list[str]:
        return await cast(Awaitable[list[str]], self._client.lrange(key, start, stop))

    async def ltrim(self, key: str, start: int, stop: int) -> str:
        return await cast(Awaitable[str], self._client.ltrim(key, start, stop))

    async def lrem(self, key: str, count: int, value: str) -> int:
        return await cast(Awaitable[int], self._client.lrem(key, count, value))

    async def list_iterator(self, key: str) -> AsyncGenerator[str, None]:
        length = await cast(Awaitable[int], self._client.llen(key))
        for i in range(length):
            value = await cast(Awaitable[str | None], self._client.lindex(key, i))
            if value is not None:
                yield value
