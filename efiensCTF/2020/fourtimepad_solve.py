import random
from Crypto.Util.number import *

printable = [chr(i) for i in range(32, 127)]
magic = -2366540547707921699196359399704685795692230503857310199630127241713302904294984638188222048954693422933286057485453364955232326575156580931098343765793 
encrypted_flag = 481730728147477590058623891675498051334529574592495375656331717409768416155349933803891410647003817827440361572464319442970436132820134834740943058323
enc = magic ^ encrypted_flag


def twist(numbers):
    A, B, C, D = numbers
    return ((~B) & (~C)) | ((C) & (~D))
'''

def twist(random_numbers):
    A,B,C,D = random_numbers
    return (~A) ^ (B & C) ^ (C | D)
'''

for s1 in range(256):
    random.seed(s1)
    b = random.getrandbits(500)
    for s2 in range(256):
        random.seed(s2)
        c = random.getrandbits(500)
        for s3 in range(256):
            random.seed(s3)
            d = random.getrandbits(500)
            # a = ~(magic ^ (b & c) ^ (c | d))
            # assert twist([a, b, c, d]) == magic
            # ct = encrypted_flag ^ a ^ b ^ c ^ d
            ct = enc ^ twist((0, b, c, d))
            plaintext = long_to_bytes(ct)
            if b'EFIENS' in plaintext:
                print(plaintext)
                break
