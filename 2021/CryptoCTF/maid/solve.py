from sock import Sock
import random
import gmpy2
from Crypto.Util.number import inverse, long_to_bytes

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

while True:
	so = Sock('04.cr.yp.toc.tf:38010')

	ct = [random.getrandbits(2000) for _ in range(2)]
	pt = []

	for i in range(2):
		so.read_until(b'[Q]uit\n')
		so.send_line(b'd')
		so.read_line()
		so.send_line(str(ct[i]).encode())
		pt.append(int(so.read_line().strip().split(b' ')[-1]))

	'''
	for i in range(2):
		so.read_until(b'[Q]uit\n')
		so.send_line(b'e')
		so.read_line()
		so.send_line(str(pt[i]).encode())
		assert int(so.read_line().strip().split(b' ')[-1]) in ct
	'''

	p2 = gcd(pt[0] ** 2 - ct[0], pt[1] ** 2 - ct[1])
	if 1024 < p2.bit_length() < 3072:
		p, t = gmpy2.iroot(p2, 2)
		if t:
			print(p)
			so.read_until(b'[Q]uit\n')
			so.send_line(b's')
			flag = int(so.read_line().strip().split(b' ')[-1])
			pt = [random.getrandbits(2000) for _ in range(2)]
			ct = []
			for i in range(2):
				so.read_until(b'[Q]uit\n')
				so.send_line(b'e')
				so.read_line()
				so.send_line(str(pt[i]).encode())
				ct.append(int(so.read_line().strip().split(b' ')[-1]))
			pubkey = gcd(pt[0] ** 2 - ct[0], pt[1] ** 2 - ct[1])
			if pubkey % (p ** 2) != 0: continue
			q = pubkey // (p ** 2)
			d = inverse(65537, (p - 1) * (q - 1))
			m = pow(flag, d, p * q)
			if b'CCTF' in long_to_bytes(m):
				print(long_to_bytes(m))
				break

	so.close()