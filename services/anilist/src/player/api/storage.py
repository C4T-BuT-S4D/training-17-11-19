import asyncio
import os

import aioredis
import asyncpg

_async_redis_pool = None
_async_db_conn = None


async def get_async_redis_pool():
    global _async_redis_pool

    if not _async_redis_pool:
        loop = asyncio.get_event_loop()

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


async def get_db_conn():
    global _async_db_conn

    if not _async_db_conn:
        config = {
            'host': os.environ['POSTGRES_HOST'],
            'port': os.environ['POSTGRES_PORT'],
            'user': os.environ['POSTGRES_USER'],
            'password': os.environ['POSTGRES_PASSWORD'],
            'database': os.environ['POSTGRES_DB'],
        }

        _async_db_conn = await asyncpg.connect(**config)

    return _async_db_conn
