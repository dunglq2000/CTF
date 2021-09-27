from sock import Sock
import re
from Crypto.Util.number import *

FAKE_COORDS = 5754622710042474278449745314387128858128432138153608237186776198754180710586599008803960884
p = 13318541149847924181059947781626944578116183244453569385428199356433634355570023190293317369383937332224209312035684840187128538690152423242800697049469987
so = Sock("pwn-2021.duc.tf", 31901)
data = so.read_line().strip().decode()
s1 = int(re.findall(r'\d+', data)[0])
so.read_line()
so.read_until(b"Enter your share: ")
so.send_line(b"1")
secret_coord = int(re.findall(r'\d+', so.read_line().strip().decode())[0])
print(so.read_line())
print(so.read_line())
so.read_until(b"Enter your share: ")
s2s3 = (pow(secret_coord, -1, p) * 1) % p
x = (FAKE_COORDS * s2s3) % p
d = inverse(3, (p - 1))
x = pow(x, d, p)
so.send_line(str(x).encode())
print(so.read_line())
so.read_until(b'Now enter the real coords: ')
REAL_COORD = (s1**3 * pow(s2s3, -1, p)) % p
so.send_line(str(REAL_COORD).encode())
for _ in range(10):
	print(so.read_line())
print(long_to_bytes(FAKE_COORDS))
so.close()
# DUCTF{m4yb3_th3_r34L_tr34sur3_w4s_th3_fr13nDs_w3_m4d3_al0ng_Th3_W4y.......}