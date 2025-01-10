# FastAPI-Redis-Dep（中文）

fastapi-redis-dep 是一个fastapi的redis集成库，提供了利用依赖注入+生命周期的常用中间价集成方式(
受fastapi_plugins第三方库的启发），使得fastapi中操作redis更为简单。

## 安装方式

### PIP

```
pip install fastapi-redis-dep
```

### POETRY

```
poetry add fastapi-redis-dep
```

## API介绍

### 快速开始

首先安装完成后，你需要在fastapi的生命周期函数中注册本库。
需要导入RedisRegistry类。
具体代码如下：

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from fastapi_redis_dep.redis import RedisRegistry, depends_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisRegistry.register_redis(app)
    yield
    await RedisRegistry.terminate(app)

```

完成后，你就可以在fastapi的依赖注入中直接使用redis了。

```python
from fastapi_redis_dep.client import RedisDep
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_redis(redis: RedisDep = Depends(depends_redis)):
    return await redis.client.ping()
# 此时访问/路径，如果返回true恭喜你，你的fastapi的redis已经集成完毕，接下来你可以尽情使用redis的API已经本库封装的API。详情请看下面。
```

## Redis五大数据结构封装类

### string数据结构

对应的为redis.string.方法

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

### hash数据结构

对应的为redis.hash.方法

```python
@app.get("/hash")
async def hash(redis: RedisDep = Depends(depends_redis)):
    # 可以通过添加字典的方式引入hash
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

    # 同时支持pydantic的方法引入hash
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

    return
```

### list数据结构

对应为redis.list.方法

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
    return ** **
```

### set数据结构

对应为redis.set.方法

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
    #
    # 添加一些数据到 another_set 进行测试
    await redis.set.add("another_set", "b", "c", "d")
    #
    print(await redis.set.intersection(["test_set", "another_set"]))
    print(await redis.set.union(["test_set", "another_set"]))
    print(await redis.set.difference(["test_set", "another_set"]))

    return

```

### zset数据结构

对应为redis.zset.方法

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

    return
```

## 缓存的使用

在redisdep类下的string对象用有对缓存的基本使用即set_cache和get_cache，请注意这个缓存只能用于缓存基本数据类型以及python中的pydantic对象。
底层使用orjson做json序列化，因此能够缓存的对象即为orjson能够缓存的对象。同时由于重写了default函数，因此也能够缓存pydantic对象。
如果要缓存比较复杂的对象例如tortoise-orm的orm对象，请使用 **cashews**(https://pypi.org/project/cashews/)等第三方缓存工具

## 锁机制

```python
@app.get("/lock")
async def lock(redis: RedisDep = Depends(depends_redis)):
    async with redis.lock("test_lock", timeout=10):
        print("locked")
```

底层使用redis-lock-py，因此可以通过使用redis-lock-py进行锁的操作。该函数就做了下面这件事情

```python
def lock(self, name: str, timeout: int = 10):
    return RedisLock(self._client, name, blocking_timeout=timeout)

```

综上所述，你可以使用redis-lock-py来创建锁，然后使用redis.client来操作redis。

## 管道

```python
@app.get("/pipline")
async def pipline(redis: RedisDep = Depends(depends_redis)):
    async with redis.pipe() as pipe:
        await pipe.set("test_pipline", "test_pipline")
        await pipe.get("test")
        print(await pipe.get("test_pipline"))
        print(await pipe.get("test_pipline"))

    return
```

## 获取redis原生操作

```python
@app.get("/redis")
async def redis(redis: RedisDep = Depends(depends_redis)):
    print(redis.client.get("test"))
    return
```

上述为原生的操作，在目前封装的函数不满足使用情况的时候可以使用，否则建议使用封装后的函数。

## 设置Redis配置

需要引入RedisSettings类
如下是redis_settings

```python

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

```

你可以创建一个settings.py文件，然后导入这个类。在环境变量文件书写配置参数，然后实现一个配置类，然后通过一个方法输出该类。

```python
return RedisSettings(
    redis_url=self.redis_url,
    redis_host=self.redis_host,
    redis_port=self.redis_port,
    redis_user=self.redis_user,
    redis_password=self.redis_password
)
```

---

# FastAPI-Redis-Dep（English)

fastapi-redis-dep is a Redis integration library for FastAPI that provides common middleware integration using
dependency injection + lifecycle (inspired by the third-party library fastapi_plugins), making it easier to operate
Redis within FastAPI.

## Installation Method

### PIP

```
pip install fastapi-redis-dep
```

### POETRY

```
poetry add fastapi-redis-dep
```

## API Introduction

### Quick Start

After installation, you need to register this library in the lifecycle functions of FastAPI.
You need to import the RedisRegistry class.
The specific code is as follows:

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from fastapi_redis_dep.redis import RedisRegistry, depends_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisRegistry.register_redis(app)
    yield
    await RedisRegistry.terminate(app)

```

Once completed, you can directly use Redis in FastAPI's dependency injection.

```python
from fastapi_redis_dep.client import RedisDep
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_redis(redis: RedisDep = Depends(depends_redis)):
    return await redis.client.ping()
# At this point, accessing the / path, if it returns true, congratulations, your FastAPI has successfully integrated with Redis. Next, you can freely use Redis APIs and the APIs encapsulated by this library. See below for details.
```

## Five Major Redis Data Structure Encapsulation Classes

### String Data Structure

Corresponding to the redis.string methods

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

Corresponding to the redis.hash methods

```python
@app.get("/hash")
async def hash(redis: RedisDep = Depends(depends_redis)):
    # You can introduce a hash by adding a dictionary
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

    # It also supports introducing a hash via Pydantic methods
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

    return
```

### List Data Structure

Corresponding to the redis.list methods

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
    return ** **
```

### Set Data Structure

Corresponding to the redis.set methods

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
    #
    # Add some data to another_set for testing
    await redis.set.add("another_set", "b", "c", "d")
    #
    print(await redis.set.intersection(["test_set", "another_set"]))
    print(await redis.set.union(["test_set", "another_set"]))
    print(await redis.set.difference(["test_set", "another_set"]))

    return

```

### ZSet Data Structure

Corresponding to the redis.zset methods

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

    return
```

## Cache Usage

The string object under the RedisDep class has basic cache usage through set_cache and get_cache. Please note that this
cache can only be used for caching primitive data types and Python's Pydantic objects.
The underlying implementation uses orjson for JSON serialization, so the objects that can be cached are those that
orjson can serialize. Since the default function has been overridden, Pydantic objects can also be cached.
If you want to cache more complex objects such as Tortoise-ORM ORM objects, please use third-party caching tools like *
*cashews**(https://pypi.org/project/cashews/).

## Lock Mechanism

```python
@app.get("/lock")
async def lock(redis: RedisDep = Depends(depends_redis)):
    async with redis.lock("test_lock", timeout=10):
        print("locked")
```

Under the hood, it uses redis-lock-py, so you can perform lock operations using redis-lock-py. This function essentially
does the following:

```python
def lock(self, name: str, timeout: int = 10):
    return RedisLock(self._client, name, blocking_timeout=timeout)

```

In summary, you can create locks using redis-lock-py and then operate on Redis using the redis.client.

## Pipelines

```python
@app.get("/pipeline")
async def pipeline(redis: RedisDep = Depends(depends_redis)):
    async with redis.pipe() as pipe:
        await pipe.set("test_pipeline", "test_pipeline")
        await pipe.get("test")
        print(await pipe.get("test_pipeline"))
        print(await pipe.get("test_pipeline"))

    return
```

## Accessing Native Redis Operations

```python
@app.get("/redis")
async def redis(redis: RedisDep = Depends(depends_redis)):
    print(redis.client.get("test"))
    return
```

The above represents native operations, which should be used when the current encapsulated functions do not meet your
needs; otherwise, it is recommended to use the encapsulated functions.

## Setting Redis Configuration

You need to import the RedisSettings class.
Below is an example of redis_settings:

```python

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

```

You can create a settings.py file, then import this class. Write configuration parameters in an environment variable
file, implement a configuration class, and output this class through a method.

```python
return RedisSettings(
    redis_url=self.redis_url,
    redis_host=self.redis_host,
    redis_port=self.redis_port,
    redis_user=self.redis_user,
    redis_password=self.redis_password
)
```