import os
import time
from contextlib import contextmanager

import redis
from psycopg2 import pool, extras

_redis_storage = None
_db_pool = None


def get_db_pool():
    global _db_pool

    if not _db_pool:
        config = {
            'host': os.environ['POSTGRES_HOST'],
            'port': os.environ['POSTGRES_PORT'],
            'user': os.environ['POSTGRES_USER'],
            'password': os.environ['POSTGRES_PASSWORD'],
            'dbname': os.environ['POSTGRES_DB'],
        }
        _db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=20, **config)

    return _db_pool


def get_redis_storage():
    global _redis_storage

    if not _redis_storage:
        password = os.environ['REDIS_PASSWORD']
        _redis_storage = redis.StrictRedis(host='redis', db=0, password=password)

    return _redis_storage


@contextmanager
def db_cursor(dict_cursor=False):
    db_pool = get_db_pool()
    conn = db_pool.getconn()
    if dict_cursor:
        curs = conn.cursor(cursor_factory=extras.RealDictCursor)
    else:
        curs = conn.cursor()
    try:
        yield conn, curs
    finally:
        curs.close()
        db_pool.putconn(conn)


def await_postgres():
    while True:
        try:
            get_db_pool()
        except Exception as e:
            print('Error connecting to postgres', e)
            time.sleep(3)
        else:
            break
