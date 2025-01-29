# FastAPI-Redis-Dep（中文）

`fastapi-redis-dep` 是一个用于 FastAPI 的 Redis 集成库，通过依赖注入和生命周期管理的方式简化了 FastAPI 中 Redis 的操作。该库受
`fastapi_plugins` 第三方库的启发，提供了常用的中间件集成方式。

## 安装方式

### 使用 PIP 安装

```bash
pip install fastapi-redis-dep
```

### 使用 POETRY 安装

```bash
poetry add fastapi-redis-dep
```

## API 介绍

### 快速开始

安装完成后，你需要在 FastAPI 的生命周期函数中注册本库。具体步骤如下：

1. **导入 `RedisRegistry` 类**。
2. **定义生命周期管理函数 `lifespan`**。

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi_redis_dep.redis import RedisRegistry, depends_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisRegistry.register_redis(app)
    yield
    await RedisRegistry.terminate(app)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_redis(redis: RedisDep = Depends(depends_redis)):
    return await redis.client.ping()
```

此时访问 `/` 路径，如果返回 `True`，恭喜你，FastAPI 的 Redis 集成已经完成，接下来你可以使用 Redis 的 API 和本库封装的 API。

## Redis 五大数据结构封装类

### String 数据结构

对应方法为 `redis.string.`。

```python
@app.get("/string")
async def string(redis: RedisDependence):
    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True)
    print(await redis.string.set("test", "test1"))
    print(await redis.string.get_cache("test"))
    print(await redis.string.set_cache("test",{"a": 1.0, "b": 2.0, "c": 3.0}))
    print(await redis.string.set_cache("test1", test_data))
    print(await redis.string.get_cache("test1", bind_pydantic_model=TestModel))
    print(await redis.string.set_cache("test1", 1.111))
    print(await redis.string.get("test"))
    print(await redis.string.delete("test", "test2"))
    print(await redis.string.set("test3", 1))
    print(await redis.string.increase("test3", 2))
    print(await redis.string.decrease("test3", 2))
    print(await redis.string.exists("test"))
    print(await redis.string.set("test", "test"))
    print(await redis.string.append("test", "1"))
    print(await redis.string.lens("test"))
    print(await redis.string.set_or_get("test5", "test5"))
    print(await redis.string.mset({
        "test7": 7,
        "test8": 8,
        "test9": 9
    }))
    print(await redis.string.mget("test7", "test8", "test9"))

    return
```

### Hash 数据结构

对应方法为 `redis.hash.`。

```python
@app.get("/hash")
async def hash(redis: RedisDep = Depends(depends_redis)):
    # 可以通过添加字典的方式引入哈希
    test_data = {
        "field1": "value1",
        "field2": 123,
        "field3": True
    }
    await redis.hash.set_hash("test_hash", test_data)
    print(await redis.hash.get_hash("test_hash"))
    print(await redis.hash.delete_field("test_hash", "field2"))
    print(await redis.hash.exists_field("test_hash", "field1"))
    print(await redis.hash.exists_field("test_hash", "field2"))

    # 同时支持 Pydantic 模型引入哈希
    from pydantic import BaseModel

    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True)
    await redis.hash.set_hash("test_hash1", test_data)
    print(await redis.hash.get_hash("test_hash1", bind_pydantic_model=TestModel))
    print(await redis.hash.delete_field("test_hash1", "field2"))
    print(await redis.hash.exists_field("test_hash1", "field1"))
    print(await redis.hash.exists_field("test_hash1", "field2"))
```

### List 数据结构

对应方法为 `redis.list.`。

```python
@app.get("/list")
async def list(redis: RedisDep = Depends(depends_redis)):
    print(await redis.list.lpush("test_list", "a", "b", "c"))
    print(await redis.list.lindex("test_list", 0))
    print(await redis.list.linsert("test_list", "AFTER", "b", "x"))
    print(await redis.list.llen("test_list"))
    print(await redis.list.lpop("test_list"))
    print(await redis.list.lset("test_list", 1, "y"))
    print(await redis.list.rpush("test_list", "d", "e"))
    print(await redis.list.rpop("test_list"))
    print(await redis.list.lrange("test_list", 0, -1))
    print(await redis.list.ltrim("test_list", 0, 1))
    print(await redis.list.lrem("test_list", 1, "y"))

    async for value in redis.list.list_iterator("test_list"):
        print(value)
