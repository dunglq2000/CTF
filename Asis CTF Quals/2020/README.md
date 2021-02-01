# ASIS CTF Quals 2020

Well, this CTF is both interesting and hard. I only solved 2 problems in cryptography and this is my writeup for those challenges.

### Baby RSA

**Description**

All babies love [RSA](baby_rsa.txz). How about you? 😂

**Solution**

We have 2 files: a python file to encrypt, and text file containing output.

```python
#!/usr/bin/python

from Crypto.Util.number import *
import random
from flag import flag

nbit = 512
while True:
	p = getPrime(nbit)
	q = getPrime(nbit)
	e, n = 65537, p*q
	phi = (p-1)*(q-1)
	d = inverse(e, phi)
	r = random.randint(12, 19)
	if (d-1) % (1 << r) == 0:
		break

s, t = random.randint(1, min(p, q)), random.randint(1, min(p, q))
t_p = pow(s*p + 1, (d-1)/(1 << r), n)
t_q = pow(t*q + 4, (d-1)/(1 << r), n)

print 'n =', n
print 't_p =', t_p
print 't_q =', t_q
print 'enc =', pow(bytes_to_long(flag), e, n)
```

This challenge looks like typical RSA, except that (d-1) % (2^r) = 0 with some random value **r**.

And we have **t_p = (s*p + 1) ^ ((d-1) // 2^r) mod n** and **t_q = (t*q + 4) ^ ((d-1) // 2^r) mod n**. Well, it looks complicated and I was stucked for a few hours. Then I realised that, if **a = b mod n** with **n = p*q**, then **a = b mod p**.

Using this result, I have:

**t_p = (s*p + 1) ^ ((d-1) // 2^r) mod p**. Because **p = 0 mod p**, **t_p = 1 mod p**.

Therefore, **p** is greatest common divisor of **n** and **t_p - 1**, so I find **p** and then recover **q**, finally having result.

```python
n = 10594734342063566757448883321293669290587889620265586736339477212834603215495912433611144868846006156969270740855007264519632640641698642134252272607634933572167074297087706060885814882562940246513589425206930711731882822983635474686630558630207534121750609979878270286275038737837128131581881266426871686835017263726047271960106044197708707310947840827099436585066447299264829120559315794262731576114771746189786467883424574016648249716997628251427198814515283524719060137118861718653529700994985114658591731819116128152893001811343820147174516271545881541496467750752863683867477159692651266291345654483269128390649
t_p = 4519048305944870673996667250268978888991017018344606790335970757895844518537213438462551754870798014432500599516098452334333141083371363892434537397146761661356351987492551545141544282333284496356154689853566589087098714992334239545021777497521910627396112225599188792518283722610007089616240235553136331948312118820778466109157166814076918897321333302212037091468294236737664634236652872694643742513694231865411343972158511561161110552791654692064067926570244885476257516034078495033460959374008589773105321047878659565315394819180209475120634087455397672140885519817817257776910144945634993354823069305663576529148
t_q = 4223555135826151977468024279774194480800715262404098289320039500346723919877497179817129350823600662852132753483649104908356177392498638581546631861434234853762982271617144142856310134474982641587194459504721444158968027785611189945247212188754878851655525470022211101581388965272172510931958506487803857506055606348311364630088719304677522811373637015860200879231944374131649311811899458517619132770984593620802230131001429508873143491237281184088018483168411150471501405713386021109286000921074215502701541654045498583231623256365217713761284163181132635382837375055449383413664576886036963978338681516186909796419
enc = 5548605244436176056181226780712792626658031554693210613227037883659685322461405771085980865371756818537836556724405699867834352918413810459894692455739712787293493925926704951363016528075548052788176859617001319579989667391737106534619373230550539705242471496840327096240228287029720859133747702679648464160040864448646353875953946451194177148020357408296263967558099653116183721335233575474288724063742809047676165474538954797346185329962114447585306058828989433687341976816521575673147671067412234404782485540629504019524293885245673723057009189296634321892220944915880530683285446919795527111871615036653620565630
def gcd(a, b):
	while b:
		a, b = b, a % b
	return a
p = gcd(t_p - 1, n)
assert n % p == 0
q = n // p
from Crypto.Util.number import *
d = inverse(65537, (p-1)*(q-1))
m = pow(enc, d, n)
print(long_to_bytes(m))
```

**Flag: ASIS{baby___RSA___f0r_W4rM_uP}**

### Tripolar

**Description**

We all know about magnetic dipoles. Have you ever thought about magnetic [tripoles](tripolar.txz)?

**Solution**

```python
#!/usr/bin/python

from Crypto.Util.number import *
from hashlib import sha1
from flag import flag

def crow(x, y, z):
	return (x**3 + 3*(x + 2)*y**2 + y**3 + 3*(x + y + 1)*z**2 + z**3 + 6*x**2 + (3*x**2 + 12*x + 5)*y + (3*x**2 + 6*(x + 1)*y + 3*y**2 + 6*x + 2)*z + 11*x) // 6

def keygen(nbit):
	p, q, r = [getPrime(nbit) for _ in range(3)]
	pk = crow(p, q, r)
	return (p, q, r, pk)

def encrypt(msg, key):
	p, q, r, pk = key
	_msg = bytes_to_long(msg)
	assert _msg < p * q * r
	_hash = bytes_to_long(sha1(msg).digest())
	_enc = pow(_msg, 31337, p * q * r)
	return crow(_enc * pk, pk * _hash, _hash * _enc)

key = keygen(256)
enc = encrypt(flag, key)
f = open('flag.enc', 'w')
f.write(long_to_bytes(enc))
f.close()
```

I think I love this CTF because challenges were implemented in a simple way but hard for me to solve :))) As first I simplified the **crow** function. There are many way to simplify this function and after some tries, I got: **crow(x, y, z) = (x+y+z+1)^3 + 3(x+y)^2 + 8x + 2y - z - 1** (I got rid of **//6** in order to easily calculate)

In this situation, we can see that (x+y+z+1)^3 is (much) bigger than 3(x+y)^2 and 8x+2y-z-1. So I got cube root of result and rounded it, I got x+y+z+1. Which means **nroot(result, 3) = x+y+z+1**. Then, I substracted this result, divided it with 3 and got square root, I got x+y. Then I got the rest.

```python
def trace_back(n):
    d = nroot(n, 3)
    e = nroot((n - d ** 3) // 3, 2)
    f = n - d**3 - 3 * e**2
```

Note that this is *approximate* algorithm and nothing is 100% right here. As I said before, **d = x+y+z+1**, **e = x+y** and **f = 8x+2y-z-1**, so I used sagemath to solve this linear equation system.

```python
    x, y, z = var('x, y, z')
    f(x, y, z) = x + y + z
    g(x, y) = x + y
    h(x, y, z) = 8*x + 2*y - z
    solutions = solve([f == (d - 1), g == e, h == f + 1], x, y, z)
    for solution in solutions:
        # show(solution)
        x = solution[0].rhs()
        y = solution[1].rhs()
        z = solution[2].rhs()
```
If we use **show(solution)** we will see that the solution of system is not integer. So I thought that there are many solutions for this equation and I needed to find integer solution.

I have new linear equation system with variables u, v, w satistying that:

- **(u+v+w+1)^3 + 3(x+y)^2 + 8x+2y-z-1 = crow(u, v, w) = m**
- **u+v+w+1 = x+y+z+1**
- **w = z+i** with some integer *i* (because, just I said before, this is approximate algorithm and when I tested with random integers, z might be the same or vary 1 unit)

Here is my full code to find 3 integers satistying **crow** function:

```python
def trace_back(n):
    d = nroot(n, 3)
    e = nroot((n - d ** 3) // 3, 2)
    f = n - d**3 - 3 * e**2
    x, y, z = var('x, y, z')
    f(x, y, z) = x + y + z
    g(x, y) = x + y
    h(x, y, z) = 8*x + 2*y - z
    solutions = solve([f == (d - 1), g == e, h == f + 1], x, y, z)
    for solution in solutions:
        # show(solution)
        x = solution[0].rhs()
        y = solution[1].rhs()
        z = solution[2].rhs()
    u, v, w = var('u, v, w')
    p(u, v, w) = (u + v + w + 1)^3 + 3*(u+v)^2 + 8*u + 2*v - w - 1
    q(u, v, w) = u + v + w
    r(u, v, w) = w
    for i in range(10):

        ss = solve([p == n, q == (x + y + z), r == z + i], u, v, w)

        for s in ss:
            x1 = s[0].rhs()
            y1 = s[1].rhs()
            z1 = s[2].rhs()
            # show(s)
            if(crow(int(x1), int(y1), int(z1)) == n):
                if x1 > 0 and y1 > 0:
                    return (x1, y1, z1)
```

Now I find **a = _enc * pk**, **b = pk * _hash** and **c = _enc * hash**

```python
from Crypto.Util.number import *

f = open('flag.enc', 'rb')
data = f.read()
f.close()
m = bytes_to_long(data) * 6
a, b, c = trace_back(m)
assert crow(a, b, c) == m
print(a, b, c)
```

Then, I find **pk**, **_enc** and **_hash**

```python
a, b, c = (234519792532819167786282671443053018493597523070397808117760874649849574053170253474779283201750560040067408534055586626285298238454056574930007324979198537842981515416322790348962375705480496130727196343885739935872052982389835044635761742610789147108150376262866881832472966640118448643518761968130052559402433720262111049287219424919946700202586529925292735342646896526966573037308578360366986983696740428755372683182119567744647185584163347041420293426277235, 2762581464355712476770917551699613866193810701690449235438768667756079268283507771437524470469036692990968847981209379342586389526181446618016286925687738526073213731120340035610204834970843045495449264218939484364178728492415908172505933955387020844105766387089557011226456161190, 167450941259610773796502678583827159860407751755497864563717532594025612094447481302392965836096877861703184443226302161820840037689763482195204215000065086736011797529719001193543759910737891596954239244095988583485321559108477198489859304023886604698711273145091870041292115634)

product = a * b * c
pk = nroot(product // (c ** 2), 2)
assert pk ** 2 == product // (c**2)
_enc = nroot(product // (b ** 2), 2)
assert _enc ** 2 == product // (b**2)
_hash = nroot(product // (a ** 2), 2)
assert _hash ** 2 == product // (a**2)
print(pk, _enc, _hash)
```

Continue using function **trace_back** with **pk * 6** and we recover the **p**, **q** and **r**. And we got **_enc**, so now we can decrypt using RSA.

```python
_p, _q, _r = (58239060955634156275821797481467504195628634364194206655149178552698557400509, 97818415784884704300575021265060951922322207515723900486664240010145262894557, 71619046278154409886798864003685410847382349782075408517334590886726130640443)
assert isPrime(_p)
assert isPrime(_q)
assert isPrime(_r)
d = inverse(31337, (_p-1)*(_q-1)*(_r-1))
plaintext = pow(_enc, d, _p * _q * _r)
print(long_to_bytes(plaintext))
```

**Flag: ASIS{I7s__Fueter-PoLy4__c0nJ3c7UrE_iN_p4Ir1n9_FuNCT10n}**

Those are my solutions for 2 challenges. Thanks for reading.
