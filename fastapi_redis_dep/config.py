from pydantic_settings import BaseSettings
from typing import Optional


class RedisSettings(BaseSettings):
    redis_ssl: bool = False
    redis_url: Optional[str] = None
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_password: Optional[str] = None
    redis_db: int = 12

    redis_max_connections: Optional[int] = None
    redis_decode_responses: bool = True

    redis_secret: Optional[str] = None

    redis_ttl: int = 3600

    def get_redis_address(self) -> str:
        socket_conn = "redis"

        if self.redis_ssl:
            socket_conn = "rediss"

        if self.redis_url:
            return self.redis_url
        elif self.redis_db:
            return f'{socket_conn}://{self.redis_host}:{self.redis_port}/{self.redis_db}'
        else:
            return f'{socket_conn}://{self.redis_host}:{self.redis_port}'
