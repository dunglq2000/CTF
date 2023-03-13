from sage.modules.free_module_integer import IntegerLattice
from random import randint
from itertools import starmap
from operator import mul
from pwn import remote, process, context
import math
import random

# Babai's Nearest Plane algorithm
# from: http://mslc.ctf.su/wp/plaidctf-2016-sexec-crypto-300/
def Babai_closest_vector(M, G, target):
  small = target
  for _ in range(1):
    for i in reversed(range(M.nrows())):
      c = ((small * G[i]) / (G[i] * G[i])).round()
      small -= M[i] * c
  return target - small

def check(array, mod, width):
    for x in array[0]:
        if not (x < 4 * width or mod-x < 4 * width):
            return False
    return True

def gen_errors(width, mod, size):
    values = [i for i in range(-4*width, 4*width)]
    weights = [math.e ** (-math.pi * (i / width)**2) for i in values]
    def dg(mod):
        return random.choices(values, weights)[0] % mod
    return [dg(mod) for _ in range(size[1])]


q = 10**9 + 7
width = 6

# context.log_level = 'Debug'
proc = remote("puffer.utctf.live", int(8484))
# proc = process(["python3", "main_fixed.py"])

'''
A_bar = AA[:-1]
b_values = AA[-1]

A_values = [[0 for i in range(len(AA))] for j in range(len(AA[0]))]

for i in range(len(A_bar)):
  for j in range(len(A_bar[0])):
    A_values[j][i] = A_bar[i][j]

A = matrix(ZZ, m + n, m)
for i in range(m):
  A[i, i] = q
for x in range(m):
  for y in range(n):
    A[m + y, x] = A_values[x][y]

lattice = IntegerLattice(A, lll_reduce=True)
print("LLL done")
gram = lattice.reduced_basis.gram_schmidt()[0]
target = vector(ZZ, b_values)
res = Babai_closest_vector(lattice.reduced_basis, gram, target)
print("Closest Vector: {}".format(res))

R = IntegerModRing(q)
M = Matrix(R, A_values)
ingredients = M.solve_right(res)

print("Ingredients: {}".format(ingredients))

for row, b in zip(A_values, b_values):
  effect = sum(starmap(mul, zip(map(int, ingredients), row))) % q
  assert(abs(b - effect) < 2 ** 37)
'''

def solve(r):
  print("Solving round {0}".format(r))
  proc.recvline()
  proc.recvline()
  proc.sendline(b"10")
  m = 10*min(r, 5)
  n = 30*min(r, 5)
  AAA = []
  for _ in range(10):
    proc.recvline()
    AAA.append(eval(proc.recvline().strip().decode()))
  for t, AA in enumerate(AAA):
    for _ in range(10): 
      matA = Matrix(ZZ, m+n+2, n)
      bb = gen_errors(width, q, (m+1, n))
      vecB = vector(ZZ, bb)

      for i in range(m+1):
        for j in range(n):
          # print(i, j)
          matA[i,j] = AA[i][j]

      for i in range(n):
        matA[m+1,i] = bb[i]

      for i in range(n):
        matA[m+2+i,i] = q

      matB = matA.LLL()

      for vec in matB:
        # print(vec)
        if check([list((vec[:m+1] * matA[:m+1]).change_ring(Zmod(q)))], q, width):
          print("Hura")
          proc.sendlineafter(b"(1-10)", str(t+1).encode())
          proc.sendlineafter(b"integers)\n", " ".join(map(str, vec[:m+1])).encode())

          print(proc.recvline())
          return
      
for r in range(1, 11):
   solve(r)

print(proc.recvline())

proc.close()

# b'utflag{mY_l34Rn1Ng_h4s_3rr0rs_2f11a84e}\n'