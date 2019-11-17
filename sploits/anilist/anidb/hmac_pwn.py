#!/usr/bin/env python3

import sys

from anidb_lib import CheckMachine

host = sys.argv[1]

mch = CheckMachine(host)
u, p = mch.register_user()
sess = mch.login_user(u, p)

animes = mch.find_anime(sess)

animes = [x.get('id') for x in animes]

for a in animes:
    r = sess.get(f"http://{host}:8000/api/db/get_access?anime[]={a}&token=")
    print(r.url)

    print(mch.get_anime_detail(sess, a))

