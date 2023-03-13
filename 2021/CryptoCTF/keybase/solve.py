from sock import Sock
from tqdm import tqdm
from itertools import product
from Crypto.Cipher import AES

so = Sock('01.cr.yp.toc.tf:17010')

def xor(a, b):
	return bytes([x^y for x, y in zip(a, b)])

so.read_until(b'[Q]uit\n')
so.send_line(b'g')

flag = so.read_line().strip().split(b' ')[-1]
flag = bytes.fromhex(flag.decode())

pt = [b'a' * 16 + b'b' * 16, b'a' * 16 + b'c' * 16]
ct = []
i = 0
while len(ct) < 2:
	so.read_until(b'[Q]uit\n')
	so.send_line(b't')
	so.read_line()
	so.send_line(pt[i])

	enc = so.read_line().strip().split(b' ')[-1]
	key = so.read_line().strip().split(b' ')[-1][:-4]
	print(key)
	if enc.index(b'*') < 3:
		ct.append(bytes.fromhex(enc[32:].decode()))
		i += 1

key = bytes.fromhex(key.decode())
for i, j in tqdm(product(range(256), repeat=2)):
	k = key + bytes([i, j])
	dec1 = AES.new(k, AES.MODE_ECB)
	dec2 = AES.new(k, AES.MODE_ECB)
	if xor(dec1.decrypt(ct[0]), b'b' * 16) == xor(dec2.decrypt(ct[1]), b'c' * 16):
		final_key = k
		break

so.read_until(b'[Q]uit\n')
so.send_line(b't')
so.read_line()
so.send_line(b'\x00' * 32)

enc = so.read_line().strip().split(b' ')[-1]
key = so.read_line()
enc = bytes.fromhex(enc[32:].decode())
iv = AES.new(final_key, AES.MODE_ECB).decrypt(AES.new(final_key, AES.MODE_ECB).decrypt(enc))

aes = AES.new(final_key, AES.MODE_CBC, iv)
print(aes.decrypt(flag))
so.close()