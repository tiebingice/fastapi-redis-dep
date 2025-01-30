from typing import cast,Awaitable,Mapping,TypeAlias

from redis.asyncio import Redis


ZSetValue: TypeAlias = str| bytes| int | float



class RedisZset:
    def __init__(self, client: Redis):
        self._client: Redis = client

    async def add(self, key: str, members_with_scores: dict[str, ZSetValue]) -> int:
        return await cast(Awaitable[int], self._client.zadd(key, cast(Mapping, members_with_scores)))


    async def remove(self, key: str, *members: str) -> int:
        return await cast(Awaitable[int], self._client.zrem(key, *members))

    async def score(self, key: str, member: str) -> float | None:
        scores=await cast(Awaitable[ZSetValue | None], self._client.zscore(key, member))
        if scores is None:
            return None
        return float(scores)
    
  

    async def range(self, key: str, start: int = 0, stop: int = -1) -> list[str]:
        members = await cast(Awaitable[list[str]], self._client.zrange(key, start, stop, withscores=False))
        return members

    
    async def range_with_scores(self, key: str, start: int = 0, stop: int = -1) -> list[tuple[str, float]]:
        members_with_scores = await cast(Awaitable[list[tuple[str, ZSetValue]]], self._client.zrange(key, start, stop, withscores=True))
        return [
            (member, float(score)) for member, score in members_with_scores
        ]    


    async def length(self, key: str) -> int:
        return await cast(Awaitable[int], self._client.zcard(key))
        

    async def range_by_score(self, key: str, minscore: float, maxscore: float, start: int = 0, num: int = 5) -> list[str]:

        members = await cast(Awaitable[list[str]], self._client.zrangebyscore(key, minscore, maxscore, start=start, num=num,
                                                             withscores=False))

        return members
    
    async def range_by_score_and_with(self, key: str, minscore: float, maxscore: float, start: int = 0, num: int = 5) -> list[str | tuple[str, float]]:
        members = await cast(Awaitable[list[tuple[str, ZSetValue]]], self._client.zrangebyscore(key, minscore, maxscore, start=start, num=num,
                                                             withscores=True))

        return [
            (member, float(score)) for member, score in members
        ]
    

    async def rank(self, key: str, member: str, reverse: bool = False) -> int | None:
        if reverse:
            return await cast(Awaitable[int | None], self._client.zrevrank(key, member))
        else:
            return await cast(Awaitable[int | None], self._client.zrank(key, member))
