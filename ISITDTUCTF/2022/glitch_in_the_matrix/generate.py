from sage.all import *

while True:
    A = random_matrix(GF(2), 128, 128)
    if A.rank() == 128:
        break

with open("basis", "w") as f:
    for vec in A:
        f.write("".join(list(map(str, list(vec)))) + "\n")

f.close()