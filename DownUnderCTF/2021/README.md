# DownUnder CTF 2021

Do hơi bận nên mình sẽ viết writeup ngắn gọn thôi, mong các bạn thông cảm :))

Code các bài ở writeup này mình có để trong folder tương ứng, còn các bài không được ghi ở đây mình không giải ra, mình để đó sau này tham khảo :))

## Subtitution Cipher 1

```python
def encrypt(msg, f):
    return ''.join(chr(f.substitute(c)) for c in msg)

P.<x> = PolynomialRing(ZZ)
f = 13*x^2 + 3*x + 7

FLAG = open('./flag.txt', 'rb').read().strip()

enc = encrypt(FLAG, f)
print(enc)

```

Bài này khá đơn giản, lấy giá trị của ký tự $$c$$, bỏ vào hàm $$f(x) = 13x^2+3x+7$$ là ra giá trị (unicode). Nên mình copy paste output từ file vào string và bruteforce xem với ký tự nào thì cho ra unicode đó.

Flag: **DUCTF{sh0uld'v3_us3d_r0t_13}**

## Substitution Cipher 2

```python
from string import ascii_lowercase, digits
CHARSET = "DUCTF{}_!?'" + ascii_lowercase + digits
n = len(CHARSET)

def encrypt(msg, f):
    ct = ''
    for c in msg:
        ct += CHARSET[f.substitute(CHARSET.index(c))]
    return ct

P.<x> = PolynomialRing(GF(n))
f = P.random_element(6)

FLAG = open('./flag.txt', 'r').read().strip()

enc = encrypt(FLAG, f)
print(enc)

```

Bài này nâng cao hơn bài trước, với bộ **CHARSET** có sẵn, chương trình sinh random 1 hàm $$f$$ bậc 6 trên $$GF(47)$$ (độ dài charset), tức là $$f$$ sẽ có dạng $$a_6 x^6 + a_5 x^5 + \cdots + a_1 x + a_0$$.

Với mỗi ký tự $$c$$ của flag, ta lấy index của nó trong **CHARSET** rồi đưa vào hàm $$f$$, sau đó lấy **CHARSET** tại kết quả. Mình sẽ tìm lại hàm $$f$$.

Mình đã biết các cặp plaintext-ciphertext tại vị trí tương ứng với **DUCTF{** và **}**, tức là 6 ký tự đầu và ký tự cuối của plaintext và ciphertext, vừa đủ cho 7 hệ số của $$f$$ :))

Gọi $$x_0, x_1, \cdots, x_6$$ tương ứng là index của **DUCTF{}**. Gọi $$y_0, y_1, \cdots, y_6$$ tương ứng là index của ciphertext ứng với **DUCTF{}** (6 ký tự đầu và ký tự cuối của ciphertext)

Như vậy, $$y_i = a_6 x_i^6 + a_5 x_i^5 + \cdots a_1 x_i + a_0$$, viết dưới dạng ma trận sẽ là $$\begin{pmatrix}x_0^0 & x_0^1 & \cdots & x_0^6 \\ x_1^0 & x_1^1 & \cdots & x_1^6 \\ \cdots & \cdots & \cdots & \cdots \\ x_6^0 & x_6^1 & \cdots & x_6^6\end{pmatrix} \begin{pmatrix}a_0 \\ a_1 \\ \cdots \\ a_6\end{pmatrix}=\begin{pmatrix}y_0 \\ y_1 \\ \cdots \\ y_6 \end{pmatrix}$$

Tính inverse thì mình có $$\begin{pmatrix}a_0 & a_1 & \cdots & a_6\end{pmatrix}$$ và làm giống bài trên. Tuy nhiên có thể có nhiều kết quả flag nên mình sẽ lấy cái có ý nghĩa.

Flag: **DUCTF{go0d_0l'_l4gr4ng3}** (nhà toán học Lagrange đấy :v)

## Break me

```python
#!/usr/bin/python3
import sys
import os
from Crypto.Cipher import AES
from base64 import b64encode

bs = 16 # blocksize
flag = open('flag.txt', 'rb').read().strip()
key = open('key.txt', 'r').read().strip().encode() # my usual password

def enc(pt):
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt+key))
    res = b64encode(ct).decode('utf-8')
    return res

def pad(pt):
    while len(pt) % bs:
        pt += b'0'
    return (pt)

def main():
    print('AES-128')
    while(1):
        msg = input('Enter plaintext:\n').strip()
        pt = flag + str.encode(msg)
        ct = enc(pt)
        print(ct)

if __name__ == '__main__':
    main()

```
Bài này thì server sẽ encrypt cho mình message có dạng **flag+input+key**, input là cái mình nhập lên í. Mình không biết flag có độ dài bao nhiêu nên mình nhập chuỗi rỗng, rồi 1 ký tự, 2 ký tự, ... và thấy khi nhập 0 ký tự, ciphertext có 3 block còn khi nhập 4 ký tự thì 4 block. Đoán chắc key 16 byte, mình đoán luôn flag 32 byte :))

