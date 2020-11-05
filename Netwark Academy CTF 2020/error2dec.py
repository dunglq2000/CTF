from functools import reduce
c = "011010100100111010010011110010110110110010010010011100001111101101101000110100110000010011100010001001110000110111100100110111111110101000101011011010000111100001000111001110010111001101011100011101111011100111111000101001110000011101011110010111111110001101110000011010010011101010010110101010001000011100101110100000101110000010110010100010101111010110001101001100001000101100100011111000100001110001100110001110101011010001111001111001101001110000110000111011001000010110001001010111111010101100010011011001110110111001100111101001001100110100100110001000101010111011101010110000111001011100111001"
c = [int(i) for i in c]
f = ""
flag = ""
code = [c[i:i+15] for i in range(0, len(c), 15)]
for k, i in enumerate(code):
    for ran in  range(len(i)):
        tmp = [j for j in i]
        tmp[ran] = tmp[ran] ^ 1
        parity = [tmp[13], tmp[8], tmp[7], tmp[5]][::-1]
        parity = [str(j) for j in parity]
        tmp[13], tmp[8], tmp[7], tmp[5] = -1, -1, -1, -1
        tmp = [j for j in tmp if j >= 0]
        for j in range(4):
            tmp.insert(2**j-1, 0)
        # print(tmp)
        p = reduce(lambda a,b: a^b, [j+1 for j, bit in enumerate(tmp) if bit])
        p = list(reversed(list(str(format(p, "04b")))))
        if p == parity:
            char = []
            for j in range(len(tmp)):
                if j in [0, 1, 3, 7]: continue
                char.append(str(tmp[j]))
            f += "".join(char)
for i in range(0, len(f), 8):
    flag += chr(int(f[i:i+8], 2))
print(flag)

'''
i = [int(j) for j in list("01101110011")]
# i = [int(j) for j in list("00001011000")]
# i = [int(j) for j in list("11011101000")]
# i = [int(j) for j in list("11001100111")]

start =  0
for j in range(4):
    i.insert(2 ** j - 1, 0)

parity = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(i) if bit])
parity = list(reversed(list(str(format(parity, "04b"))))) # separates number into individual binary bits

i = [k for j, k in enumerate(i) if j not in (0, 1, 3, 7)]
for j in range(4):
    print(parity[j])
test = [int(j) for j in list(c[15*start: 15*(start+1)])]
summ = 0
for j in i:
    if j == 1:
        summ += 1
print(i)
temp = []
for ind in range(15):
    tmp = [j for j in test]
    tmp[ind] = int(not tmp[ind])

    s = 0
    for t in tmp:
        if t == 1:
            s += 1
    if s - summ == 2:
        # print(ind, tmp)
        temp.append(tmp)
maxval = 11
haha = []
for tmp in temp:
    t = [j for j in i]
    for i1 in range(maxval):
        t.insert(i1, 1)
        for i2 in range(maxval):
            t.insert(i2, 0)
            for i3 in range(maxval):
                t.insert(i3, 0)
                for i4 in range(maxval):
                    t.insert(i4, 1)
                    if t == tmp:
                        print(i1, i2, i3, i4, tmp)
                        haha.append((i1, i2, i3, i4))
                    del t[i4]
                del t[i3]
            del t[i2]
        del t[i1]
print(haha)
'''
