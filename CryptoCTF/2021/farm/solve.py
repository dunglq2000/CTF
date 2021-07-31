from sage.all import *
import string, base64, math

ALPHABET = string.printable[:62] + '\\='

F = list(GF(64))

def keygen(l):
	key = [F[randint(1, 63)] for _ in range(l)] 
	key = math.prod(key) # Optimization the key length :D
	return key

def maptofarm(c):
	assert c in ALPHABET
	return F[ALPHABET.index(c)]

def encrypt(msg, key):
	m64 = base64.b64encode(msg)
	enc, pkey = '', key**5 + key**3 + key**2 + 1
	for m in m64:
		enc += ALPHABET[F.index(pkey * maptofarm(chr(m)))]
	return enc

enc = '805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj'
for k in range(1, 64):
	res = ''
	for e in enc:
		r = F[ALPHABET.index(e)]
		r = (r * F[k] ** -1)
		res += ALPHABET[F.index(r)]
	try:
		pt = base64.b64decode(res.encode())
		if b'CCTF' in pt:
			print(k, pt)
	except:
		pass

'''
for fl in ALPHABET:
	# flag = fl.encode()
	flag = b'CCT'
	for key in range(64):
		pkey = F[key]
		f64 = base64.b64encode(flag)
		ctxt = ''
		for i, f in enumerate(f64):
			ct = ALPHABET[F.index(pkey * maptofarm(chr(f)))]
			ctxt += ct
			if ct == enc[i]:
				print(key, i, ct)
		print('====', ctxt, '====')
	break
'''