```

### Set 数据结构

对应方法为 `redis.set.`。

```python
@app.get("/set")
async def set(redis: RedisDep = Depends(depends_redis)):
    print(await redis.set.add("test_set", "a", "b", "c"))
    print(await redis.set.remove("test_set", "b"))
    print(await redis.set.exists("test_set", "a"))
    print(await redis.set.get_all("test_set"))
    print(await redis.set.length("test_set"))
    print(await redis.set.intersection(["test_set", "another_set"]))
    print(await redis.set.union(["test_set", "another_set"]))
    print(await redis.set.difference(["test_set", "another_set"]))

    # 添加一些数据到 another_set 进行测试
    await redis.set.add("another_set", "b", "c", "d")

    print(await redis.set.intersection(["test_set", "another_set"]))
    print(await redis.set.union(["test_set", "another_set"]))
    print(await redis.set.difference(["test_set", "another_set"]))
```

### Sorted Set 数据结构

对应方法为 `redis.zset.`。

```python
@app.get("/zset")
async def zset(redis: RedisDep = Depends(depends_redis)):
    print(await redis.zset.add("test_zset", {"a": 1.0, "b": 2.0, "c": 3.0}))
    print(await redis.zset.remove("test_zset", "b"))
    print(await redis.zset.score("test_zset", "a"))
    print(await redis.zset.get_all("test_zset", withscores=True))
    print(await redis.zset.length("test_zset"))
    print(await redis.zset.range_by_score("test_zset", 1.0, 3.1, withscores=True))
    print(await redis.zset.rank("test_zset", "a"))
    print(await redis.zset.rank("test_zset", "c", reverse=True))
```

## 缓存的使用

`RedisDep` 类下的 `string` 对象提供了缓存的基本操作，如 `set_cache` 和 `get_cache`。请注意，这些缓存只能用于基本数据类型和
Python 中的 Pydantic 对象。底层使用 `orjson` 进行 JSON 序列化，因此能够缓存的对象即为 `orjson` 支持的对象。同时由于重写了
`default` 函数，因此也能够缓存 Pydantic 对象。如果要缓存更复杂的对象（例如 Tortoise-ORM 的 ORM
对象），请使用第三方缓存工具如 [cashews](https://pypi.org/project/cashews/)。

## 锁机制

```python
@app.get("/lock")
async def lock(redis: RedisDep = Depends(depends_redis)):
    async with redis.lock("test_lock", timeout=10):
        print("locked")
```

底层使用 `redis-lock-py` 实现分布式锁。你可以通过 `redis-lock-py` 创建锁，并使用 `redis.client` 操作 Redis。

## 管道

```python
@app.get("/pipeline")
async def pipeline(redis: RedisDep = Depends(depends_redis)):
    async with redis.pipe() as pipe:
        await pipe.set("test_pipeline", "test_pipeline")
        await pipe.get("test")
        print(await pipe.get("test_pipeline"))
        print(await pipe.get("test_pipeline"))
```

## 获取 Redis 原生操作

```python
@app.get("/redis")
async def redis(redis: RedisDep = Depends(depends_redis)):
    print(redis.client.get("test"))
```

上述为原生的操作，在当前封装的函数不满足需求时可以使用，否则建议使用封装后的函数。

## 设置 Redis 配置

需要引入 `RedisSettings` 类来配置 Redis 连接参数。RedisSettings的实现如下：

```python
from pydantic import BaseSettings


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

```

你可以创建一个 `settings.py` 文件，然后导入这个类。通过这个类实例化对象，实例化时请传入要修改的配置，可以通过一个方法输出这个对象本身。
例如：

```python
def get_redis_settings():
    return RedisSettings(
        redis_url=redis_url,
        redis_host=redis_host,
        redis_port=redis_port,
        redis_user=redis_user,
        redis_password=redis_password
    )
```

## 简写方式

fastapi-redis-dep同时提供了简写方式，需要导入RedisDependence，这是一个注解，通过它你可以快速引入Redis的依赖注入，而无需使用上面的方法。
例如：

```python
@app.get("/redis")
async def redis(redis: RedisDependence):
    print(redis.client.get("test"))
