enc = 5550332817876280162274999855997378479609235817133438293571677699650886802393479724923012712512679874728166741238894341948016359931375508700911359897203801700186950730629587624939700035031277025534500760060328480444149259318830785583493
tmp = enc
three = ""
from functools import reduce
import operator
from Crypto.Util.number import *

def comb(n, k):
	if k > n :
		return 0
	k = min(k, n - k)
	u = reduce(operator.mul, range(n, n - k, -1), 1)
	d = reduce(operator.mul, range(1, k + 1), 1)
	return u // d 

while enc > 0:
	three += str(enc % 3)
	enc //= 3
m = 0
for i in three[::-1]:
	m *= 2
	if i == "1":
		m += 1
	elif i == "2":
		m -= 1

ciphertext = bin(m)[2:]
n = len(ciphertext)
for k_start in range(0, n):
	k = k_start
	msg = 0
	for i in range(n, 0, -1):
		if ciphertext[i-1] == "1":
			k += 1
			msg += comb(n - i, k)
	m1 = long_to_bytes(msg)
	m2 = long_to_bytes(msg - comb(n - i, k))
	if b'CCTF' in m1:
		print(m1)
	if b'CCTF' in m2:
		print(m2)