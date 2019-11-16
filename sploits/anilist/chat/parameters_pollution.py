#!/usr/bin/env python3

import sys
from chat_lib import *

ip = sys.argv[1]

mch = CheckMachine(ip)

u, p = mch.register_user()
s = mch.login_user(u, p)
mch.enter_chat(s)

l = mch.list_users(s)

for u1 in l:
    try:
        for u2 in l:
            try:
                r = s.post(f'http://{ip}:8000/api/chat/get_messages/', json={
                    "to": u2.get("name"),
                    "from": u1.get("name")
                })

                print(r.content, flush=True)
            except:
                pass
    except:
        pass