```

在这个例子中，RedisDependence注解用于快速引入Redis的依赖注入，简化了代码。

---

# FastAPI-Redis-Dep (English)

`fastapi-redis-dep` is a Redis integration library for FastAPI that provides common middleware integration using
dependency injection and lifecycle management (inspired by the third-party library `fastapi_plugins`). This makes it
easier to operate Redis within FastAPI.

## Installation Method

### Using PIP

```bash
pip install fastapi-redis-dep
```

### Using POETRY

```bash
poetry add fastapi-redis-dep
```

## API Introduction

### Quick Start

After installation, you need to register this library in the lifecycle functions of FastAPI. Specifically:

1. **Import the `RedisRegistry` class**.
2. **Define the `lifespan` function**.

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi_redis_dep.redis import RedisRegistry, depends_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisRegistry.register_redis(app)
    yield
    await RedisRegistry.terminate(app)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_redis(redis: RedisDep = Depends(depends_redis)):
    return await redis.client.ping()
```

At this point, accessing the `/` path, if it returns `True`, congratulations! Your FastAPI has successfully integrated
with Redis. You can now use Redis APIs and the APIs encapsulated by this library. For more details, see below.

## Five Major Redis Data Structure Encapsulation Classes

### String Data Structure

Corresponding methods are under `redis.string.`.

```python
@app.get("/string")
async def string(redis: RedisDep = Depends(depends_redis)):
    print(await redis.string.set("test", "test1"))
    print(await redis.string.get_cache("test"))
    print(await redis.string.set_cache("test1", 1.111))
    print(await redis.string.get("test"))
    print(await redis.string.delete("test", "test2"))
    print(await redis.string.set("test3", 1))
    print(await redis.string.increase("test3", 2))
    print(await redis.string.decrease("test3", 2))
    print(await redis.string.exists("test"))
    print(await redis.string.set("test", "test"))
    print(await redis.string.append("test", "1"))
    print(await redis.string.lens("test"))
    print(await redis.string.set_or_get("test5", "test5"))
    print(await redis.string.mset({
        "test7": 7,
        "test8": 8,
        "test9": 9
    }))
    print(await redis.string.mget("test7", "test8", "test9"))
```

### Hash Data Structure

Corresponding methods are under `redis.hash.`.

```python
@app.get("/hash")
async def hash(redis: RedisDep = Depends(depends_redis)):
    # Introduce a hash by adding a dictionary
    test_data = {
        "field1": "value1",
        "field2": 123,
        "field3": True
    }
    await redis.hash.set_hash("test_hash", test_data)
    print(await redis.hash.get_hash("test_hash"))
    print(await redis.hash.delete_field("test_hash", "field2"))
    print(await redis.hash.exists_field("test_hash", "field1"))
    print(await redis.hash.exists_field("test_hash", "field2"))

    # Also supports introducing a hash via Pydantic models
    from pydantic import BaseModel

    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True)
    await redis.hash.set_hash("test_hash1", test_data)
    print(await redis.hash.get_hash("test_hash1", bind_pydantic_model=TestModel))
    print(await redis.hash.delete_field("test_hash1", "field2"))
    print(await redis.hash.exists_field("test_hash1", "field1"))
    print(await redis.hash.exists_field("test_hash1", "field2"))
```

### List Data Structure

Corresponding methods are under `redis.list.`.

```python
@app.get("/list")
async def list(redis: RedisDep = Depends(depends_redis)):
    print(await redis.list.lpush("test_list", "a", "b", "c"))
    print(await redis.list.lindex("test_list", 0))
    print(await redis.list.linsert("test_list", "AFTER", "b", "x"))
    print(await redis.list.llen("test_list"))
    print(await redis.list.lpop("test_list"))
    print(await redis.list.lset("test_list", 1, "y"))
    print(await redis.list.rpush("test_list", "d", "e"))
    print(await redis.list.rpop("test_list"))
    print(await redis.list.lrange("test_list", 0, -1))
    print(await redis.list.ltrim("test_list", 0, 1))
    print(await redis.list.lrem("test_list", 1, "y"))

    async for value in redis.list.list_iterator("test_list"):
        print(value)
```

### Set Data Structure

Corresponding methods are under `redis.set.`.

