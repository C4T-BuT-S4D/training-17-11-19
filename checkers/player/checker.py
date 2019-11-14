#!/usr/bin/env python3

import random
import sys

from player_lib import *


def put(host, flag_id, flag, vuln):
    cquit(Status.OK, f'kek')


def get(host, flag_id, flag, vuln):
    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host)
    username, password = mch.register_user()
    sess = mch.login_user(username, password)

    me = mch.get_me(sess)
    assert_eq(username, me['username'], 'Invalid "me" page')
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
        # print(frames[i][8:].decode())
        # print('\n\n\n\n')
        # print(parsed_frames[i].decode())
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
