import requests
from checklib import *

PORT = 8000

class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/api'

    def __init__(self, host):
        self.host = host
        self.port = PORT

    def register_user(self):
        username = rnd_username()
        password = rnd_password()

        sess = get_initialized_session()

        r = sess.post(f'{self.url}/auth/register', json={'username': username, 'password': password})
        check_response(r, 'Could not register')
        return username, password

    def login_user(self, username, password):
        sess = get_initialized_session()

        r = sess.post(f'{self.url}/auth/login', json={'username': username, 'password': password})
        check_response(r, 'Could not login')

        return sess

    def list_users(self, sess):
        r = sess.get(f'{self.url}/chat/users/')

        check_response(r, 'Could not list users')

        resp = get_json(r, 'Invalid json on user listing')

        assert_in('result', resp, 'Invalid json on user listing')

        return resp['result']

    def enter_chat(self, sess):
        r = sess.post(f'{self.url}/chat/enter/')

        check_response(r, 'Could not enter chat')

        resp = get_json(r, 'Invalid json on chat entering')

        assert_in('result', resp, 'Invalid json on chat entering')

        assert_eq('ok', resp['result'], 'Invalid json on chat entering')

    def send_message(self, sess, to, message):
        r = sess.post(f'{self.url}/chat/send_message/', json={
            "to": to,
            "message": message
        })

        check_response(r, 'Could not send message')

        resp = get_json(r, 'Invalid json on message sending')

        assert_in('result', resp, 'Invalid json on message sending')

        assert_eq('ok', resp['result'], 'Invalid json on message sending')

    def get_messages(self, sess, to):
        r = sess.get(f'{self.url}/chat/get_messages/', json={
            "to": to
        })

        check_response(r, 'Could not get messages')

        resp = get_json(r, 'Invalid json on messages getting')

        assert_in('result', resp, 'Invalid json on messages getting')

        return resp['result']