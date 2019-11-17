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

        r = sess.post(f'{self.url}/auth/register', json={'name': username, 'password': password})
        check_response(r, 'Could not register')
        return username, password

    def login_user(self, username, password):
        sess = get_initialized_session()

        r = sess.post(f'{self.url}/auth/login', json={'name': username, 'password': password})
        check_response(r, 'Could not login')

        return sess

    def list_users(self, sess):
        r = sess.get(f'{self.url}/chat/users/')

        check_response(r, 'Could not list users')

        resp = get_json(r, 'Invalid json on user listing')

        assert_in('result', resp, 'Invalid json on user listing')

        return resp['result']

    def add_anime(self, sess, title, description, year=1337, public='0'):
        data = {'title': title, 'description': description, 'year': year, 'public': public}
        r = sess.post(f'{self.url}/db/anime', data=data)
        check_response(r, 'Could not add anime')

        resp = get_json(r, 'Invalid json on create anime')

        assert_eq(True, resp['result'], 'Could not add anime')

        return resp.get('id')

    def find_anime(self, sess, title=None, description=None):
        params = {}
        if title:
            params['title'] = title
        if description:
            params['description'] = description

        r = sess.get(f'{self.url}/db/anime', params=params)
        check_response(r, 'Could not list anime')

        resp = get_json(r, 'Invalid json on list anime')

        return resp['result']

    def add_links(self, sess, anime_id=None, content=None):
        r = sess.post(f'{self.url}/db/anime/{anime_id}', data={'link': content})
        check_response(r, 'Could not add anime link')
        resp = get_json(r, 'Invalid json on create anime')
        assert_eq('ok', resp['result'], 'Could not add anime link')

    def get_anime_detail(self, sess, anime_id):
        r = sess.get(f'{self.url}/db/anime/{anime_id}')
        check_response(r, 'Could not get anime detail')
        resp = get_json(r, 'Invalid json on anime detail')

        return resp.get('result')

    def get_token(self, sess, anime_id):
        details = self.get_anime_detail(sess, anime_id)
        return details.get('access_token')

    def get_links(self, sess, anime_id):
        details = self.get_anime_detail(sess, anime_id)
        return details.get('links')

    def get_my_anime(self, sess):
        r = sess.get(f'{self.url}/db/my_anime')
        check_response(r, 'Could not get my anime')
        resp = get_json(r, 'Invalid json on my anime')
        result = resp.get('result')
        assert_neq(result, None, "Failed to get user's anime")
        return result

    def get_access(self, sess, anime_id, token):
        params = {'anime': anime_id, 'token': token}
        r = sess.get(f'{self.url}/db/get_access', params=params)
        check_response(r, 'Could not get access page')
        resp = get_json(r, 'Invalid json on get access to anime')
        assert_eq(True, resp.get('result'), 'Could not get access by token')
