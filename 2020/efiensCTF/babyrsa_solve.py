n = 79753459280206880128113574432814937699658173430959080655543409042957247559575129669546574580450020074729891652719995259102247118118129856047047260436761118020607272628218875167846537090248986069614704056782852058656553098641635416733510555297527445944922605886852081480971490040604366056053007281766327844861
p = '1x01x000xx11x01xx0110xxx100xxx1x0xx1x10x010110xx1x1xx0xx0001xx01xx0xxx1xx00xxxx1x0xx0x0x10x11xx100x0xxx10x1x1x01xx00110xx1x1x00xx0x0x11100xx0x11x1x1xxxx1x1xx0x00x01x110xx1001x1x0x1x11xx010x1x100xx0x1x0x1000x0x0x110x1x110x00x01x10001x0x0xxxx000xxx0x1xx011x0x1001x0x0xxx001x1xxx11010xx1xx100x1x00110xx00xx001xx0010xxxx0xxx10110xx1xx1x11xx1x01xx1xxxx00x01x10x1110x1000x0x0xxxx000x0x1110000x1010x1010xxxx1x0xxx0xx0xxx0x111x0x0xxx0x1xxx00x0xxx0xxxx0x11x00x110x00xx1x0x11xxx0x10x110x00xx001111x1x00001xxx01xxx11xxx10x1'
q = '1100xx0xxxxx11x0xxxxxx0x1x1x0xxxxx0x100xx01xxx0xxx0xx0x0xx1000xxx0x111x1xxx0x000111x1xx1xx0x1x010011x1x1x10100x1xxx000x10x1xx01xxx1x0000xx10111xxxxxx010xx1x011x10xxxx0001010110x100xxx0111x000x1xxxx00x00011xx1000x0101x0010xxx001xxxxxxxx1x11xxx0xx0xx11x0xxx01xx00011xx0xx1x1x1x100x1x001xx1x100x01111xxxx100x11xx00010x10xx010xx1xx1x1100x00x0x0x0xx1xxxxxx100x1001x01xx010x100x111x111x1xxx1xxx0x01xxx1xx0xx1x110000xx0x00xx10100x111xxx101x1xxxx1001111xxx101xxxxxxx1001x0xxx01x1100001x001x0001xx1x00x0xx0110x01xx0xx01xx'

p_ = [i for i in p]
q_ = [i for i in q]
L = len(p_)
from Crypto.Util.number import *
c = 69798571987059279536020048590380044210697540311399633826675257935676764846459954894967850784513288877022680859815373044798758357399449803892309076689360603234922881853951574595305273158929170599103698971345765935160435747059203310715064910469854375945380312715370629665433775374987617013660468800917779452238
nn = bin(n)[2:]
ans_p = ['1'] * L
ans_q = ['1'] * L
def bruteforce(i):
    if i > L:
        return
    pp = p_[-i:]
    qq = q_[-i:]
    # print(pp, qq)
    if pp[0] == 'x':
        if qq[0] == 'x':
            for j in range(2):
                for k in range(2):
                    pp[0] = str(j)
                    qq[0] = str(k)
                    p1 = int("".join(pp), 2)
                    q1 = int("".join(qq), 2)
                    # print(bin(p1 * q1)[-i:], nn[-i:])
                    if bin(p1 * q1)[-i:] == nn[-i:]:
                        p_[-i] = str(j)
                        q_[-i] = str(k)
                        if i == L:
                            ptest = int("".join(p_), 2)
                            qtest = int("".join(q_), 2)
                            d = inverse(65537, (ptest-1)*(qtest-1))
                            m = long_to_bytes(c, d, n)
                            if b'EFIENS' in m:
                                print(m)
                        bruteforce(i+1)
                        p_[-i] = 'x'
                        q_[-i] = 'x'
                        # break
        else:
            for j in range(2):
                pp[0] = str(j)
                p1 = int("".join(pp), 2)
                q1 = int("".join(qq), 2)
                # print(bin(p1 * q1)[-i:], nn[-i:])
                if bin(p1 * q1)[-i:] == nn[-i:]:
                    p_[-i] = str(j)
                    if i == L:
                        ptest = int("".join(p_), 2)
                        qtest = int("".join(q_), 2)
                        d = inverse(65537, (ptest-1)*(qtest-1))
                        m = long_to_bytes(pow(c, d, n))
                        if b'EFIENS' in m:
                            print(m)
                    bruteforce(i+1)
                    p_[-i] = 'x'
                    # break
    else:
        if qq[0] == 'x':
            for j in range(2):
                qq[0] = str(j)
                p1 = int("".join(pp), 2)
                q1 = int("".join(qq), 2)
                # print(bin(p1 * q1)[-i:], nn[-i:])
                if bin(p1 * q1)[-i:] == nn[-i:]:
                    q_[-i] = str(j)
                    if i == L:
                        ptest = int("".join(p_), 2)
                        qtest = int("".join(q_), 2)
                        d = inverse(65537, (ptest-1)*(qtest-1))
                        m = long_to_bytes(pow(c, d, n))
                        if b'EFIENS' in m:
                            print(m)
                    bruteforce(i+1)
                    q_[-i] = 'x'
                    # break
        else:
            p1 = int("".join(pp), 2)
            q1 = int("".join(qq), 2)
            # print(i, p1, q1)
            if bin(p1 * q1)[-i:] == nn[-i:]:
                if i == L:
                    ptest = int("".join(p_), 2)
                    qtest = int("".join(q_), 2)
                    d = inverse(65537, (ptest-1)*(qtest-1))
                    m = long_to_bytes(pow(c, d, n))
                    if b'EFIENS' in m:
                        print(m)
                bruteforce(i+1)
                
bruteforce(1)
'''
for i in range(1, L):
    p_ = p.split()
    q_ = q.split()
    pp = p[:(i+1)]
    qq = q[:(i+1)]
    print(pp[-1], qq[-1:])
    t = 0
    if pp[0] == 'x':
        if qq[0] == 'x':
            for j in range(2):
                for k in range(2):
                     pt = str(j) + pp[1:]
                     qt = str(k) + qq[1:]
                     if (int(pt, 2) * int(qt, 2)) % (2**(i+1)) == n % (2**(i+1)):
                         print(pt, qt)
        else:
            for j in range(2):
                pt = str(j) + pp[1:]
                qt = qq
                if (int(pt, 2) * int(qt, 2)) % (2**(i+1)) == n % (2**(i+1)):
                    print(pt, qt)
    else:
        if qq[0] == 'x':
            for j in range(2):
                pt = pp
                qt = str(j) + qq[1:]
                if (int(pt, 2) * int(qt, 2)) % (2**(i+1)) == n % (2**(i+1)):
                    print(pt, qt)
        else:
            pt = pp
            qt = qq
            if (int(pt, 2) * int(qt, 2)) % (2**i) == n % (2**i):
                    print(pt, qt)
    break
'''