```python
@app.get("/set")
async def set(redis: RedisDep = Depends(depends_redis)):
    print(await redis.set.add("test_set", "a", "b", "c"))
    print(await redis.set.remove("test_set", "b"))
    print(await redis.set.exists("test_set", "a"))
    print(await redis.set.get_all("test_set"))
    print(await redis.set.length("test_set"))
    print(await redis.set.intersection(["test_set", "another_set"]))
    print(await redis.set.union(["test_set", "another_set"]))
    print(await redis.set.difference(["test_set", "another_set"]))

    # Add some data to another_set for testing
    await redis.set.add("another_set", "b", "c", "d")

    print(await redis.set.intersection(["test_set", "another_set"]))
    print(await redis.set.union(["test_set", "another_set"]))
    print(await redis.set.difference(["test_set", "another_set"]))
```

### Sorted Set Data Structure

Corresponding methods are under `redis.zset.`.

```python
@app.get("/zset")
async def zset(redis: RedisDep = Depends(depends_redis)):
    print(await redis.zset.add("test_zset", {"a": 1.0, "b": 2.0, "c": 3.0}))
    print(await redis.zset.remove("test_zset", "b"))
    print(await redis.zset.score("test_zset", "a"))
    print(await redis.zset.get_all("test_zset", withscores=True))
    print(await redis.zset.length("test_zset"))
    print(await redis.zset.range_by_score("test_zset", 1.0, 3.1, withscores=True))
    print(await redis.zset.rank("test_zset", "a"))
    print(await redis.zset.rank("test_zset", "c", reverse=True))
```

## Cache Usage

The `string` object under the `RedisDep` class provides basic cache operations such as `set_cache` and `get_cache`. Note
that this cache can only be used for caching primitive data types and Python's Pydantic objects. The underlying
implementation uses `orjson` for JSON serialization, so the objects that can be cached are those that `orjson` can
serialize. Since the `default` function has been overridden, Pydantic objects can also be cached. If you want to cache
more complex objects such as Tortoise-ORM ORM objects, please use third-party caching tools
like [cashews](https://pypi.org/project/cashews/).

## Lock Mechanism

```python
@app.get("/lock")
async def lock(redis: RedisDep = Depends(depends_redis)):
    async with redis.lock("test_lock", timeout=10):
        print("locked")
```

Under the hood, it uses `redis-lock-py`, so you can perform lock operations using `redis-lock-py`. This function
essentially does the following:

```python
def lock(self, name: str, timeout: int = 10):
    return RedisLock(self._client, name, blocking_timeout=timeout)
```

In summary, you can create locks using `redis-lock-py` and then operate on Redis using the `redis.client`.

## Pipelines

```python
@app.get("/pipeline")
async def pipeline(redis: RedisDep = Depends(depends_redis)):
    async with redis.pipe() as pipe:
        await pipe.set("test_pipeline", "test_pipeline")
        await pipe.get("test")
        print(await pipe.get("test_pipeline"))
        print(await pipe.get("test_pipeline"))
```

## Accessing Native Redis Operations

```python
@app.get("/redis")
async def redis(redis: RedisDep = Depends(depends_redis)):
    print(redis.client.get("test"))
```

The above represents native operations, which should be used when the current encapsulated functions do not meet your
needs; otherwise, it is recommended to use the encapsulated functions.

## Setting Redis Configuration

YTo configure Redis connection parameters, you need to introduce the RedisSettings class. The implementation of
RedisSettings is as follows:

```python
from pydantic import BaseSettings


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

```

You can create a settings.py file and import this class. Instantiate the class with the configurations you want to
modify. You can output this object itself through a method. For example:

```python
def get_redis_settings():
    return RedisSettings(
        redis_url=redis_url,
        redis_host=redis_host,
        redis_port=redis_port,
        redis_user=redis_user,
        redis_password=redis_password
    )
```

## Abbreviation Method

fastapi-redis-dep also provides a shorthand way, which requires importing RedisDependence. This is a decorator that
allows you to quickly inject Redis dependencies without using the method described above.
For example:

```python
@app.get("/redis")
async def redis(redis: RedisDependence):
    print(redis.client.get("test"))
```

In this example, the RedisDependence decorator is used to quickly inject Redis dependencies, simplifying the code.

---