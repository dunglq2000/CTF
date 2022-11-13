from sage.all import *
from pwn import *

def byte2mat(bs):
    res = []
    bs = bytes.fromhex(bs)
    for b in bs:
        res.extend(list(map(int, bin(b)[2:].rjust(8, "0"))))
    return res

p = process(["python3", "chall.py"])
A = []
for _ in range(128):
    p.sendlineafter(b"Your option> ", b"2")
    ct = p.recvline().strip().decode().split(" ")[-1]
    ct = byte2mat(ct)
    A.append(ct)
    matA = matrix(GF(2), [A[i][:128] for i in range(len(A))])
    #if matA.rank() != 64:
        #break

assert matA.rank() == 64

flag = "0"
for j in range(128, len(A[0]), 128):
    matB = matrix(GF(2), [A[i][j:j+128] for i in range(len(A))])
    if (matB - matA).rank() == 64:
        flag += "0"
    else:
        flag += "1"

flag = [int(flag[i:i+8], 2) for i in range(0, len(flag), 8)]
flag = bytes(flag).hex()
print(flag)
p.sendlineafter(b"Your option> ", b"1")
p.sendlineafter(b" (hex): ", flag.encode())
print(p.recvline())
p.close()
