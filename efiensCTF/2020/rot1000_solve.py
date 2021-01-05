from base64 import b64decode
from string import ascii_uppercase as ALPHABET
def rot(s, num):
    return ''.join(ALPHABET[(ALPHABET.index(x) + num) % len(ALPHABET)] if x in ALPHABET else x for x in s)

cipher = "Z1kqFGZqFhoDLSE8VAhpBWVANhIBPQ4wEAgbA2cJDn0db2EKOSECHQNvdBo7CAIwAy0hAWsDDWs="
cipher = b64decode(cipher)

for i in range(32, 128):
    l = bytearray(cipher)
    c = [0] * len(cipher)
    c[-1] = i
    for j in range(len(cipher)):
        c[j] = l[(j-1)%len(cipher)] ^ c[(j-1)%len(cipher)]
    try:
        res = b64decode(bytes(c)).decode()
        # print(res)
        for key in range(26):
            flag = rot(res, key)
            # print(key)
            if 'EFIEN' in flag:
                print(flag)
    except:
        continue
