from typing import Any
from pydantic import BaseModel

from redis.asyncio import Redis
import logging
import orjson

logger = logging.getLogger(__name__)



def default(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump_json()


async def set_cache(client: Redis, key: str, value: Any, expire: int = None) -> bool:
    try:
        if expire is not None and (not isinstance(expire, int) or expire < 0):
            logger.error("Invalid expire value: must be a non-negative integer or None")
            return False

        value_json = orjson.dumps(
            value,
            option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_UUID | orjson.OPT_PASSTHROUGH_DATACLASS,
            default=default
        )
        await client.set(key, value_json, expire)
        return True
    except orjson.JSONEncodeError as e:
        logger.error(f"JSON encoding error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


async def get_cache(client: Redis, key: str, bind_pydantic_model: type(BaseModel) | None = None) -> Any:
    value = None
    try:
        value = await client.get(key)

        if value is None:
            return None
        else:

            value_json = orjson.loads(
                value
            )

            if value_json is None:
                return value
            if bind_pydantic_model is not None:
                return bind_pydantic_model.model_validate_json(value_json)
            else:
                return value_json

    except orjson.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        return value
