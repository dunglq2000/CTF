from pwn import *
def legendre(a, p):
        result = pow(a, (p-1)/2, p)
        if result == p-1:
                return -1
        return 1
r = remote('guess.q.2020.volgactf.ru', 7777)

d = r.recv(1024)
key = d.strip().split(', ')
gx = int(key[1][6:])
p = int(key[2][:-1])
key_sqrt = legendre(gx, p)

for tries in xrange(1000):
        print(tries)
        d = r.recv(1024)
        ciphertext = d.strip().split(', ')
        print(ciphertext)
        if ciphertext[0][-1] == 'L':
                gr = int(ciphertext[0][1:-1])
        else:
                gr = int(ciphertext[0][1:])
        if ciphertext[1][-2] == 'L':
                c = int(ciphertext[1][:-2])
        else:
                c = int(ciphertext[1][:-1])
        print(gr, c)
        c1_sqrt = legendre(gr, p)
        if key_sqrt == 1 or c1_sqrt == 1:
                if legendre(c, p) == -1:
                        r.sendline('0')
                else:
                        r.sendline('1')
        else:
                if legendre(c, p) == 1:
                        r.sendline('0')
                else:
                        r.sendline('1')

d = r.recv(1024)
print(d)
r.close()