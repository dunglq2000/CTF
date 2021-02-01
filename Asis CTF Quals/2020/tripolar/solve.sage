def crow(x, y, z):
    return (x**3 + 3*(x + 2)*y**2 + y**3 + 3*(x + y + 1)*z**2 + z**3 + 6*x**2 + (3*x**2 + 12*x + 5)*y + (3*x**2 + 6*(x + 1)*y + 3*y**2 + 6*x + 2)*z + 11*x)
def nroot(a, n):
    high = 1
    while high ** n < a:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if (mid ** n) < a and mid > low:
            low = mid
        elif (mid ** n) > a and mid < high:
            high = mid
        else:
            return mid
    return mid + 1
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
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
from Crypto.Util.number import *

f = open('flag.enc', 'rb')
data = f.read()
f.close()
m = bytes_to_long(data) * 6
a, b, c = trace_back(m)
assert crow(a, b, c) == m
print(a, b, c)
# Copy a, b and c because trace_back return result as Symbolic Ring
a, b, c = (234519792532819167786282671443053018493597523070397808117760874649849574053170253474779283201750560040067408534055586626285298238454056574930007324979198537842981515416322790348962375705480496130727196343885739935872052982389835044635761742610789147108150376262866881832472966640118448643518761968130052559402433720262111049287219424919946700202586529925292735342646896526966573037308578360366986983696740428755372683182119567744647185584163347041420293426277235, 2762581464355712476770917551699613866193810701690449235438768667756079268283507771437524470469036692990968847981209379342586389526181446618016286925687738526073213731120340035610204834970843045495449264218939484364178728492415908172505933955387020844105766387089557011226456161190, 167450941259610773796502678583827159860407751755497864563717532594025612094447481302392965836096877861703184443226302161820840037689763482195204215000065086736011797529719001193543759910737891596954239244095988583485321559108477198489859304023886604698711273145091870041292115634)
assert crow(a, b, c) == m

product = a * b * c
pk = nroot(product // (c ** 2), 2)
assert pk ** 2 == product // (c**2)
_enc = nroot(product // (b ** 2), 2)
assert _enc ** 2 == product // (b**2)
_hash = nroot(product // (a ** 2), 2)
assert _hash ** 2 == product // (a**2)
print(pk, _enc, _hash)

_p, _q, _r = trace_back(pk * 6)
print(_p, _q, _r)
# Copy _p, _q and _r because trace_back return result as Symbolic Ring
_p, _q, _r = (58239060955634156275821797481467504195628634364194206655149178552698557400509, 97818415784884704300575021265060951922322207515723900486664240010145262894557, 71619046278154409886798864003685410847382349782075408517334590886726130640443)
assert isPrime(_p)
assert isPrime(_q)
assert isPrime(_r)
d = inverse(31337, (_p-1)*(_q-1)*(_r-1))
plaintext = pow(_enc, d, _p * _q * _r)
print(long_to_bytes(plaintext))