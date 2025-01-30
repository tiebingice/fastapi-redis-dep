# FastAPI-Redis-Dep

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

    #定义一个pydantic模型
    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True) 

    #字符串的Set与Get
    print("Set",await redis.string.set("test", "test1")) #set一个python字符串 返回一个布尔值代表是否设置成功，此时结果应该是true
    print("Get",await redis.string.get("test")) #get 一个python字符串 返回一个字符串，此时结果应该是test1
    print("Set Or Get",await redis.string.set_or_get("test2", "test2")) #新操作Set Or Get ,如果key存在就Get,否则Set 结果是 test2

    #字符串的Delete
    print("Set",await redis.string.set("test2", b"1")) #set一个python bytes 结果是true
    print("Set",await redis.string.set("test3", 1)) #set一个python int 结果是true
    print("Delete",await redis.string.delete("test2", "test3")) #delete一个或多个key，返回删除的个数，结果是2


    #字符串的Exists
    print("Exists",await redis.string.exists("test")) #判断是否存在一个key 返回一个布尔值，结果是true
    print("Exists",await redis.string.exists("test2")) #判断是否存在一个key 返回一个布尔值，结果是false
    print("Exists",await redis.string.exists("test3")) #判断是否存在一个key 返回一个布尔值，结果是false


    #字符串的Append
    print("Append",await redis.string.append("test", "1"))  #append一个python字符串，返回的是操作后的字符串长度，结果应该是5+1=6

    #字符串的Len
    print("Len",await redis.string.lens("test")) #获取字符串的长度，结果是6

    #字符串的批量Set和Get
    print("Mset",await redis.string.mset({
    "test7": 7,
    "test8": 8,
    "test9": 9
    })) #批量set，返回的是布尔值，结果是true
    print("Mget",await redis.string.mget("test7", "test8", "test9")) #批量get，返回的是一个列表，结果是[7, 8, 9]


    #缓存的简单使用
    print("Get Cache",await redis.string.get_cache("test")) #获取缓存,结果是test1
    print("Set Cache dict",await redis.string.set_cache("test",{"a": 1.0, "b": 2.0, "c": 3.0})) #设置缓存，一个python dict,返回一个布尔值，结果是true
    print("Set Cache pydantic model",await redis.string.set_cache("test1", test_data)) #设置缓存，一个pydantic模型,返回一个布尔值，结果是true
    print("Get Cache ",await redis.string.get_cache("test")) #获取缓存，一个python dict,返回一个python dict，结果是{"a": 1.0, "b": 2.0, "c": 3.0}
    print("Get Cache",await redis.string.get_cache("test1", bind_pydantic_model=TestModel)) #获取缓存，一个pydantic模型，返回一个pydantic模型，结果是TestModel(field1='value1', field2=123, field3=True)

    ## 如果设置了bind_pydantic_model，返回的是pydantic模型，否则返回的是python dict或者是list,取决于如何这个值本身。

   
    # 字符串的数字操作，增加和减少 
    print(await redis.string.increase("test3", 2)) #字符串的数字操作，增加，返回一个字符串，结果是2
    print(await redis.string.decrease("test3", 2)) #字符串的数字操作，减少，返回一个字符串，结果是0
  

    return {
        "message": "Hello World"
    }


```

### Hash 数据结构
对应方法为 `redis.hash.`。
```python
@app.get("/hash")
async def hash(redis: RedisDependence):
    test_data = {
        "field1": "value1",
        "field2": 123,
        "field3": True
    } #设置一个字典

    # 设置一个哈希
    await redis.hash.set_hash("test_hash", test_data) #设置一个哈希,
    print("get_hash",await redis.hash.get_hash("test_hash")) #获取一个哈希,返回一个字典，结果是{'field1': 'value1', 'field2': '123', 'field3': 'True'}
    print("delete_field",await redis.hash.delete_field("test_hash", "field2")) #删除一个字段,返回一个整数，代表删除的数量，结果是1
    print("exists_field",await redis.hash.exists_field("test_hash", "field1")) #判断一个字段是否存在，返回一个布尔值，代表是否存在，结果是True
    print("exists_field",await redis.hash.exists_field("test_hash", "field2")) #判断一个字段是否存在，返回一个布尔值，代表是否存在，结果是False

    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True) #设置一个pydantic模型
    await redis.hash.set_hash("test_hash1", test_data) #设置一个哈希,设置pydantic模型
    print("get_hash",await redis.hash.get_hash("test_hash1", bind_pydantic_model=TestModel)) #获取一个哈希,获取pydantic模型，结果是 field1='value1' field2=123 field3=True


    return {
        "message": "Hello World"
    }


