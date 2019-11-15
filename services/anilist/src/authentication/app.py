import json
import os
import re
import secrets
from functools import wraps

from flask import Flask, request, abort, jsonify, make_response

import storage

storage.await_postgres()

app = Flask('__name__')
app.secret_key = os.environ['SECRET_KEY']


@app.before_first_request
def init_db():
    users_query = '''CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255)
    )'''

    anime_uploads_query = '''CREATE TABLE IF NOT EXISTS anime_uploads(
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        token VARCHAR(64) NOT NULL
    )'''

    with storage.db_cursor() as (conn, curs):
        curs.execute(users_query)
        curs.execute(anime_uploads_query)
        conn.commit()


def get_error(message, code):
    return jsonify(dict(error=message)), code


def get_user():
    sess = request.cookies.get('session')
    if not sess:
        abort(401)
    with storage.get_redis_storage().pipeline() as pipeline:
        user_exists, user = pipeline.exists(sess).get(sess).execute()

    if not user_exists:
        abort(401)

    try:
        user = json.loads(user.decode())
    except (UnicodeDecodeError, json.JSONDecodeError):
        abort(401)

    return user


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        get_user()
        return f(*args, **kwargs)

    return wrapper


def assert_json_post(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.json is None:
            abort(400)
        return f(*args, **kwargs)

    return wrapper


@app.route('/api/auth/login', methods=['POST'])
@assert_json_post
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return get_error('Specify both username and password', 400)

    with storage.db_cursor(dict_cursor=True) as (conn, curs):
        query = 'SELECT * FROM users WHERE username=%s AND password=%s'
        curs.execute(query, (username, password))
        user = curs.fetchone()

    if not user:
        return get_error('Invalid credentials', 403)

    session = secrets.token_hex(32)
    with storage.get_redis_storage().pipeline() as pipeline:
        pipeline.set(session, json.dumps(dict(user))).execute()

    resp = make_response(jsonify('ok'))
    resp.set_cookie('session', session)
    return resp


@app.route('/api/auth/register', methods=['POST'])
@assert_json_post
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return get_error('Specify both username and password', 400)

    username = re.sub('[\\x00-\\x1f!@#$%^&*()]', '', username)

    with storage.db_cursor(dict_cursor=True) as (conn, curs):
        query = 'SELECT * FROM users WHERE username=%s'
        curs.execute(query, (username,))
        user = curs.fetchone()

    if user:
        return get_error('Username taken', 400)

    with storage.db_cursor(dict_cursor=True) as (conn, curs):
        query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        curs.execute(query, (username, password))
        conn.commit()

    return jsonify('ok')


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    sess = request.cookies.get('session')
    if not sess:
        return jsonify('ok')

    resp = make_response(jsonify('ok'))
    resp.set_cookie('session', '', expires=0)
    return resp


@app.route('/api/auth/me', methods=['GET'])
@login_required
def me():
    user = get_user()
    return jsonify(user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
