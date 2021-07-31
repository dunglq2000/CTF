#!/usr/bin/env python

from Crypto.Util.number import *

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n

with open('g.enc', 'rb') as f:
    gg = bytes_to_long(f.read())

with open('h.enc', 'rb') as f:
    hh = bytes_to_long(f.read())

g, h = [], []
while gg > 0:
    g.append(gg % 5)
    gg //= 5

g.reverse()
while hh > 0:
    h.append(hh % 5)
    hh //= 5

h.reverse()

for lenf in range(160, 10000):
    c = nextPrime(lenf >> 2)
    al = len(g) - c
    bl = len(h) - c
    l = gcd(al, bl)
    if lenf == l:
        break

a = nextPrime(lenf)
b = nextPrime(a)
c = nextPrime(lenf >> 2)

for _ in [g, h]:
    for i in range(len(_) - c - 1, -1, -1): _[i] -= _[i+c]
    assert all(_[i] == 0 for i in range(c))

g, h = g[c:], h[c:]

assert len(g) % a == 0
flag = g[:lenf]

for i in range(len(flag) - 2, -1, -1):
    flag[i] -= flag[i+1]

ff = int(''.join(map(str, flag)), 2)
print(long_to_bytes(ff))