```

### List 数据结构

对应方法为 `redis.list.`。

```python
@app.get("/list")
async def list(redis: RedisDependence):
    # 列表的增加
    print("lpush",await redis.list.lpush("test_list", "a", "b", "c")) #列表的增加，添加到列表的前部，返回一个整数，代表现在列表的长度，结果是3
    print("rpush",await redis.list.rpush("test_list", "d", "e")) #列表的增加，添加到列表的后部，返回一个整数，代表现在列表的长度，结果是5

    print("insert_before",await redis.list.linsert_before("test_list", "b", "x")) #列表的增加，在第二个参数的前面添加一个参数，返回一个整数，代表现在列表的长度，结果是6
    print("insert_after",await redis.list.linsert_after("test_list", "b", "x")) #列表的增加，在第二个参数的后面添加一个参数，返回一个整数，代表现在列表的长度，结果是7

    #获取列表的元素，利用下标
    print("Lindex",await redis.list.lindex("test_list", 0)) #列表的获取,获取第一个元素，返回一个元素，结果是"c"


    #列表的长度
    print("Llen",await redis.list.llen("test_list")) #列表的长度,返回一个整数，结果是7

    #列表的删除
    print("Lpop",await redis.list.lpop("test_list")) #列表的删除，删除首部，返回一个元素，结果是"c"
    print("Rpop",await redis.list.rpop("test_list")) #列表的删除，删除尾部，返回一个元素，结果是"e"

    #列表的修改
    print("Lset",await redis.list.lset("test_list", 1, "y")) #列表的修改，指定下标修改,返回一个布尔值，代表是否修改成功，结果是True
 


    #列表的截取
    print("Lpush",await redis.list.lpush("test_list", "y", "a", "b","y","y","a","b")) 
    print("Lrange",await redis.list.lrange("test_list", 0, -1)) #列表的截取 返回一个list,结果是['b', 'a', 'y', 'y', 'b', 'a', 'y', 'x', 'y', 'x', 'a', 'd']
    print("Lrem",await redis.list.lrem("test_list", 1, "y")) #列表的删除，从头部搜索删除值为y的元素（删除数量=1），返回一个整数，代表删除的数量，结果是1
    print("Lrem",await redis.list.lrem("test_list", -2, "y")) #列表的删除，从尾部搜索删除值为y的元素（删除数量=2），返回一个整数，代表删除的数量，结果是2
    print("Ltrim",await redis.list.ltrim("test_list", 0, 1)) #列表的截取，截取从0到1的元素，其它删除,返回一个布尔值，代表是否删除成功，结果是True
    async for value in redis.list.list_iterator("test_list"): #列表的迭代
        print(value)
    
    return {
        "message": "Hello World"
    }

