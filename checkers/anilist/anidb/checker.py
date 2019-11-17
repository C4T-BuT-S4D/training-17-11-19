#!/usr/bin/env python3

import sys
from random import randint
from time import sleep
import random
from anidb_lib import *

random_titles = open('titles.txt').readlines()


def random_title():
    return random.choice(random_titles).strip()


def random_description(title):
    fmt = [
        "Story about: {}",
        "It's all about {} adventures",
        "It's definitely not a Boku no Pico"
    ]
    t = ' '.join(title.split()[:-1])
    return random.choice(fmt).format(title)


def put(host, _flag_id, flag, _vuln):
    mch = CheckMachine(host)

    u, p = mch.register_user()
    s = mch.login_user(u, p)

    title = random_title() + ' ' + rnd_string(3, '0123456789')

    description = random_description(title)
    mch.add_anime(s, title, description, randint(1998, 2021), '0')

    # Get last user's anime
    my_anime = mch.get_my_anime(s)
    my_anime = [x for x in my_anime if x['description'] == description]

    if len(my_anime) < 1:
        cquit(Status.MUMBLE, 'Coudn get user anime')

    ani_id = my_anime[-1]['id']

    mch.add_links(s, ani_id, flag)

    cquit(Status.OK, f'{u}:{p}:{ani_id}')


def get(host, flag_id, flag, _vuln):
    u, p, ani_id = flag_id.strip().split(":")
    mch = CheckMachine(host)

    s1 = mch.login_user(u, p)

    res = mch.get_anime_detail(s1, ani_id)

    links = [x.get('content') for x in res['links']]

    if flag not in links:
        cquit(Status.CORRUPT, 'Failed to find anime link')
    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host)

    u1, p1 = mch.register_user()

    s1 = mch.login_user(u1, p1)

    title = random_title() + ' ' + rnd_string(3, '0123456789')

    description = random_description(title)
    mch.add_anime(s1, title, description, randint(1998, 2021), '1')

    # Get last user's anime
    my_anime = mch.get_my_anime(s1)
    my_anime = [x for x in my_anime if x['description'] == description]

    if len(my_anime) < 1:
        cquit(Status.MUMBLE, 'Coudn get user anime')

    # Check anime search
    ani_search = []
    if randint(0, 1) % 2 == 0:
        ani_search = mch.find_anime(s1, title=title[:-2])
    else:
        ani_search = mch.find_anime(s1, description=description[:-2])

    assert_in(title, [x.get('title') for x in ani_search], 'Failed to find anime by fields')

    u1_ani_id = my_anime[-1]['id']

    u1_link = rnd_string(10)

    mch.add_links(s1, u1_ani_id, u1_link)

    # User 2

    u2, p2 = mch.register_user()
    s2 = mch.login_user(u2, p2)

    description = random_description(title)
    title = random_title() + ' ' + rnd_string(3, '0123456789')
    mch.add_anime(s2, title, description, randint(1998, 2021), '0')
    # Get last user's anime
    my_anime = mch.get_my_anime(s2)
    my_anime = [x for x in my_anime if x['description'] == description]

    if len(my_anime) < 1:
        cquit(Status.MUMBLE, 'Coudn get user anime')

    u2_ani_id = my_anime[-1]['id']

    u2_link = rnd_string(10)

    mch.add_links(s2, u2_ani_id, u2_link)

    # User2 get's user1 public link
    links = [x.get('content') for x in mch.get_links(s2, u1_ani_id)]

    assert_in(u1_link, links, 'Failed to get public link')

    # User1 get's user2 private link by token
    u2_token = mch.get_token(s2, u2_ani_id)

    mch.get_access(s1, u2_ani_id, u2_token)

    links = [x.get('content') for x in mch.get_links(s1, u2_ani_id)]

    assert_in(u2_link, links, 'Failed to get private links by token')

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
