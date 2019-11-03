import aioredis

_async_redis_pool = None


async def get_async_redis_pool(loop):
    global _async_redis_pool

    if not _async_redis_pool:
        address = f'redis://redis:6379'
        db = 0
        _async_redis_pool = await aioredis.create_redis_pool(
            address=address,
            db=db,
            minsize=5,
            maxsize=15,
            loop=loop,
        )

    return _async_redis_pool