```

### Set 数据结构

对应方法为 `redis.set.`。

```python
@app.get("/string")
async def string(redis: RedisDependence):

    #定义一个pydantic模型
    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True) 

    #字符串的Set与Get
    print("Set",await redis.string.set("test", "test1")) #set一个python字符串 返回一个布尔值代表是否设置成功，此时结果应该是true
    print("Get",await redis.string.get("test")) #get 一个python字符串 返回一个字符串，此时结果应该是test1
    print("Set Or Get",await redis.string.set_or_get("test2", "test2")) #新操作Set Or Get ,如果key存在就Get,否则Set 结果是 test2

    #字符串的Delete
    print("Set",await redis.string.set("test2", b"1")) #set一个python bytes 结果是true
    print("Set",await redis.string.set("test3", 1)) #set一个python int 结果是true
    print("Delete",await redis.string.delete("test2", "test3")) #delete一个或多个key，返回删除的个数，结果是2


    #字符串的Exists
    print("Exists",await redis.string.exists("test")) #判断是否存在一个key 返回一个布尔值，结果是true
    print("Exists",await redis.string.exists("test2")) #判断是否存在一个key 返回一个布尔值，结果是false
    print("Exists",await redis.string.exists("test3")) #判断是否存在一个key 返回一个布尔值，结果是false


    #字符串的Append
    print("Append",await redis.string.append("test", "1"))  #append一个python字符串，返回的是操作后的字符串长度，结果应该是5+1=6

    #字符串的Len
    print("Len",await redis.string.lens("test")) #获取字符串的长度，结果是6

    #字符串的批量Set和Get
    print("Mset",await redis.string.mset({
    "test7": 7,
    "test8": 8,
    "test9": 9
    })) #批量set，返回的是布尔值，结果是true
    print("Mget",await redis.string.mget("test7", "test8", "test9")) #批量get，返回的是一个列表，结果是[7, 8, 9]


    #缓存的简单使用
    print("Get Cache",await redis.string.get_cache("test")) #获取缓存,结果是test1
    print("Set Cache dict",await redis.string.set_cache("test",{"a": 1.0, "b": 2.0, "c": 3.0})) #设置缓存，一个python dict,返回一个布尔值，结果是true
    print("Set Cache pydantic model",await redis.string.set_cache("test1", test_data)) #设置缓存，一个pydantic模型,返回一个布尔值，结果是true
    print("Get Cache ",await redis.string.get_cache("test")) #获取缓存，一个python dict,返回一个python dict，结果是{"a": 1.0, "b": 2.0, "c": 3.0}
    print("Get Cache",await redis.string.get_cache("test1", bind_pydantic_model=TestModel)) #获取缓存，一个pydantic模型，返回一个pydantic模型，结果是TestModel(field1='value1', field2=123, field3=True)

    ## 如果设置了bind_pydantic_model，返回的是pydantic模型，否则返回的是python dict或者是list,取决于如何这个值本身。

   
    # 字符串的数字操作，增加和减少 
    print(await redis.string.increase("test3", 2)) #字符串的数字操作，增加，返回一个字符串，结果是2
    print(await redis.string.decrease("test3", 2)) #字符串的数字操作，减少，返回一个字符串，结果是0
  

    return {
        "message": "Hello World"
    }


```

### Hash 数据结构

对应方法为 `redis.hash.`。

```python
@app.get("/hash")
async def hash(redis: RedisDependence):
    test_data = {
        "field1": "value1",
        "field2": 123,
        "field3": True
    } #设置一个字典

    # 设置一个哈希
    await redis.hash.set_hash("test_hash", test_data) #设置一个哈希,
    print("get_hash",await redis.hash.get_hash("test_hash")) #获取一个哈希,返回一个字典，结果是{'field1': 'value1', 'field2': '123', 'field3': 'True'}
    print("delete_field",await redis.hash.delete_field("test_hash", "field2")) #删除一个字段,返回一个整数，代表删除的数量，结果是1
    print("exists_field",await redis.hash.exists_field("test_hash", "field1")) #判断一个字段是否存在，返回一个布尔值，代表是否存在，结果是True
    print("exists_field",await redis.hash.exists_field("test_hash", "field2")) #判断一个字段是否存在，返回一个布尔值，代表是否存在，结果是False

    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True) #设置一个pydantic模型
    await redis.hash.set_hash("test_hash1", test_data) #设置一个哈希,设置pydantic模型
    print("get_hash",await redis.hash.get_hash("test_hash1", bind_pydantic_model=TestModel)) #获取一个哈希,获取pydantic模型，结果是 field1='value1' field2=123 field3=True


    return {
        "message": "Hello World"
    }


