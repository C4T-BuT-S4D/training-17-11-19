import asyncio
import base64
import concurrent.futures
import os

import aniparser
from sanic import Sanic
from sanic.response import json

app = Sanic()


def create_frame(prefix, number, frame):
    frame = base64.b64decode(frame)
    fname = f'/anime/{prefix}/{number}.frame'
    ani = aniparser.Aniparser(frame, fname)
    ani.create()


def get_frame(prefix, number):
    fname = f'/anime/{prefix}/{number}.frame'
    try:
        with open(fname, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        return number, ''
    else:
        return number, base64.b64encode(data)


def parse_frame(frame, number):
    frame = base64.b64decode(frame.encode())
    ani = aniparser.Aniparser(frame, '')
    return number, base64.b64encode(ani.parse())


@app.route('/create/', methods=['POST'])
async def create(request):
    data = request.json
    frames = data['frames']
    prefix = data['prefix']
    start = data['start']

    folder = f'/anime/{prefix}'
    os.makedirs(folder, exist_ok=True)

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    tasks = [
        loop.run_in_executor(executor, create_frame, prefix, start + i, frame)
        for i, frame in enumerate(frames)
    ]

    await asyncio.wait(tasks)

    return json('ok')


# noinspection PyUnresolvedReferences
@app.route('/get/<prefix>/', methods=['GET'])
async def get(request, prefix):
    data = request.args
    r_start = int(data['start'][0])
    r_end = int(data['end'][0])

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    tasks = [
        loop.run_in_executor(executor, get_frame, prefix, number)
        for number in range(r_start, r_end + 1)
    ]

    completed, _ = await asyncio.wait(tasks)
    frames = [task.result() for task in completed]
    frames = map(lambda x: x[1], sorted(frames))

    return json(frames)


@app.route('/parse/', methods=['POST'])
async def get(request):
    data = request.json
    frames = data['frames']

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    tasks = [
        loop.run_in_executor(executor, parse_frame, frame, i)
        for i, frame in enumerate(frames)
    ]

    completed, _ = await asyncio.wait(tasks)
    frames = [task.result() for task in completed]
    frames = map(lambda x: x[1], sorted(frames))

    return json(frames)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, workers=4)
