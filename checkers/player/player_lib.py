import requests
from checklib import *

PORT = 8000


class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/api/auth'

    def __init__(self, host):
        self.host = host
        self.port = PORT

    def register_user(self):
        username = rnd_username()
        password = rnd_password()

        r = requests.post(f'{self.url}/register', json={'username': username, 'password': password})
        check_response(r, 'Could not register')
        return username, password

    def login_user(self, username, password):
        sess = get_initialized_session()

        r = sess.post(f'{self.url}/login', json={'username': username, 'password': password})
        check_response(r, 'Could not login')

        return sess

    def get_me(self, sess):
        r = sess.get(f'{self.url}/me')
        check_response(r, 'Could not get Me')
        return get_json(r, 'Could not get Me')