```

### List 数据结构

对应方法为 `redis.list.`。

```python
@app.get("/list")
async def list(redis: RedisDependence):
    # 列表的增加
    print("lpush",await redis.list.lpush("test_list", "a", "b", "c")) #列表的增加，添加到列表的前部，返回一个整数，代表现在列表的长度，结果是3
    print("rpush",await redis.list.rpush("test_list", "d", "e")) #列表的增加，添加到列表的后部，返回一个整数，代表现在列表的长度，结果是5

    print("insert_before",await redis.list.linsert_before("test_list", "b", "x")) #列表的增加，在第二个参数的前面添加一个参数，返回一个整数，代表现在列表的长度，结果是6
    print("insert_after",await redis.list.linsert_after("test_list", "b", "x")) #列表的增加，在第二个参数的后面添加一个参数，返回一个整数，代表现在列表的长度，结果是7

    #获取列表的元素，利用下标
    print("Lindex",await redis.list.lindex("test_list", 0)) #列表的获取,获取第一个元素，返回一个元素，结果是"c"


    #列表的长度
    print("Llen",await redis.list.llen("test_list")) #列表的长度,返回一个整数，结果是7

    #列表的删除
    print("Lpop",await redis.list.lpop("test_list")) #列表的删除，删除首部，返回一个元素，结果是"c"
    print("Rpop",await redis.list.rpop("test_list")) #列表的删除，删除尾部，返回一个元素，结果是"e"

    #列表的修改
    print("Lset",await redis.list.lset("test_list", 1, "y")) #列表的修改，指定下标修改,返回一个布尔值，代表是否修改成功，结果是True
 


    #列表的截取
    print("Lpush",await redis.list.lpush("test_list", "y", "a", "b","y","y","a","b")) 
    print("Lrange",await redis.list.lrange("test_list", 0, -1)) #列表的截取 返回一个list,结果是['b', 'a', 'y', 'y', 'b', 'a', 'y', 'x', 'y', 'x', 'a', 'd']
    print("Lrem",await redis.list.lrem("test_list", 1, "y")) #列表的删除，从头部搜索删除值为y的元素（删除数量=1），返回一个整数，代表删除的数量，结果是1
    print("Lrem",await redis.list.lrem("test_list", -2, "y")) #列表的删除，从尾部搜索删除值为y的元素（删除数量=2），返回一个整数，代表删除的数量，结果是2
    print("Ltrim",await redis.list.ltrim("test_list", 0, 1)) #列表的截取，截取从0到1的元素，其它删除,返回一个布尔值，代表是否删除成功，结果是True
    async for value in redis.list.list_iterator("test_list"): #列表的迭代
        print(value)
    
    return {
        "message": "Hello World"
    }

```

### Set 数据结构

对应方法为 `redis.set.`。

```python
@app.get("/set")
async def set(redis: RedisDependence):
    # 集合的增加和删除
    print("Add",await redis.set.add("test_set", "a", "b", "c")) #集合增加，返回一个布尔值，结果是true
    print("Remove",await redis.set.remove("test_set", "b")) #集合删除，返回一个布尔值，结果是true
    print("Exists",await redis.set.exists("test_set", "a")) #集合判断，返回一个布尔值，结果是true

    # 获取集合的所有成员
    print("Get All",await redis.set.get_all("test_set")) #集合获取所有成员，返回一个集合，结果是{ "c", "a" }

    # 获取集合的长度
    print("Length",await redis.set.length("test_set")) #集合获取长度，返回一个整数，结果是2


    
    #集合的交并差运算 
    await redis.set.add("another_set", "b", "c", "d") 
    print("Intersection",await redis.set.intersection(["test_set", "another_set"])) #交集，返回一个集合，结果是{ "c" }
    print("Union",await redis.set.union(["test_set", "another_set"])) #并集，返回一个集合，结果是{ "c", "d", "a", "b" }
    print("Difference",await redis.set.difference(["test_set", "another_set"])) #差集，返回一个集合，结果是{ "a" }

    return {
        "message": "Hello World"
    }

