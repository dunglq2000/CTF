from sage.all import *
from pwn import remote, process, context
from Crypto.Util.number import isPrime, long_to_bytes, bytes_to_long, inverse
import re
import random

context.log_level = 'Debug'

# p = process(["python3", "server.py"])
p = remote("puffer.utctf.live", 52548)
data = p.recvline().strip().decode()
n, e = re.findall(f"Alice's pk: (.*) (.*)", data)[0]
m, s = map(int, p.recvline().strip().decode().split(" "))

print(m, s)

primes = []
for i in range(10000):
    if isPrime(i):
        primes.append(i)
# p_weak = 2
'''
while True:
    p_weak = 2
    for prime in primes:
        p_weak *= prime**random.randint(1, 200)
    p_weak += 1
    if isPrime(p_weak) and p_weak > s:
        print(p_weak)
        break
'''

p_weak = 65537**128
assert p_weak > s
d_prime = discrete_log(Mod(s, p_weak), Mod(m, p_weak))
print(d_prime)
assert gcd(d_prime, euler_phi(p_weak)) == 1
e_prime = pow(d_prime, -1, euler_phi(p_weak))

p.sendlineafter(b"n': ", str(p_weak).encode())
p.sendlineafter(b"e': ", str(e_prime).encode())
p.sendlineafter(b"d': ", str(d_prime).encode())

p.recvline()
p.recvline()
p.recvline()

p.close()

# b'Flag: utflag{hey_wait_signature_forgery_is_illegal}\n'