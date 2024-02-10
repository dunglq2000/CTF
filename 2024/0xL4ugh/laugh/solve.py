from pwn import process, context, remote
import json
from Crypto.Util.number import isPrime
from sage.all import *

context.log_level = 'Debug'

#pr = process(["python", "challenge.py"])
pr = remote("20.55.48.101", 1337)
pr.recvuntil(b'all input data is in json')

pr.recvuntil(b'option:\t')

pr.sendline(json.dumps({"option": "1"}).encode())

Ns = eval(pr.recvline().strip().decode()[3:])
es = eval(pr.recvline().strip().decode()[3:])

print([int(e).bit_length() for e in es])

Mat = Matrix(ZZ, 4, 7)
for i in range(3):
    Mat[0, i] = es[i]
Mat[0, 3] = 2**512

for i in range(3):
    Mat[i+1, i] = Ns[i]
    Mat[i+1, i+4] = 2**512

N = Mat.LLL()

print(N[0])

d_evil = abs(N[0][3]) // 2**512

assert isPrime(d_evil)

pr.recvuntil(b'option:\t')
pr.sendline(json.dumps({"option": "2"}).encode())

pr.recvuntil(b"Enter your payload:\t")
pr.sendline(str(2**333-1).encode())

res = eval(pr.recvline().strip().decode()[7:])

kres = [r // (2**333) for r in res]

d_goods = [r - k * (2**333 - 1) for r, k in zip(res, kres)]
d_good = None

for r, k in zip(res, kres):
    d_ = r - k * (2**333 - 1)
    if isPrime(d_):
        d_good = k

assert d_good != None

d = d_evil * 2**333 + d_good

pr.recvuntil(b'option:\t')
pr.sendline(json.dumps({"option": "3", "d": int(d)}).encode())

pr.recvuntil(b'2.sign in')
pr.sendline(json.dumps({"option": "1", "user": "user"}).encode())

data = pr.recvline().strip().decode()
data = data.replace("\'", "\"")

print(data, len(data))

idx = data.index("False")
#data = data.replace("false", "true ")

ctx = pr.recvline().strip().decode()

iv, ct = ctx[:32], ctx[32:]
iv, ct = bytes.fromhex(iv), list(bytes.fromhex(ct))

tmp = [int(i).__xor__(int(j)) for i, j in zip(b'False', b'True ')]
for i, j in zip(range(idx, idx + len(tmp)), range(len(tmp))):
    ct[i - 16] = int(ct[i - 16]).__xor__(int(tmp[j]))

pr.recvuntil(b'option:\t')
pr.sendline(json.dumps({"option": "3", "d": int(d)}).encode())

pr.recvuntil(b'2.sign in')
pr.sendline(json.dumps({"option": "2", "token": iv.hex() + bytes(ct).hex()}).encode())

test = pr.recvline().strip().decode()

assert test[:17] == 'Unpadding Error: '

test = test[19:-1]

def convert(st: str):
    result = []
    i = 0
    while i < len(st):
        if st[i:i+2] != "\\x":
            result.append(ord(st[i]))
            i += 1
        else:
            result.append(int(st[i+2:i+4], 16))
            i += 4
    return bytes(result)

pti = convert(test) # P_0'
pti = bytes(p_ ^ d_ for p_, d_ in zip(pti, data[:16].encode())) # XOR with P_0
pti = bytes(p_ ^ i_ for p_, i_ in zip(pti, iv)) # XOR with IV

pr.recvuntil(b'option:\t')
pr.sendline(json.dumps({"option": "3", "d": int(d)}).encode())

pr.recvuntil(b'2.sign in')
pr.sendline(json.dumps({"option": "2", "token": pti.hex() + bytes(ct).hex()}).encode())

pr.recvline()
pr.recvline()
pr.recvline()
pr.recvuntil(b"2.Exit\n")
pr.sendline(json.dumps({"option": "1"}).encode())

print(pr.recvline())

pr.close()

# b'0xL4ugh{cryptocats_B3b0_4nd_M1ndfl4y3r}\n'