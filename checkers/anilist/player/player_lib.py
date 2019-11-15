import base64
import binascii
import gzip
import os
import struct

from checklib import *

PORT = 8000
MAX_DEN = 255
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/api'

    def __init__(self, host):
        self.host = host
        self.port = PORT

    @staticmethod
    def compress(data):
        result = b''
        cur_char = 0
        cur_cnt = 0

        for c in data:
            if c == cur_char:
                cur_cnt += 1
            elif cur_cnt == 0:
                cur_char = c
                cur_cnt = 1
            else:
                result += bytes([cur_cnt, cur_char])
                cur_char = c
                cur_cnt = 1

            if cur_cnt == MAX_DEN:
                result += bytes([cur_cnt, cur_char])
                cur_char = 0
                cur_cnt = 0

        if cur_cnt:
            result += bytes([cur_cnt, cur_char])

        return struct.pack('<Q', len(result)) + result

    def register_user(self):
        username = rnd_username()
        password = rnd_password()
        r = get_initialized_session().post(
            f'{self.url}/auth/register',
            json={'username': username, 'password': password},
        )
        check_response(r, 'Could not register')
        return username, password

    def login_user(self, username, password):
        sess = get_initialized_session()

        r = sess.post(f'{self.url}/auth/login', json={'username': username, 'password': password})
        check_response(r, 'Could not login')

        return sess

    def get_me(self, sess):
        r = sess.get(f'{self.url}/auth/me')
        check_response(r, 'Could not get Me')
        return get_json(r, 'Could not get Me')

    def get_upload_token(self, sess):
        r = sess.get(f'{self.url}/player/init_upload/')
        check_response(r, 'Could not get upload token')
        data = get_json(r, 'Could not get upload token')
        assert_in('token', data, 'Could not get upload token')
        return data['token']

    @staticmethod
    def load_local_frames(video, numbers):
        result = []
        for num in numbers:
            frame_name = str(num).zfill(5) + '.frame.gz'
            frame_path = os.path.join(BASE_DIR, 'frames_compressed', str(video), frame_name)
            with open(frame_path, 'rb') as f:
                data = gzip.decompress(f.read())
            result.append(data)
        return result

    @staticmethod
    def load_local_letter(letter):
        name = base64.b64encode(letter.encode()).decode().replace('=', '')
        frame_name = f'{name}.frame'
        frame_path = os.path.join(BASE_DIR, 'letters_frames', frame_name)
        with open(frame_path, 'rb') as f:
            data = f.read()
        return data

    def upload_frames(self, sess, frames):
        blocks = [
            list(map(
                lambda x: base64.b64encode(x).decode(),
                frames[i:i + 10],
            )) for i in range(0, len(frames), 10)
        ]

        token = self.get_upload_token(sess)
        for i, block in enumerate(blocks):
            r = sess.post(
                f'{self.url}/player/upload_chunk/',
                json={
                    'token': token,
                    'frames': block,
                    'start': i * 10,
                })
            check_response(r, 'Could not upload anime chunk')

        return token

    def get_frames(self, sess, token, start, end):
        frames = []
        for i in range(start, end + 1, 30):
            cur_start = i
            cur_end = min(end, i + 29)
            r = sess.get(
                f'{self.url}/player/get_chunk/',
                params={
                    'token': token,
                    'start': cur_start,
                    'end': cur_end,
                }
            )
            check_response(r, 'Could not get anime chunk')
            data = get_json(r, 'Could not get anime chunk')
            assert_in('response', data, 'Could not get anime chunk')
            assert_eq(type(data['response']), list, 'Could not get anime chunk')

            for frame in data['response']:
                with handle_exception(
                        binascii.Error,
                        'Could not get anime chunk',
                        'Error decoding frame'
                ):
                    frames.append(base64.b64decode(frame))
        return frames

    def parse_frames(self, sess, frames):
        result = []
        for i in range(0, len(frames), 30):
            block = frames[i:i + 30]
            r = sess.post(
                f'{self.url}/player/parse_chunk/',
                json={
                    'frames': list(map(
                        lambda x: base64.b64encode(x).decode(),
                        block,
                    ))
                }
            )
            check_response(r, 'Could not parse anime chunk')
            data = get_json(r, 'Could not parse anime chunk')
            assert_in('response', data, 'Could not parse anime chunk')
            assert_eq(type(data['response']), list, 'Could not parse anime chunk')

            for frame in data['response']:
                with handle_exception(
                        binascii.Error,
                        'Could not parse anime chunk',
                        'Error decoding frame'
                ):
                    result.append(base64.b64decode(frame))
        return result
