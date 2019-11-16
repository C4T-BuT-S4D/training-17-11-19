#!/usr/bin/env python3

import sys
from random import randint
from time import sleep

from chat_lib import *


def put(host, _flag_id, flag, _vuln):
    mch = CheckMachine(host)

    u1, p1 = mch.register_user()
    s1 = mch.login_user(u1, p1)
    mch.enter_chat(s1)

    u2, p2 = mch.register_user()
    s2 = mch.login_user(u2, p2)
    mch.enter_chat(s2)

    mch.send_message(s1, u2, "Hello!")
    sleep(0.5)
    mch.send_message(s2, u1, "Hello!")
    sleep(0.5)
    mch.send_message(s1, u2, flag)

    cquit(Status.OK, f'{u1}:{p1}:{u2}:{p2}')


def get(host, flag_id, flag, _vuln):
    u1, p1, u2, p2 = flag_id.split(":")
    mch = CheckMachine(host)

    s1 = mch.login_user(u1, p1)
    mch.enter_chat(s1)

    s2 = mch.login_user(u2, p2)
    mch.enter_chat(s2)

    messages1 = mch.get_messages(s1, u2)
    messages2 = mch.get_messages(s2, u1)

    if len(messages1) == 0 or not messages1[-1].get('message') == flag:
        cquit(Status.CORRUPT, 'Could not get flag')

    if len(messages2) == 0 or not messages2[-1].get('message') == flag:
        cquit(Status.CORRUPT, 'Could not get flag')

    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host)

    u1, p1 = mch.register_user()
    s1 = mch.login_user(u1, p1)
    mch.enter_chat(s1)

    u2, p2 = mch.register_user()
    s2 = mch.login_user(u2, p2)
    mch.enter_chat(s2)

    u3, p3 = mch.register_user()
    s3 = mch.login_user(u3, p3)

    l = mch.list_users(s3)

    f1 = False
    f2 = False

    for u in l:
        if u.get('name') == u1:
            f1 = True
        if u.get('name') == u2:
            f2 = True

    if not f1 or not f2:
        cquit(Status.MUMBLE, 'Could not find user on user listing')

    messages = []

    for i in range(10):
        c = randint(1, 2)
        if c == 1:
            sender_s = s1
            receiver_u = u2
        else:
            sender_s = s2
            receiver_u = u1
        message = rnd_string(10)
        mch.send_message(sender_s, receiver_u, message)
        messages.append(message)
        sleep(0.5)

    server_messages1 = mch.get_messages(s1, u2)
    server_messages2 = mch.get_messages(s2, u1)

    for i in range(len(messages)):
        try:
            if messages[i] != server_messages1[i].get('message') or\
               messages[i] != server_messages2[i].get('message'):
                cquit(Status.MUMBLE, 'Could not get sent messages')
        except:
            cquit(Status.MUMBLE, 'Invalid json on messages getting')


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