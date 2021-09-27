from sock import Sock
from base64 import b64decode
from string import printable
from Crypto.Cipher import AES

FLAGLEN = 16

key = b"!_SECRETSOURCE_!"
so = Sock("pwn-2021.duc.tf", 31914)
while len(key) < 16:
    payload = b"A"*(15-len(key))
    so.read_until(b"Enter plaintext:\n")
    so.send_line(payload)
    ct = b64decode(so.read_line().strip())
    # print("Bruteforce at %d with ciphertext %s" % (i, ct))
    for c in printable:
        so.read_until(b"Enter plaintext:\n")
        so.send_line(payload + key + str.encode(c))
        ctt = b64decode(so.read_line().strip())
        if ctt[:48] == ct[:48]:
            print("Found %c" % c)
            key += str.encode(c)
            break
    print(key)
    
so.read_until("Enter plaintext:\n")
so.send_line(b"")
ct = so.read_line().strip()
ct = b64decode(ct)
assert len(key) == 16
aes = AES.new(key, AES.MODE_ECB)
print(aes.decrypt(ct))
# DUCTF{ECB_M0DE_K3YP4D_D474_L34k}
