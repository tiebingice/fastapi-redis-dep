from typing import AsyncGenerator

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
from .utils.string import RedisString
from .utils.set import RedisSet
from .utils.zset import RedisZset
from .utils.list import RedisList
from .utils.hash import RedisHash
from contextlib import asynccontextmanager
from redis_lock.asyncio import RedisLock


class RedisDep:
    def __init__(self, client: Redis):
        self._client = client
        self.string = RedisString(self._client)
        self.set = RedisSet(self._client)
        self.zset = RedisZset(self._client)
        self.list = RedisList(self._client)
        self.hash = RedisHash(self._client)

    async def aclose(self):
        await self._client.aclose()

    @property
    def client(self) -> Redis:
        return self._client

    @asynccontextmanager
    async def pipe(self, transaction: bool = True) -> AsyncGenerator[Pipeline, None]:
        pipe = self._client.pipeline(transaction=transaction)
        yield pipe
        await pipe.execute()

    def lock(self, name: str, timeout: int = 10) -> RedisLock:
        return RedisLock(self._client, name, blocking_timeout=timeout)