```

### Sorted Set 数据结构

对应方法为 `redis.zset.`。

```python
@app.get("/zset")
async def zset(redis: RedisDependence):

    #Zset的增加
    print("Zadd",await redis.zset.add("test_zset", {"a": 1.0, "b": 2.0, "c": 4.0})) #Zset的增加，返回一个整数，代表添加的数量，结果是3
    
    #Zset的删除
    print("Zrem",await redis.zset.remove("test_zset", "b")) #Zset的删除，返回一个整数，代表删除的数量，结果是1

    #Zset的获取
    print("Zscore",await redis.zset.score("test_zset", "a")) #Zset的获取,获取某个值的分数，返回一个浮点数，结果是1.0
    print("Zrange",await redis.zset.range("test_zset")) #Zset的获取，根据下标，返回一个list，结果是['a', 'c']
    print("Zrange with scores",await redis.zset.range_with_scores("test_zset")) #Zset的获取，根据下标，返回一个list，结果是[('a', 1.0), ('c', 4.0)]
    print("Zrange_by_score",await redis.zset.range_by_score("test_zset", 1.0, 3.1)) #Zset的获取，根据分数，返回一个list，结果是['a']
    print("Zrange_by_score with scores",await redis.zset.range_by_score_and_with("test_zset", 1.0, 3.1)) #Zset的获取，根据分数，返回一个list，结果是[('a', 1.0)]
    
    #Zset的长度
    print("Zlen",await redis.zset.length("test_zset")) #Zset的长度，返回一个整数，代表集合的长度，结果是2

    #Zset的排名
    print("Zrank",await redis.zset.rank("test_zset", "a")) #Zset的排名，返回一个整数，代表值的排名，结果是0
    print("Zrank",await redis.zset.rank("test_zset", "c", reverse=True)) #Zset的排名逆序，返回一个整数，代表值的排名，结果是0

    return {
        "message": "Hello World"
    }

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

@app.get("/pipline")
async def pipline(redis: RedisDependence):
    async with redis.pipe() as pipe:
        await pipe.set("test_pipline", "test_pipline")
        await pipe.get("test")
    print(await redis.string.get("test_pipline"))
   

    return {
        "message": "Hello World"
    }
```

## 三个通用操作
```python
@app.get("/")
async def get_redis(redis: RedisDependence):
    await redis.expire("test_hash", 10) #通用方法，设置key的过期时间
    await redis.delete("test_list") #通用方法，删除key
    return await redis.client.ping()

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

The corresponding method is `redis.string.`.

```python

@app.get("/string")
async def string(redis: RedisDependence):

    # Define a pydantic model
    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True) 

    # String Set and Get
    print("Set", await redis.string.set("test", "test1")) # Set a Python string, returns a boolean indicating success, should be true
    print("Get", await redis.string.get("test")) # Get a Python string, returns a string, should be "test1"
    print("Set Or Get", await redis.string.set_or_get("test2", "test2")) # New operation Set Or Get, if key exists, Get, otherwise Set, result should be "test2"

    # String Delete
    print("Set", await redis.string.set("test2", b"1")) # Set a Python bytes, result should be true
    print("Set", await redis.string.set("test3", 1)) # Set a Python int, result should be true
    print("Delete", await redis.string.delete("test2", "test3")) # Delete one or more keys, returns the number of deletions, should be 2

    # String Exists
    print("Exists", await redis.string.exists("test")) # Check if a key exists, returns a boolean, should be true
    print("Exists", await redis.string.exists("test2")) # Check if a key exists, returns a boolean, should be false
    print("Exists", await redis.string.exists("test3")) # Check if a key exists, returns a boolean, should be false

    # String Append
    print("Append", await redis.string.append("test", "1"))  # Append a Python string, returns the length after operation, should be 5+1=6

    # String Length
    print("Len", await redis.string.lens("test")) # Get the length of the string, should be 6

    # Batch Set and Get
    print("Mset", await redis.string.mset({
    "test7": 7,
    "test8": 8,
    "test9": 9
    })) # Batch set, returns a boolean, should be true
    print("Mget", await redis.string.mget("test7", "test8", "test9")) # Batch get, returns a list, should be [7, 8, 9]

    # Simple Cache Usage
    print("Get Cache", await redis.string.get_cache("test")) # Get cache, should be "test1"
    print("Set Cache dict", await redis.string.set_cache("test", {"a": 1.0, "b": 2.0, "c": 3.0})) # Set cache, a Python dict, returns a boolean, should be true
    print("Set Cache pydantic model", await redis.string.set_cache("test1", test_data)) # Set cache, a pydantic model, returns a boolean, should be true
    print("Get Cache ", await redis.string.get_cache("test")) # Get cache, a Python dict, returns a Python dict, should be {"a": 1.0, "b": 2.0, "c": 3.0}
    print("Get Cache", await redis.string.get_cache("test1", bind_pydantic_model=TestModel)) # Get cache, a pydantic model, returns a pydantic model, should be TestModel(field1='value1', field2=123, field3=True)

    ## If bind_pydantic_model is set, returns a pydantic model, otherwise returns a Python dict or list, depending on the value itself.

    # String Number Operations, Increment and Decrement
    print(await redis.string.increase("test3", 2)) # String number operation, increment, returns a string, should be "2"
    print(await redis.string.decrease("test3", 2)) # String number operation, decrement, returns a string, should be "0"

    return {
        "message": "Hello World"
    }
```

