#!/usr/bin/env python3
import hashlib
import sys

import hmac

from anidb_lib import CheckMachine

host = sys.argv[1]

mch = CheckMachine(host)
u, p = mch.register_user()
sess = mch.login_user(u, p)

animes = mch.find_anime(sess)

animes = [x.get('id') for x in animes]
for a in animes:
    t = hmac.new(b"abacaba", a.encode(), hashlib.sha256).hexdigest()
    print(t)
    r = sess.get(f"http://{host}:8000/api/db/get_access?anime={a}&token={t}")
    print(mch.get_anime_detail(sess, a))
