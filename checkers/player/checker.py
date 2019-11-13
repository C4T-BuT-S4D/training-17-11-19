#!/usr/bin/env python3

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