### Hash Data Structure

The corresponding method is `redis.hash.`.

```python

@app.get("/hash")
async def hash(redis: RedisDependence):
    test_data = {
        "field1": "value1",
        "field2": 123,
        "field3": True
    } # Set a dictionary

    # Set a hash
    await redis.hash.set_hash("test_hash", test_data) # Set a hash
    print("get_hash", await redis.hash.get_hash("test_hash")) # Get a hash, returns a dictionary, should be {'field1': 'value1', 'field2': '123', 'field3': 'True'}
    print("delete_field", await redis.hash.delete_field("test_hash", "field2")) # Delete a field, returns an integer representing the number of deletions, should be 1
    print("exists_field", await redis.hash.exists_field("test_hash", "field1")) # Check if a field exists, returns a boolean, should be True
    print("exists_field", await redis.hash.exists_field("test_hash", "field2")) # Check if a field exists, returns a boolean, should be False

    class TestModel(BaseModel):
        field1: str
        field2: int
        field3: bool

    test_data = TestModel(field1="value1", field2=123, field3=True) # Set a pydantic model
    await redis.hash.set_hash("test_hash1", test_data) # Set a hash, set pydantic model
    print("get_hash", await redis.hash.get_hash("test_hash1", bind_pydantic_model=TestModel)) # Get a hash, get pydantic model, should be field1='value1' field2=123 field3=True

    return {
        "message": "Hello World"
    }
```

### List Data Structure

The corresponding method is `redis.list.`.

```python
@app.get("/list")
async def list(redis: RedisDependence):
    # List addition
    print("lpush", await redis.list.lpush("test_list", "a", "b", "c")) # List addition, add to the front, returns an integer representing the current length, should be 3
    print("rpush", await redis.list.rpush("test_list", "d", "e")) # List addition, add to the back, returns an integer representing the current length, should be 5

    print("insert_before", await redis.list.linsert_before("test_list", "b", "x")) # List addition, insert before the second parameter, returns an integer representing the current length, should be 6
    print("insert_after", await redis.list.linsert_after("test_list", "b", "x")) # List addition, insert after the second parameter, returns an integer representing the current length, should be 7

    # Get list elements by index
    print("Lindex", await redis.list.lindex("test_list", 0)) # List get, get the first element, returns an element, should be "c"

    # List length
    print("Llen", await redis.list.llen("test_list")) # List length, returns an integer, should be 7

    # List deletion
    print("Lpop", await redis.list.lpop("test_list")) # List deletion, delete from the front, returns an element, should be "c"
    print("Rpop", await redis.list.rpop("test_list")) # List deletion, delete from the back, returns an element, should be "e"

    # List modification
    print("Lset", await redis.list.lset("test_list", 1, "y")) # List modification, modify by index, returns a boolean indicating success, should be True

    # List slicing
    print("Lpush", await redis.list.lpush("test_list", "y", "a", "b", "y", "y", "a", "b")) 
    print("Lrange", await redis.list.lrange("test_list", 0, -1)) # List slicing, returns a list, should be ['b', 'a', 'y', 'y', 'b', 'a', 'y', 'x', 'y', 'x', 'a', 'd']
    print("Lrem", await redis.list.lrem("test_list", 1, "y")) # List deletion, search from the front and delete elements with value "y" (delete count=1), returns an integer representing the number of deletions, should be 1
    print("Lrem", await redis.list.lrem("test_list", -2, "y")) # List deletion, search from the back and delete elements with value "y" (delete count=2), returns an integer representing the number of deletions, should be 2
    print("Ltrim", await redis.list.ltrim("test_list", 0, 1)) # List slicing, slice from 0 to 1, delete others, returns a boolean indicating success, should be True
    async for value in redis.list.list_iterator("test_list"): # List iteration
        print(value)
    
    return {
        "message": "Hello World"
    }
```

