from functools import reduce
c = [int(i) for i in "010011011010011010100011011001111110111101000101010011110111010101110110100110001100000111011101100100101111011010110001010011001110011010101111010111111010111010110111010111110110100110011011001101101101011101000111101000110100001010110100100001110110011110111011111101111000001100100011011010010111101100100100000011001101000001001010100000100111001011111101"]
code = [c[i:i+15] for i in range(0, len(c), 15)]
f = ""
flag = ""
for k, i in enumerate(code):
    for ran in range(len(i)):
        tmp = [j for j in i]
        tmp[ran] = tmp[ran] ^ 1
        parity = ["1"] * 4
        for j in range(4):
            if tmp[2 ** j - 1] == 0:
                parity[j] = "0"
            tmp[2 ** j - 1] = 0
        
        p = reduce(lambda a, b: a^b, [j+1 for j, bit in enumerate(tmp) if bit])
        p = list(reversed(list(str(format(p, "04b")))))
        if p == parity:
            char = []
            for j in range(len(tmp)):
                if j in [0, 1, 3, 7]: continue
                char.append(str(tmp[j]))
            f += "".join(char)
            break
for i in range(0, len(f), 8):
    flag += chr(int(f[i:i+8], 2))
print(flag)
