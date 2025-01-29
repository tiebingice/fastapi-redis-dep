
from typing import Annotated

import fastapi
import pydantic_settings
import redis.asyncio as aioredis
import tenacity
from .config import RedisSettings
from .exception import RedisException
from fastapi import Depends
from fastapi.requests import HTTPConnection
from .client import RedisDep


class RedisRegistry:

    @classmethod
    async def register_redis(
            cls,
            app: fastapi.FastAPI,
            config: pydantic_settings.BaseSettings|None = None

    ) -> None:
        config = config or RedisSettings() 

        if not isinstance(config, RedisSettings):
            raise RedisException('Redis configuration is not valid')

        clients = await cls._init(config)

        app.state.REDIS = RedisDep(clients)

    @classmethod
    async def _init(cls, config: RedisSettings) -> aioredis.Redis:

        opts = dict(
            db=config.redis_db,
            username=config.redis_user,
            password=config.redis_password,
            max_connections=config.redis_max_connections,
            decode_responses=config.redis_decode_responses,
        )

        address = config.get_redis_address()
        method = aioredis.from_url

        if not address:
            raise ValueError('Redis address is empty')

        @tenacity.retry(
            stop=tenacity.stop_after_attempt(60 * 5),
            wait=tenacity.wait_fixed(1),
        )
        async def _inner():
            return method(address, **opts)

        clients = await _inner()

        ping = await clients.ping()

        if not ping:
            raise RedisException('CouldNotConnected to Redis')

        return clients

    @classmethod
    async def terminate(cls, app: fastapi.FastAPI):
        if app.state.REDIS:
            await app.state.REDIS.aclose()


async def depends_redis(
        conn: HTTPConnection
) -> RedisDep:
    return conn.app.state.REDIS


RedisDependence = Annotated[RedisDep, Depends(depends_redis)]
