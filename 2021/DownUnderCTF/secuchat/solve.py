import sqlite3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from itertools import product
from Crypto.Util.number import *

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

con = sqlite3.connect("secuchat.db")

cur = con.cursor()

cur.execute("SELECT * FROM User")
users = cur.fetchall()
usernames = [user[0] for user in users]
keys = [RSA.importKey(user[1]).n for user in users]
for i in range(len(keys)):
	for j in range(i+1, len(keys)):
		p, q = keys[i], keys[j]
		g = gcd(p, q)
		if g < p and g > 1:
			idx, jdx = i, j
			print(i, j)
			# break

# print("Users have private key: ", users[idx][0], users[jdx][1])
g = gcd(keys[idx], keys[jdx])
keyi = g, keys[idx] // g
keyj = g, keys[jdx] // g
di = inverse(65537, (keyi[0] - 1) * (keyi[1] - 1))
dj = inverse(65537, (keyj[0] - 1) * (keyj[1] - 1))
keyi = RSA.construct((keys[idx], 65537, di))
keyi = PKCS1_OAEP.new(keyi)
keyj = RSA.construct((keys[jdx], 65537, dj))

cur.execute("SELECT * FROM Conversation")
convers = cur.fetchall()

for conver in convers:
	if conver[1] == usernames[idx]:
		print("Initiator i", conver)
		cur.execute(f"SELECT * FROM Message WHERE (conversation={conver[0]} and from_initiator=1)")
		msg = cur.fetchall()
		for m in msg:
			cur.execute(f"SELECT * FROM Parameters WHERE (id={m[3]-1})")
			params = cur.fetchall()
			for param in params:
				aes_key = keyi.decrypt(param[1])
				iv = param[3]
				aes = AES.new(aes_key, AES.MODE_CBC, iv)
				print(aes.decrypt(m[4]))
	elif conver[1] == usernames[jdx]:
		print("Initiator j", conver)
	elif conver[2] == usernames[idx]:
		print("Peer i", conver)
	elif conver[2] == usernames[jdx]:
		print("Peer j", conver)

con.close()