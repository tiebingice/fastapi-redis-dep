from typing import AsyncGenerator
from datetime import timedelta

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
from .utils.string import RedisString
from .utils.set import RedisSet
from .utils.zset import RedisZset
from .utils.list import RedisList
from .utils.hash import RedisHash
from contextlib import asynccontextmanager
from redis_lock.asyncio import RedisLock
from typing import Awaitable, cast

class RedisDep:
    def __init__(self, client: Redis):
        self._client = client
        self._string = RedisString(client)
        self._set = RedisSet(client)
        self._zset = RedisZset(client)
        self._list = RedisList(client)
        self._hash = RedisHash(client)

    async def aclose(self):
        print("redis client closed!")
        await self._client.aclose()

    @property
    def client(self) -> Redis:
        return self._client

    @property
    def string(self) -> RedisString:
        return self._string

    @property
    def set(self) -> RedisSet:
        return self._set

    @property
    def list(self) -> RedisList:
        return self._list

    @property
    def zset(self) -> RedisZset:
        return self._zset

    @property
    def hash(self) -> RedisHash:
        return self._hash

    @asynccontextmanager
    async def pipe(self, transaction: bool = True) -> AsyncGenerator[Pipeline, None]:
        pipe = self._client.pipeline(transaction=transaction)
        yield pipe
        await pipe.execute()

    def lock(self, name: str, timeout: int = 10) -> RedisLock:
        return RedisLock(self._client, name, blocking_timeout=timeout)


    async def expire(self, key: str, time_seconds: int | timedelta) -> bool:
        """Set the expiration time for a key.
        
        Args:
            key: Redis key
            time_seconds: Expiration time, can be seconds or a timedelta object
        
        Returns:
            bool: Whether the operation was successful
        """
        
        return await cast(Awaitable[bool], self._client.expire(key, time_seconds))
    
    async def delete(self, key: str) -> bool:
        """Delete a key from Redis.
        
        Args:
            key: Redis key to be deleted
        
        Returns:
            bool: Whether the deletion was successful
        """
        return await cast(Awaitable[int], self._client.delete(key)) == 1
