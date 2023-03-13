from sage.all import *
from pwn import remote, process, context

# context.log_level = "Debug"

# p = process(["python3", "encrypt_pub.py"])

def xor(a, b):
        return bytes(x^y for x, y in zip(a, b))

while True:
    p = remote("puffer.utctf.live", 52584)

    def vec_to_byte(v):
        result = []
        for i in range(0, len(v), 8):
            result.append(int("".join(list(map(str, v[i:i+8]))), 2))
        return bytes(result)

    def byte_to_vec(b):
        result = []
        for i in range(len(b)):
            b_ = b[i]
            for _ in range(8):
                result.append(b_ % 2)
                b_ //= 2
        return result

    PP = []
    CC = []

    p0 = [0] * 128
    p.sendlineafter(b"string: ", vec_to_byte(p0).hex())
    c0 = p.recvline().strip().decode()
    c0 = bytes.fromhex(c0)

    for _ in range(128):
        row = [0] * 128
        row[_] = 1
        p.sendlineafter(b"string: ", vec_to_byte(row).hex())
        ct = p.recvline().strip().decode()

        ct = xor(bytes.fromhex(ct), c0)
        PP.append(row)
        CC.append(byte_to_vec(ct))

    PP = matrix(GF(2), PP)
    CC = matrix(GF(2), CC)

    if not CC.is_invertible():
        p.close()
        continue

    AA = CC.inverse() * PP

    

    ctx = bytes.fromhex("3384f87f781c394b79e331510540a4125a371b057b058d8e793521cd43f2ae94")
    ptx1 = vec_to_byte(vector(GF(2), byte_to_vec(xor(ctx[:16], c0))) * AA)
    ptx2 = vec_to_byte(vector(GF(2), byte_to_vec(xor(ctx[16:32], c0))) * AA)                                      

    print(ptx1, ptx2)
    break

'''

bb = vec_to_byte([1, 0] * 64)
print(bb)
print(byte_to_vec(bb))
'''