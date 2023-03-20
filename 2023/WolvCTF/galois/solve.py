from sage.all import *
from pwn import remote, process, context
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.strxor import strxor
import re
from Crypto.Cipher import AES

# context.log_level = 'Debug'

F2 = GF(2)['x']
x = F2.gen()
modulus = x**128 + x**7 + x**2 + x + 1
F = GF(2**128, name='x', modulus=modulus)
PR = PolynomialRing(F, 'z')
z = PR.gen()

def GF_mult(x, y):
    product = 0
    for i in range(127, -1, -1):
        product ^= x * ((y >> i) & 1)
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    return product

def H_mult(H, val):
    product = 0
    for i in range(16):
        product ^= GF_mult(H, (val & 0xFF) << (8 * i))
        val >>= 8
    return product

def GHASH(H, A, C):
    C_len = len(C)
    A_padded = bytes_to_long(A + b'\x00' * (16 - len(A) % 16))
    if C_len % 16 != 0:
        C += b'\x00' * (16 - C_len % 16)

    tag = H_mult(H, A_padded)

    for i in range(0, len(C) // 16):
        tag ^= bytes_to_long(C[i*16:i*16+16])
        tag = H_mult(H, tag)

    tag ^= bytes_to_long((8*len(A)).to_bytes(8, 'big') + (8*C_len).to_bytes(8, 'big'))
    tag = H_mult(H, tag)

    return tag

def aes_ecb(key, plaintext):
    return AES.new(key, AES.MODE_ECB).encrypt(plaintext)

def byte_to_pol(block):
    n = int.from_bytes(block, 'big')
    nn = list(map(int, bin(n)[2:].zfill(128)))
    pol = sum(j*x**i for i, j in enumerate(nn))
    return F(pol)

def pol_to_byte(element):
    coeff = element.polynomial().coefficients(sparse=False)
    coeff = coeff + [0] * (128 - len(coeff))
    num = int(''.join(list(map(str, coeff))), 2)
    return int.to_bytes(num, 16, 'big')

def decrypt(H, ct, tag):
    # ct = bytes.fromhex(ct)
    assert(len(ct) % 16 == 0)
    numBlocks = len(ct) // AES_BLOCK_SIZE

    # tag = bytes.fromhex(tag)
    assert(len(tag) == 16)

    hkey = H
    #enc = b''
    #for i in range(numBlocks + 1):
    #   enc += ct0[(i+1)*16:(i+2)*16]
    enc = ct0

    # print(len(enc), len(ct0))

    pt = b''

    for i in range(1, numBlocks + 1):
        pt += strxor(
            enc[i * AES_BLOCK_SIZE: (i+1) * AES_BLOCK_SIZE],
            ct[(i-1) * AES_BLOCK_SIZE: i * AES_BLOCK_SIZE])
        
    authTag = strxor(
        enc[:AES_BLOCK_SIZE],
        long_to_bytes(GHASH(bytes_to_long(hkey), header, ct)))

    if(pt == message):
        if(authTag == tag):
            print("OK")
            return True
        else:
            print("Whoops, that doesn't seem to be authentic!")
    else:
        print("Hmm, that's not the message I was looking for...")

#pr = process(["python3", "server.py"])
pr = remote("galois.wolvctf.io", 1337)

AES_BLOCK_SIZE = 16
header = b'WolvCTFCertified'
message = b'heythisisasupersecretsupersecret'

pr.sendlineafter(b"> ", b"1")
pr.sendlineafter(b"> ", long_to_bytes(0, 16).hex())
pr.sendlineafter(b"> ", bytes(48).hex())

ct0 = re.findall(r"CT:  (.*)", pr.recvline().strip().decode())[0]
tag0 = re.findall(r"TAG:  (.*)", pr.recvline().strip().decode())[0]
ct0, tag0 = bytes.fromhex(ct0), bytes.fromhex(tag0)

pr.sendlineafter(b"> ", b"1")
pr.sendlineafter(b"> ", long_to_bytes(2, 16).hex())
pr.sendlineafter(b"> ", b'')

# ct2 = b''
pr.recvline()
tag2 = re.findall(r"TAG:  (.*)", pr.recvline().strip().decode())[0]

tag2 = bytes.fromhex(tag2)

header_pad = header + b'\x00' * (16 - len(header) % 16)
L = (8*len(header)).to_bytes(8, 'big') + bytes(8)

print(header_pad)

# f = byte_to_pol(header) * z**2 + byte_to_pol(L) * z + byte_to_pol(tag2) + byte_to_pol(ct0[16:32])
f = byte_to_pol(L) * z + byte_to_pol(tag2) + byte_to_pol(ct0[16:32])

roots = f.roots()

assert len(roots) > 0

for root in roots:
    H = pol_to_byte(root[0])

    print(H)

    ctx = b''

    for i in range(0, len(ct0)-16, 16):
        ctx += strxor(ct0[i+16:i+32], message[i:i+16])

    '''
    tag = 0
    for i in range(0, len(ctx), 16):
        tag = tag * H + byte_to_pol(ctx[i:i+16])

    tag = tag * H + byte_to_pol((8*len(header)).to_bytes(8, 'big') + (8*len(ctx)).to_bytes(8, 'big'))
    tag = tag * H + byte_to_pol(ct0[0:16])

    tag = pol_to_byte(tag)
    '''

    tag = strxor(ct0[:16], 
                long_to_bytes(GHASH(bytes_to_long(H), header, ctx)))
    
    if decrypt(H, ctx, tag):
        print("Found")

        pr.sendlineafter(b"> ", b"2")
        pr.sendlineafter(b"> ", int.to_bytes(int(1), 16, 'big').hex())
        pr.sendlineafter(b"> ", ctx.hex())
        pr.sendlineafter(b"> ", tag.hex())

        print(pr.recvline())
        break

# b'wctf{th13_sup3r_s3cr3t_13nt_v3ry_s3cr3t}\n'