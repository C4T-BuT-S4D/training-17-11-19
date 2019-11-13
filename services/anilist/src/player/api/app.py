from functools import wraps

import httpx
from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json

import controllers

app = Sanic()


def login_required(f):
    @wraps(f)
    async def wrapper(request, *args, **kwargs):
        await controllers.get_current_user(request)
        return await f(request, *args, **kwargs)

    return wrapper


@app.route('/api/player/init_upload/', methods=['GET'])
@login_required
async def init_upload(request):
    upload_token = await controllers.add_user_upload(request)
    return json({'token': upload_token})


@app.route('/api/player/upload_chunk/', methods=['POST'])
@login_required
async def upload_chunk(request):
    data = request.json

    token = data['token']
    r_start = data['start']
    frames = data['frames']

    await controllers.upload_exists_or_404(request, token)

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f'http://player_internal:5000/create/',
            json={
                'start': r_start,
                'prefix': token,
                'frames': frames,
            })
    try:
        return json({'response': r.json()})
    except Exception as e:
        return json({'error': str(e)}, status=400)


@app.route('/api/player/get_chunk/', methods=['GET'])
@login_required
async def get_chunk(request):
    data = request.args
    token = data.get('token', '')

    if not token:
        abort(400)

    await controllers.upload_exists_or_404(request, token)

    start = int(data.get('start', 0))
    end = int(data.get('end', start + 5))

    if end - start > 5:
        end = start + 5

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f'http://player_internal:5000/get/{token}/',
            params={
                'start': start,
                'end': end,
            })
    try:
        return json({'response': r.json()})
    except Exception as e:
        return json({'error': str(e)}, status=400)


@app.route('/api/player/parse_chunk/', methods=['POST'])
@login_required
async def get_chunk(request):
    data = request.json
    frames = data['frames']
    if not all(frames):
        return json({'error': 'empty frame'}, status=400)

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f'http://player_internal:5000/parse/',
            json={
                'frames': frames,
            })
    try:
        return json({'response': r.json()})
    except Exception as e:
        return json({'error': str(e)}, status=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, workers=4)
