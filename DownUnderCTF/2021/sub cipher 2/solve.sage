from string import ascii_lowercase, digits
CHARSET = "DUCTF{}_!?'" + ascii_lowercase + digits
n = len(CHARSET)
P.<x> = PolynomialRing(GF(n))
enc = "Ujyw5dnFofaou0au3nx3Cn84"
a = "DUCTF{}"
b = enc[:6] + enc[-1]
mat = [[CHARSET.index(x)^i for i in range(7)] for x in a]
print(mat)
matA = Matrix(GF(n), mat)
matB = vector(GF(n), [CHARSET.index(y) for y in b])
coeff = matA.inverse() * matB
f = sum([x^i * j for i, j in enumerate(coeff)])
print(f)

flag = []
def brute(i):
	if i == len(enc):
		print("".join(flag))
	else:
		g = f - CHARSET.index(enc[i])
		for _ in g.roots():
			flag.append(CHARSET[_[0]])
			brute(i+1)
			flag.pop()
brute(0)
# DUCTF{go0d_0l'_l4gr4ng3}