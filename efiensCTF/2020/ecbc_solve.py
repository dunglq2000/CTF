import socket
from Crypto.Util.number import *
'''
host, port = '128.199.234.122', 3333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
payload = (b'a' * 32).hex()
print(payload)
s.connect((host, port))
s.send(payload.encode() + b'\n')
res = s.recv(40960)
print(len(res.split(b'\n')))
'''
f = open('ecbd.txt', 'r')
d = f.read()
f.close()

res = d.split('\n')
flag = ''
for r in res:
    if r[:32] == r[32:]:
        flag = '1' + flag
    else:
        flag = '0' + flag

print(long_to_bytes(int(flag, 2)))