Bây giờ, brute key thôi, AES-ECB. Rồi lấy key đó decrypt là ra flag

Flag: **DUCTF{ECB_M0DE_K3YP4D_D474_L34k}**

## Treasure

```python
#!/usr/bin/python3

import re
from Crypto.Util.number import long_to_bytes
from Crypto.Random import random
from secret import REAL_COORDS, FLAG_MSG

FAKE_COORDS = 5754622710042474278449745314387128858128432138153608237186776198754180710586599008803960884
p = 13318541149847924181059947781626944578116183244453569385428199356433634355570023190293317369383937332224209312035684840187128538690152423242800697049469987

def create_shares(secret):
    r1 = random.randint(1, p - 1)
    r2 = random.randint(1, p - 1)
    s1 = r1*r2*secret % p
    s2 = r1*r1*r2*secret % p
    s3 = r1*r2*r2*secret % p
    return [s1, s2, s3]

def reveal_secret(shares):
    s1, s2, s3 = shares
    secret = pow(s1, 3, p) * pow(s2*s3, -1, p) % p
    return secret

def run_combiner(shares):
    try:
        your_share = int(input('Enter your share: '))
        return reveal_secret([your_share, shares[1], shares[2]])
    except:
        print('Invalid share')
        exit()

def is_coords(s):
    try:
        return re.match(r'-?\d+\.\d+?, -?\d+\.\d+', long_to_bytes(s).decode())
    except:
        return False

def main():
    shares = create_shares(REAL_COORDS)
    print(f'Your share is: {shares[0]}')
    print(f'Your two friends input their shares into the combiner and excitedly wait for you to do the same...')

    secret_coords = run_combiner(shares)
    print(f'The secret is revealed: {secret_coords}')
    if not is_coords(secret_coords):
        print('"Hey those don\'t look like coordinates!"')
        print('Your friends grow a bit suspicious, but you manage to convince them that you just entered a digit wrong. You decide to try again...')
    else:
        print('"Let\'s go get the treasure!!"')
        print('Your friends run off to the revealed location to look for the treasure...')
        exit()

    secret_coords = run_combiner(shares)
    if not is_coords(secret_coords):
        print('"This is way too sus!!"')
        exit()

    if secret_coords == FAKE_COORDS:
        print('You\'ve successfully deceived your friends!')

        try:
            real_coords = int(input('Now enter the real coords: '))
            if real_coords == REAL_COORDS:
                print(FLAG_MSG)
            else:
                print('Incorrect!')
        except:
            print('Incorrect!')
    else:
        print('You are a terrible trickster!')

if __name__ == '__main__':
    main()

```

Gọi $$S$$ là **REAL_COORD** bị giấu, hàm **create_shares** thực hiện như sau:

- Chọn random 2 số $$r_1$$ và $$r_2$$
- Lần lượt tính $$s_1 = r_1 r_2 S \pmod p$$, $$s_2 = r_1^2 r_2 S \pmod p$$ và $$s_3 = r_1 r_2^2 S \pmod p$$
- Trả về ($$s_1$$, $$s_2$$, $$s_3$$) và leak cho mình $$s_1$$

Tiếp theo, hàm **run_combiner** cần mình input 1 số nguyên mình đặt là $$t$$, lấy $$s_2$$ và $$s_3$$ ở trên đưa vào **reveal_secret** và trả về $$t^3 (s_2 s_3)^{-1} \pmod p$$

Sau đó mình cần input 1 số $$t'$$, cũng với $$s_2$$ và $$s_3$$ ở trên qua hàm **reveal_secret** trả về **FAKE_COORDS**. Tức là $$FAKE_COORDS = t'^3 (s_2 s_3)^{-1} \pmod p$$

Ý tưởng của mình như sau:

- Mình cho $$t=1$$ cho dễ tính, khi đó giá trị trả về ở **run_combiner** lần đầu sẽ là $$(s_2 s_3)^{-1} \pmod p$$, lấy nghịch đảo sẽ được $$s_2 s_3 \pmod p$$
- Tiếp theo, mình có $$x = t'^3 = FAKE_COORDS \cdot (s_2 s_3) \pmod p$$, tính $$phi(p)=p-1$$ rồi $$d = 3^{-1} \pmod p$$ rồi $$t'=x^d \pmod p$$ (nói chung là RSA)
- Có $$t'$$ rồi thì submit lên, read server tới khi flag lòi ra thôi :))