### Set Data Structure

The corresponding method is `redis.set.`.

```python

@app.get("/set")
async def set(redis: RedisDependence):
    # Set addition and deletion
    print("Add", await redis.set.add("test_set", "a", "b", "c")) # Set addition, returns a boolean, should be true
    print("Remove", await redis.set.remove("test_set", "b")) # Set deletion, returns a boolean, should be true
    print("Exists", await redis.set.exists("test_set", "a")) # Set check, returns a boolean, should be true

    # Get all members of the set
    print("Get All", await redis.set.get_all("test_set")) # Get all members of the set, returns a set, should be { "c", "a" }

    # Get the length of the set
    print("Length", await redis.set.length("test_set")) # Get the length of the set, returns an integer, should be 2

    # Set intersection, union, and difference operations
    await redis.set.add("another_set", "b", "c", "d") 
    print("Intersection", await redis.set.intersection(["test_set", "another_set"])) # Intersection, returns a set, should be { "c" }
    print("Union", await redis.set.union(["test_set", "another_set"])) # Union, returns a set, should be { "c", "d", "a", "b" }
    print("Difference", await redis.set.difference(["test_set", "another_set"])) # Difference, returns a set, should be { "a" }

    return {
        "message": "Hello World"
    }
```

### Sorted Set Data Structure

The corresponding method is `redis.zset.`.

```python
@app.get("/zset")
async def zset(redis: RedisDependence):

    # Zset addition
    print("Zadd", await redis.zset.add("test_zset", {"a": 1.0, "b": 2.0, "c": 4.0})) # Zset addition, returns an integer representing the number of additions, should be 3
    
    # Zset deletion
    print("Zrem", await redis.zset.remove("test_zset", "b")) # Zset deletion, returns an integer representing the number of deletions, should be 1

    # Zset get
    print("Zscore", await redis.zset.score("test_zset", "a")) # Zset get, get the score of a value, returns a float, should be 1.0
    print("Zrange", await redis.zset.range("test_zset")) # Zset get, by index, returns a list, should be ['a', 'c']
    print("Zrange with scores", await redis.zset.range_with_scores("test_zset")) # Zset get, by index, returns a list, should be [('a', 1.0), ('c', 4.0)]
    print("Zrange_by_score", await redis.zset.range_by_score("test_zset", 1.0, 3.1)) # Zset get, by score, returns a list, should be ['a']
    print("Zrange_by_score with scores", await redis.zset.range_by_score_and_with("test_zset", 1.0, 3.1)) # Zset get, by score, returns a list, should be [('a', 1.0)]
    
    # Zset length
    print("Zlen", await redis.zset.length("test_zset")) # Zset length, returns an integer representing the length of the set, should be 2

    # Zset ranking
    print("Zrank", await redis.zset.rank("test_zset", "a")) # Zset ranking, returns an integer representing the rank of the value, should be 0
    print("Zrank", await redis.zset.rank("test_zset", "c", reverse=True)) # Zset ranking reverse, returns an integer representing the rank of the value, should be 0

    return {
        "message": "Hello World"
    }
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
## Three Common Operations
```python

@app.get("/")
async def get_redis(redis: RedisDependence):
    await redis.expire("test_hash", 10) # Common method to set expiration time for a key
    await redis.delete("test_list") # Common method to delete a key
    return await redis.client.ping()

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