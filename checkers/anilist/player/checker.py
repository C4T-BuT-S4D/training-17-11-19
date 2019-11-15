#!/usr/bin/env python3

import random
import sys

import requests

from player_lib import *


def put(host, _flag_id, flag, _vuln):
    mch = CheckMachine(host)

    frames = list(map(mch.load_local_letter, flag))
    name, password = mch.register_user()
    sess = mch.login_user(name, password)
    token = mch.upload_frames(sess, frames)

    cquit(Status.OK, f'{name}:{password}:{token}')


def get(host, flag_id, flag, _vuln):
    mch = CheckMachine(host)

    name, password, token = flag_id.split(':')
    sess = mch.login_user(name, password)

    frames = list(map(mch.load_local_letter, flag))

    returned_frames = mch.get_frames(sess, token, 0, len(frames) - 1)
    assert_eq(
        len(frames), len(returned_frames),
        'Invalid number of frames returned',
        status=Status.CORRUPT,
    )

    parsed_frames = mch.parse_frames(sess, returned_frames)
    assert_eq(
        len(frames), len(parsed_frames),
        'Invalid number of frames returned from parser',
        status=Status.CORRUPT,
    )

    for i in range(len(frames)):
        assert_eq(
            len(frames[i][8:]), len(parsed_frames[i]),
            'Invalid frame from parser',
            status=Status.CORRUPT,
        )
        assert_eq(
            frames[i][8:], parsed_frames[i],
            'Invalid frame from parser',
            status=Status.CORRUPT,
        )

    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host)
    name, password = mch.register_user()
    sess = mch.login_user(name, password)

    me = mch.get_me(sess)
    assert_eq(name, me['name'], 'Invalid "me" page')
    assert_in('id', me, 'Invalid "me" page')

    video = random.randint(1, 10)
    frames_start = random.randint(0, 8400)
    frames_end = random.randint(frames_start + 30, frames_start + 200)
    frames_indices = list(range(frames_start, frames_end + 1))
    frames = mch.load_local_frames(video, frames_indices)

    token = mch.upload_frames(sess, frames)
    returned_frames = mch.get_frames(sess, token, 0, len(frames) - 1)
    assert_eq(len(frames), len(returned_frames), 'Invalid number of frames returned')
    for i in range(len(frames)):
        assert_eq(mch.compress(frames[i][8:]), returned_frames[i], 'Invalid frame compression')

    parsed_frames = mch.parse_frames(sess, returned_frames)
    assert_eq(len(frames), len(parsed_frames), 'Invalid number of frames returned from parser')

    for i in range(len(frames)):
        assert_eq(len(frames[i][8:]), len(parsed_frames[i]), 'Invalid frame from parser')
        assert_eq(frames[i][8:], parsed_frames[i], 'Invalid frame from parser')

    cquit(Status.OK)


if __name__ == '__main__':
    action, *args = sys.argv[1:]
    try:
        if action == "check":
            host, = args
            check(host)
        elif action == "put":
            host, flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)
        elif action == "get":
            host, flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)
        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))