Flag: **DUCTF{m4yb3_th3_r34L_tr34sur3_w4s_th3_fr13nDs_w3_m4d3_al0ng_Th3_W4y.......}** (dài vl)

## Secuchat

Bài này cho 1 file database và mình dùng mấy tool xem database (ví dụ như link [này](https://inloop.github.io/sqlite-viewer/)) thì cấu trúc database như sau:

- **Conversation**: chứa các đoạn conversation, gồm **id**, **initiator**, **peer** và **initial_parameters**. Ở đây **initiator** là người khởi động cuộc hội thoại và **peer** là đối tác của cuộc hội thoại. **initial_parameters** là parameter đầu tiên của cuộc hội thoại sẽ được ghi rõ ở bảng sau
- **Message**: chứa các message, gồm **conversation** là id của conversation ở trên, **timestamp** là thời gian message (mình bỏ qua), **from_initiator** có giá trị 1 nếu message được gửi bởi initiator của cuộc hội thoại, 0 thì ngược lại là peer, **next_parameter** là parameter cho message tiếp theo, dễ thấy các message của cùng 1 cuộc hội thoại thì parameter liên tiếp nhau và message đầu tiên của đoạn hội thoại dùng initial_parameter ở trên :)) cuối cùng là **encrypted_message** là message đã bị mã hóa bằng AES
- **Parameters**: gồm **id**, **encrypted_aes_key_for_initiator** và **encrypted_aes_key_for_peer** - nghĩa là nếu message được gửi bởi initiator thì sẽ dùng key cho initiator, nếu được gửi từ peer thì dùng key cho peer. Ở đây cả 2 key đều bị mã hóa bởi RSA, mình đề cập ở table sau. Cuối cùng là **iv** cho AES-CBC
- **User**: gồm **username** và **rsa_key** tương ứng với người dùng đó

Tóm lại, trong 1 conversation, các message bị encrypt bằng thuật toán AES-CBC và chúng ta có key cho AES-CBC đã bị encrypt bởi RSA của người gửi (tất nhiên là public key)

Ý tưởng của mình là tìm ra tất cả private key có thể. Để làm điều này mình gcd tất cả cặp public key để xem hên xui có không :)) và có thật

```python
import sqlite3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from itertools import product
from Crypto.Util.number import *

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

con = sqlite3.connect("secuchat.db")

cur = con.cursor()
cur.execute("SELECT * FROM User")
users = cur.fetchall()
usernames = [user[0] for user in users]
keys = [RSA.importKey(user[1]).n for user in users]
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        p, q = keys[i], keys[j]
        g = gcd(p, q)
        if g < p and g > 1:
            idx, jdx = i, j
            print(i, j)
            # break

g = gcd(keys[idx], keys[jdx])
keyi = g, keys[idx] // g
keyj = g, keys[jdx] // g
di = inverse(65537, (keyi[0] - 1) * (keyi[1] - 1))
dj = inverse(65537, (keyj[0] - 1) * (keyj[1] - 1))
keyi = RSA.construct((keys[idx], 65537, di))
keyi = PKCS1_OAEP.new(keyi)
keyj = RSA.construct((keys[jdx], 65537, dj))
```

Sau đó mình search trên các **Conversation** và tìm xem có conversation nào mà initiator (hoặc peer) là người mình đã tìm ra private key ở trên. Từ đó mình tìm trên **Message** với conversation tương ứng, from_initiator là 1 (hoặc 0 nếu ở conversation là peer). Tiếp theo mình search **Parameters** tương ứng với message đó, như mình đã nói, các message dùng parameter liên tiếp nhau, nên mình chỉ cần tìm với next_parameter-1. Decrypt thử nào!

```python
cur.execute("SELECT * FROM Conversation")
convers = cur.fetchall()

for conver in convers:
    if conver[1] == usernames[idx]:
        print("Initiator i", conver)
        cur.execute(f"SELECT * FROM Message WHERE (conversation={conver[0]} and from_initiator=1)")
        msg = cur.fetchall()
        for m in msg:
            cur.execute(f"SELECT * FROM Parameters WHERE (id={m[3]-1})")
            params = cur.fetchall()
            for param in params:
                aes_key = keyi.decrypt(param[1])
                iv = param[3]
                aes = AES.new(aes_key, AES.MODE_CBC, iv)
                print(aes.decrypt(m[4]))
    elif conver[1] == usernames[jdx]:
        print("Initiator j", conver)
    elif conver[2] == usernames[idx]:
        print("Peer i", conver)
    elif conver[2] == usernames[jdx]:
        print("Peer j", conver)

con.close()

```
Ở đây mình chỉ dùng 1 user là initiator và cũng có flag

Flag: **DUCTF{pr1m1t1v35, p4dd1ng, m0d35- wait, 3n7r0py?!}**

Cám ơn các bạn đã đọc.