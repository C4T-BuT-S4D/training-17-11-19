import secrets

import httpx
from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route('/api/player/init_upload/', methods=['GET'])
async def init_upload(_request):
    upload_token = secrets.token_hex(16)
    return json({'token': upload_token})


@app.route('/api/player/upload_chunk/<token>/', methods=['POST'])
async def upload_chunk(request, token):
    data = request.json
    r_start = data['start']
    frames = data['frames']
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


@app.route('/api/player/get_chunk/<token>/', methods=['POST'])
async def get_chunk(request, token):
    data = request.args
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
