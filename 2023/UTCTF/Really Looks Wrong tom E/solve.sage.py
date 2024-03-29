

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_4 = Integer(4); _sage_const_2 = Integer(2); _sage_const_10 = Integer(10); _sage_const_9 = Integer(9); _sage_const_7 = Integer(7); _sage_const_6 = Integer(6); _sage_const_8484 = Integer(8484); _sage_const_37 = Integer(37); _sage_const_5 = Integer(5); _sage_const_30 = Integer(30); _sage_const_11 = Integer(11); _sage_const_50 = Integer(50); _sage_const_150 = Integer(150)
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
  for _ in range(_sage_const_1 ):
    for i in reversed(range(M.nrows())):
      c = ((small * G[i]) / (G[i] * G[i])).round()
      small -= M[i] * c
  return target - small

def check(array, mod, width):
    for x in array[_sage_const_0 ]:
        if not (x < _sage_const_4  * width or mod-x < _sage_const_4  * width):
            return False
    return True

def gen_errors(width, mod, size):
    values = [i for i in range(-_sage_const_4 *width, _sage_const_4 *width)]
    weights = [math.e ** (-math.pi * (i / width)**_sage_const_2 ) for i in values]
    def dg(mod):
        return random.choices(values, weights)[_sage_const_0 ] % mod
    return [dg(mod) for _ in range(size[_sage_const_1 ])]


q = _sage_const_10 **_sage_const_9  + _sage_const_7 
width = _sage_const_6 

# context.log_level = 'Debug'

proc = remote("puffer.utctf.live", int(_sage_const_8484 ))
# proc = process(["python3", "main_fixed.py"])

def solve2(AA, m, n):
  A_bar = AA[:-_sage_const_1 ]
  b_values = AA[-_sage_const_1 ]

  print(len(A_bar), len(A_bar[_sage_const_0 ]))

  A_values = [[_sage_const_0  for i in range(len(AA))] for j in range(len(AA[_sage_const_0 ]))]

  for i in range(len(A_bar)):
    for j in range(len(A_bar[_sage_const_0 ])):
      A_values[j][i] = A_bar[i][j]
  m, n = n, m

  A = matrix(ZZ, m + n, m)
  for i in range(m):
    A[i, i] = q
  for x in range(m):
    for y in range(n):
      A[m + y, x] = A_values[x][y]

  lattice = IntegerLattice(A, lll_reduce=True)
  print("LLL done")
  gram = lattice.reduced_basis.gram_schmidt()[_sage_const_0 ]
  target = vector(ZZ, b_values)
  res = Babai_closest_vector(lattice.reduced_basis, gram, target)
  print("Closest Vector: {}".format(res))

  R = IntegerModRing(q)
  M = Matrix(R, A_values)
  ingredients = M.solve_right(res)

  print("Ingredients: {}".format(ingredients))

  for row, b in zip(A_values, b_values):
    effect = sum(starmap(mul, zip(map(int, ingredients), row))) % q
    assert(abs(b - effect) < _sage_const_2  ** _sage_const_37 )

  eT = target - M * ingredients
  print("et = {}".format(eT))


def solve(r):
  print("Solving round {0}".format(r))
  proc.recvline()
  proc.recvline()
  proc.sendline(b"10")
  m = _sage_const_10 *min(r, _sage_const_5 )
  n = _sage_const_30 *min(r, _sage_const_5 )
  AAA = []
  for _ in range(_sage_const_10 ):
    proc.recvline()
    AAA.append(eval(proc.recvline().strip().decode()))
  for t, AA in enumerate(AAA):
    for _ in range(_sage_const_1 ):
      if r == _sage_const_5  and t == _sage_const_0 :
        global Ax
        # solve2(AA, m, n)
        Ax = AA
      proc.sendlineafter(b"(1-10)", str(t+_sage_const_1 ).encode())
      proc.sendlineafter(b"integers)\n", " ".join(map(str, [_sage_const_0 ] * (m+_sage_const_1 ))).encode())

      print(proc.recvline())
      return
      '''
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
      '''


Ax = None

for r in range(_sage_const_1 , _sage_const_11 ):
   solve(r)

print(proc.recvline())

proc.close()

solve2(Ax, _sage_const_50 , _sage_const_150 )

# b'utflag{mY_l34Rn1Ng_h4s_3rr0rs_2f11a84e}\n'

