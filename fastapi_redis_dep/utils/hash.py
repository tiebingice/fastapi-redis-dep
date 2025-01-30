from typing import Any, cast,Awaitable,TypeVar


from redis.asyncio import Redis
from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)


class RedisHash:
    def __init__(self, client: Redis):
        self._client = client


    async def set_hash(self, key: str, data: dict[str, Any] | BaseModel) -> bool:
        if isinstance(data, BaseModel):
            data = data.model_dump()
        
        set_data = {}
        
        for k, v in data.items():
            if isinstance(v, BaseModel):
                data[k] = v.model_dump()
            
            if not isinstance(v, (str, bytes, int, float)) or isinstance(v, bool):
                v = str(v)
            set_data[k] = v
        

        return await cast(Awaitable[int], self._client.hset(name=key, mapping=set_data)) == 1


    async def get_hash(self, key: str, bind_pydantic_model: type[T] | None = None) -> dict[str, Any]|T:

        data = await cast(Awaitable[dict[str, Any]], self._client.hgetall(name=key))
        
        if not data:
            raise KeyError(f"Key '{key}' does not exist.")


        if bind_pydantic_model:
            return bind_pydantic_model.model_validate(data)

        return data

    async def delete_field(self, key: str, *field: str) -> int:
        return await cast(Awaitable[int], self._client.hdel(key, *field))

    async def exists_field(self, key: str, field: str) -> bool:
        return await cast(Awaitable[bool], self._client.hexists(key, field))
