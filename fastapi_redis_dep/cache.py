from datetime import timedelta
from typing import Any, TypeVar, Optional
from pydantic import BaseModel

from redis.asyncio import Redis
import orjson


T = TypeVar('T', bound=BaseModel)



def default(obj: Any) -> str:
    """Serialize Pydantic model objects to JSON strings.

    Args:
        obj: The object to be serialized

    Returns:
        str: The serialized JSON string
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump_json()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


async def set_cache(
    client: Redis,
    key: str,
    value: Any,
    expire: Optional[int | timedelta] = None
) -> bool:
    """Set cache value.

    Args:
        client: Redis client instance
        key: Cache key
        value: Value to be cached
        expire: Expiration time (seconds or timedelta object)

    Returns:
        bool: Whether the operation was successful
    """
    try:
        if expire is not None and (
            not isinstance(expire, (int, timedelta)) or 
            (isinstance(expire, int) and expire < 0)
        ):
            return False
       

        value_json = orjson.dumps(
            value,
            option=orjson.OPT_SERIALIZE_NUMPY | 
                   orjson.OPT_SERIALIZE_UUID | 
                   orjson.OPT_PASSTHROUGH_DATACLASS,
            default=default
        )
        await client.set(key, value_json, expire)
        return True
    except orjson.JSONEncodeError as e:
        return False
    except Exception as e:
        return False


async def get_cache(
    client: Redis,
    key: str,
    bind_pydantic_model: Optional[type[T]] = None
) -> Optional[Any | T]:
    """Get cached value.

    Args:
        client: Redis client instance
        key: Cache key
        bind_pydantic_model: Optional Pydantic model class for deserialization

    Returns:
        Optional[Any | T]: Cached value, or instance of bind_pydantic_model if specified
    """
    value = None
    try:
        value = await client.get(key)
        if value is None:
            return None

        value_json = orjson.loads(value)
        if value_json is None:
            return value

        if bind_pydantic_model is not None:
            return bind_pydantic_model.model_validate_json(value_json)
        return value_json

    except orjson.JSONDecodeError as e:
        return value
    except Exception as e:
        return None
