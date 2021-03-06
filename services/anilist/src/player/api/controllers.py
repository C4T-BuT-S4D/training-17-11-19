import secrets

import ujson
from sanic.exceptions import abort

import storage


async def get_current_user(request):
    if 'user' in request:
        return request['user']

    sess = request.cookies.get('session')
    if not sess:
        abort(401)

    redis = await storage.get_async_redis_pool()
    tr = redis.multi_exec()
    tr.exists(sess)
    tr.get(sess)
    user_exists, user = await tr.execute()

    if not user_exists:
        abort(401)

    try:
        user = ujson.loads(user.decode())
    except (UnicodeDecodeError, ValueError):
        abort(401)

    request['user'] = user
    return user


async def add_user_upload(request):
    user = await get_current_user(request)
    upload_token = secrets.token_hex(16)
    name = request.json.get('name', '')

    conn = await storage.get_db_conn()
    query = '''INSERT INTO anime_uploads (user_id, name, token) VALUES ($1, $2, $3)'''
    await conn.execute(query, user['id'], name, upload_token)

    query = '''SELECT * FROM anime_uploads WHERE token=$1'''
    result = await conn.fetchrow(query, upload_token)
    result = dict(result)

    redis = await storage.get_async_redis_pool()
    await redis.set(upload_token, ujson.dumps(result))

    return upload_token


async def get_upload(upload_token):
    redis = await storage.get_async_redis_pool()
    upload = await redis.get(upload_token)
    if not upload:
        return None
    return ujson.loads(upload.decode())


async def user_upload_exists_or_404(request, token):
    user = await get_current_user(request)
    upload = await get_upload(token)
    if not upload or upload.get('user_id') != user['id']:
        abort(404)
    return True


async def get_upload_or_404(token):
    upload = await get_upload(token)
    if not upload:
        abort(404)
    return upload


async def get_user_uploads(request):
    user = await get_current_user(request)
    conn = await storage.get_db_conn()
    query = '''SELECT * FROM anime_uploads WHERE user_id = $1'''
    rows = await conn.fetch(query, user['id'])
    return list(map(dict, rows))
