cipher = b"gh}w_{aPDSmk$ch&r+Ah-&F|\x14z\x11P\x15\x10\x1dR\x1e"
flag = ""
for i in range(len(cipher)):
	flag += chr((cipher[i] + 2) ^ (i + 10))
print(flag)