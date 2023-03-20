from sage.all import *
from itertools import product
from Crypto.Util.number import long_to_bytes
from Crypto.Util.strxor import strxor

def Z2kDH_init(private_exponent):
	"""
	Computes the public result by taking the generator 5 to the private exponent, then removing the last 2 bits
	private_exponent must be a positive integer less than 2^256
	"""
	return pow(5, private_exponent, modulus) // 4

def Z2kDH_exchange(public_result, private_exponent):
	"""
	Computes the shared secret by taking the sender's public result to the receiver's private exponent, then removing the last 2 bits
	public_result must be a non-negative integer less than 2^256
	private_exponent must be a positive integer less than 2^256
	"""
	return pow(public_result * 4 + 1, private_exponent, modulus) // 4

g = 5
p = 2**258
modulus = p

c1 = int('99edb8ed8892c664350acbd5d35346b9b77dedfae758190cd0544f2ea7312e81', 16)
c2 = int('40716941a673bbda0cc8f67fdf89cd1cfcf22a92fe509411d5fd37d4cb926afd', 16)

#c1 = Mod(c1, p).log(Mod(g, p))
#c2 = Mod(c2, p).log(Mod(g, p))

for i, j in product(range(4), repeat=2):
	ct1 = c1 * 4 + i
	ct2 = c2 * 4 + j
	try:
		p1 = discrete_log(Mod(ct1, p), Mod(g, p))
		p2 = discrete_log(Mod(ct2, p), Mod(g, p))
		# print(long_to_bytes(int(p1)) + long_to_bytes(int(p2)))
		# print(strxor(long_to_bytes(int(p1)), long_to_bytes(int(p2))))
		shared1 = Z2kDH_exchange(c2, int(p1))
		shared2 = Z2kDH_exchange(c1, int(p2))
		print(shared1, shared2)
		assert shared1 == shared2
		print(long_to_bytes(shared1))
	except:
		continue
		