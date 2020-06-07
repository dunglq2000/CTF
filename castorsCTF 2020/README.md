# Castor CTF 2020

Giải này team mình team mình cũng khá "xanh". Trận này mạng mình khá lag nên không tạo nick :v mình dùng nick của đồng đội mình là **n3mo** nên điểm số của nick này là mình và bạn í cũng làm :D

## Cryptography

### Goose chase

Đề bài cho mình 2 tấm hình và ở 2 tấm hình này có 1 khu vực bị "nhòe". Dựa vào 1 số kinh nghiệm trước đây mình đoán rằng khu vực đó đã bị xor với 1 key nào đó nên mình không thể xem được. Do đó mình xor 2 tấm hình lại bằng đoạn code như sau

```python
from PIL import Image
f = Image.open('a.png')
px = f.load()
w, h = f.size
print(w, h)
f = Image.open('b.png')
px2 = f.load()
w2, h2 = f.size

newImg = Image.new(f.mode, f.size)
newImgData = newImg.load()
for width in range(w):
    rows = []
    for heigth in range(h):
        a = px[width, heigth][0] ^ px2[width, heigth][0]
        b = px[width, heigth][1] ^ px2[width, heigth][1]
        c = px[width, heigth][2] ^ px2[width, heigth][2]
        rows.append((a, b, c))
        newImgData[width, heigth] = (a, b, c)
newImg.save("answer.png")
```

Kết quả: ![goose](answer.png)

### Jigglypuff's Song

![jiggly](chal.png)

Bài này ban đầu mình đã nghi nghi về tấm hình rồi và đề cũng gợi ý là MSB nhưng mình hơi *bối rối* và phải nhờ đồng đội support. Challenge này chỉ đơn giản là lấy MSB (most significant bit) của tấm hình. Ở đây mình dùng **StegSolve**, tích vào channel R, G, B đều là 7. Message sẽ nằm trong đoạn text đó. 

**Flag:** castorsCTF{r1ck_r0ll_w1ll_n3v3r_ d3s3rt_y0uuuu}

### Bagel Bytes

**nc chals20.cybercastors.com 14420**

[Server](schoolbus.py)

Khi netcat lên server thì mình có 2 lựa chọn, nếu chọn 1 thì mình sẽ nhập vào 1 chuỗi thì hàm **bake_your_own** được gọi, trả về cho mình bản mã AES của chuỗi mình nhập vào. Nếu là 2 thì mình cũng nhập 1 chuỗi, nhưng lần này hàm **bake_flag** được gọi với plaintext sẽ gồm flag theo sau là input của mình.

Và quan trọng nhất, AES dùng mode **ECB**. Tới đây mình chỉ cần viết đoạn script tấn công AES ECB thôi.

```python
from pwn import *
r = remote('chals20.cybercastors.com', 14420)
len_flag = 64
flag = b'castorsCTF{I_L1k3_muh_b4G3l5_3x'
index = 0
charset = ''.join([chr(i) for i in range(97, 97+26)])
charset += ''.join([chr(i) for i in range(65, 65+26)])
charset += '{}_1234567890'
for i in range(len(flag) + 1, len_flag):
        payload = b'a' * (len_flag - i)
        d = r.recvuntil(b'Your choice: ')
        r.sendline(b'2')
        d = r.recv(1024)
        print(d)
        r.sendline(payload)
        d = r.recv(1024).strip().split(b'\n')
        cipher = d[-1]
        # print(cipher)
        print("Cracking...........")
        # for j in range(32, 128):
        for j in charset:
                # test = payload + chr(j).encode()
                d = r.recvuntil(b'Your choice: ')
                r.sendline(b'1')
                d = r.recv(1024)
                # r.sendline(payload + flag + chr(j).encode())
                r.sendline(payload + flag + j.encode())
                data = r.recv(1024).strip().split(b'\n')
                # print(data)
                if data[-1][:(2*len_flag)] == cipher[:(2*len_flag)]:
                        flag += j.encode() #chr(j).encode()
                        break
        print(flag)
        if flag[-1] == b'}':
                break
r.close()
```

**Flag:** castorsCTF{I_L1k3_muh_b4G3l5_3x7r4_cr15pY}

### Two Paths

![two-paths](two-paths.png)

Bài này không khó nhưng khiến mình mất khá nhiều thời gian. Vẫn là dùng **StegSolve**, mình xem qua các channel và phát hiện, ở góc trái dưới tấm hình có 1 đường link gì đó :v

![two-paths](two.png)

Đường link tới *https://go.aws/2X1R6H7* (hiện tại thì link này đã die). Lúc giải đấu diễn ra, nếu vào link này sẽ hiện ra 1 đoạn hội thoại. Vì hơi dài nên các bạn có thể xem ở [đây](text-cipher-img.png)

Mã hoán vị! Và tất nhiên cách mình đã làm để giải mã này là ........... đoán. Thống kê số lượng chữ, dựa trên câu thoại để đoán ra từ ngữ tương ứng. Kết quả sẽ ra như vầy: 

```python
#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
charset = {"♓": 'o', "♒": 'n', "🔁": 'r', "♉": 'a', "❌": 't', "🈲": 'u', "♏": 'l', "⏺": 'i', "♊": 's',
			"⏺": 'i', "💯": 'f', "🔟": 'y', "⛎": 'd', "⏫": 'h', "🚺": 'w', "✖": 'e', "➿": 'j', "♑": 'p', 
			"Ⓜ": 'm', "♌": 'b', "🔴": 'x', "➗": 'v', "♐": 'q', "🆔": 'k', "📶": 'z', "♈": 'c',
			"🌀": 'g'}
```

Hardcore cả đêm! Nhưng tới đây vẫn có gì đó sai sai, mình chưa thấy flag đâu cả! Khi bật **StegSolve** lên lần nữa nhưng lần này mình vào *Analyse->File Format* thì thấy ở cuối hình có 1 dãy bit là ```0110100 0 011101 00 01110 100 0111 0000 011 10011 00 111010 0 0101111 00101111 0110011 1 011011 11 00101 110 0110 0001 011 10111 01 110011 0 0101111 00110010 0111101 0 011101 01 01000 011 0100 0110 010 00011 01 110000```, lấy từng bộ 8 bit ra và chuyển thành ascii, mình nhận được 1 đường *link* khác: *https://go.aws/2zuCFCp*. 

Chắc flag ở đây =))) Mở ra thì ............. 1 đống :( Nhưng mình đã tìm ra ký tự tương ứng với hình, nên bây giờ chỉ việc dùng dictionary vừa rồi để giải thôi (các bạn nhớ thêm 2 dòng comment ở đầu như mình nhé, nếu không thì python không encode được mấy ký hiệu kia đâu).

**Flag:** castorsCTF{sancocho_flag_qjzmlpg}

### Amazon

Bài này khá ......... thú vị (đối với mình) vì ít khi mình làm mấy dạng đoán mò như vầy :v

**Description**

Are you watching the new series on Amazon?

198 291 575 812 1221 1482 1955 1273 1932 2030 3813 2886 1968 4085 3243 5830 5900 5795 5628 3408 7300 4108 10043 8455 6790 4848 11742 10165 8284 5424 14986 6681 13015 10147 7897 14345 13816 8313 18370 8304 19690 22625

**Solution**

Mình biết format flag là castorsCTF{}. Oke, mình lấy từng số trong đề trừ đi ascii number trong format flag và phát hiện ra:

```
198 - ord('c') = 1*ord('c')
291 - ord('a') = 2*ord('a')
575 - ord('s') = 4*ord('s')
```

Mới làm tới đây mình phán luôn quy luật: *ciphertext = 2^i * ord(ký tự)* :))) và tất nhiên là ....... sai. Mình thử thêm vài cái nữa

```
812 - ord('t') = 6*ord('t')
1221 - ord('o') = 10*ord('o')
```

Tới đây thì mình mới hiểu :v *ciphertext = (số nguyên tố kế số nguyên tố trước) * ord(ký tự)*. Vì vậy việc giải mã khá đơn giản, chỉ cần lấy số nguyên tố kế nhau và lấy ciphertext chia cho nó.

```python
enc = "198 291 575 812 1221 1482 1955 1273 1932 2030 3813 2886 1968 4085 3243 5830 5900 5795 5628 3408 7300 4108 10043 8455 6790 4848 11742 10165 8284 5424 14986 6681 13015 10147 7897 14345 13816 8313 18370 8304 19690 22625".split(" ")
num = [int(i) for i in enc]
flag = ""
from Crypto.Util.number import *
def next_prime(n):
	r = n+1
	while True:
		if isPrime(r):
			return r
		r += 1
cnt = 2
for i in num:
	flag += chr(i // cnt)
	cnt = next_prime(cnt)
print(flag)
```

**Flag:** castorsCTF{N0_End_T0d4y_F0r_L0v3_I5_X3n0n}

### Magic School Bus

nc chals20.cybercastors.com 14421

Ở đây mình cần nhập 1 cái gì đó, dựa theo đề bài mình nhập từ *driver* vào và chương trình trả về *VDIRER*. Đây là 1 hoán vị các chữ cái theo quy luật gì đó. Mình nhập thử *student* thì chương trình trả về *tdsuten*. Chả rút ra được gì :)))

NHƯNG! Nếu nó đã hoán vị theo quy tắc nào đó thì chỉ cần mình dùng ciphertext của lần input trước làm input cho lần sau, ví dụ như ở trên *driver* cho ra *vdirer* thì lần sau mình lấy *vdirer* làm input và nhận về kết quả tiếp theo. Cứ làm vậy 3, 4 lần thì, ngạc nhiên :) , nó quay lại như cũ là *driver*. Vậy nghĩa là: **quay 1 vòng rồi cũng về vạch xuất phát!**. Khi mình có ciphertext là option 2, thì làm như vậy sau mười mấy lần là có flag :v

**Flag:** CASTORSCTF{R3C0N4ISSANCE_IS_K3Y_TO_S0LV1NG_MYS73R1E5}

### One Trick Pony

nc chals20.cybercastors.com 14422

Nếu mình nhập đại gì đó vào thì chương trình trả về ciphertext, không phải base64, base32 hay gì. Mình thử nhập format flag là *castorsCTF* thì chương trình trả về chuỗi rỗng! Là sao???

Mình rút ngắn lại, nhập *c* thôi, kết quả vẫn vậy =)))) Nếu chỉ nhập *a* thôi thì mình vẫn nhận được 1 chuỗi khác rỗng (ciphertext). Điều đó đơn giản là, mình có thể brute force ký tự tiếp theo, nếu server trả về chuỗi rỗng, tức là ký tự đó kết nạp vào flag được.

```python
from pwn import *
r = remote('chals20.cybercastors.com', 14422)
flag = 'castorsCTF{k33p_y0ur_k3y5_53cr37_4nd_d0n7_r3u53_7h3m!}'
charset = 'abcdefghijklmnopqrstuvwxyz'
charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
charset += ''
for _ in range(100):
        for i in range(32, 128):
                d = r.recvuntil(b'> ')
                # print(d)
                r.sendline((flag + chr(i)).encode())
                d = r.recvline()
                # print(d, len(d))
                if len(d) == 4:
                        flag += chr(i)
                        break
        print("Flag found: " + flag)
```

Lưu ý là server trả về b''\n là 4 ký tự dạng ascii chứ không phải chuỗi byte python rỗng, nên len(d) mới so sánh với 4 mà không phải 0. Charset của mình không có dấu chấm than (!) nên tới bước cuối thì mình khá hoang mang và phải đổi loop lại là từ 32 tới 128 để brute hết khả năng của nó.

**Flag:** castorsCTF{k33p_y0ur_k3y5_53cr37_4nd_d0n7_r3u53_7h3m!}

## Forensic

### Manipulation

File ở [đây](pooh.jpg)

File này có 1 điều thú vị đó là khi mình mở file bằng các trình đọc hexa (mình dùng **hex editor workshop**) thì thấy các bộ 00000010, 00000020, vân vân và mây mây. Để ý một chút, sau đó là dấu 2 chấm (:) và những ký tự hexa. Mình thử decode hex thì hóa ra chúng chính là hexa của các ký tự ngay sau đó. Ví dụ như **00000010: 012c 0000 ffe1 20e8 4578 6966 0000 4949** và  **.,.... .Exif..II** thì đoạn hex sau dấu : decode sẽ ra đoạn có chữ Exif.

Vậy mình chỉ cần đọc file, filter các đoạn text và chỉ giữ lại hex thôi và ghi ra 1 file answer. Lưu ý là ở cuối file chứa phần mở đầu của file jpg và do mỗi cụm như vậy gồm 8x4=32 ký tự hexa, tương đương 16 byte nên sau khi *cắt ghép* thì phải đưa 16 byte cuối lên đầu.

Code của mình ở [đây](manipulate.py) và đây là kết quả

![pooh](manipulate.jpg)

**Flag:** castorsCTF{H3r3_Is_y0uR_Fl4gg}

## Coding

### Arithmetics

Bài này nói chung để .......... giải trí và cho điểm :v chỉ cần filter toán hạng 1, toán tử, toán hạng 2 rồi tính thôi :)))

```python
from pwn import *
def calculate(a1, p, a2):
        num = [b'one', b'two', b'three', b'four', b'five', b'six',
                b'seven', b'eight', b'nine']
        charset = num = {b'one': 1, b'two': 2, b'three': 3, b'four': 4, b'five': 5, b'six': 6,
                b'seven': 7, b'eight': 8, b'nine': 9}
        check1, check2 = 0, 0
        b1, b2 = -1, -1
        if a1 in num:
                b1 = charset[a1]
                check1 = 1
        if a2 in num:
                b2 = charset[a2]
                check2 = 1
        if check1 == 0:
                b1 = int(a1)
        if check2 == 0:
                b2 = int(a2)
        if p == b'+' or p == b'plus':
                return b1 + b2
        elif p == b'-' or p == b'minus':
                return b1 - b2
        elif p == b'*' or p == b'multiplied-by':
                return b1 * b2
        elif p == b'//' or p == b'divided-by':
                return b1 // b2
r = remote('chals20.cybercastors.com', 14430)
d = r.recvuntil(b'Hit <enter> when ready.\n')
r.sendline(b'\n')
d = r.recvuntil(b'\n').strip().split(b' ')
text = ''
print(d)
for i in d:
        text += chr(int(i, 2))
r.sendline(text.encode())
d = r.recv(1024)
print(d)
r.close()
```

Ngoài ra mình còn làm 1 bài misc là **Gif**, 5 bài reverse ít điểm nhất thôi nên mình không viết ra ở đây để đỡ mất thời gian. Cũng không quá khó, các bạn có thể thử.

Flag cho các bài:

- **Gif**: castorsCTF{omgsofunnylol}
- **XoR**: castorsCTF{x0rr1n6_w17h_4_7w157}
- **reverse-me**: castorsCTF{r3v3r51n6_15_fun}
- **Stacking**: castorsCTF{w3lc0m3_70_70_r3v3r23_3n61n33r1n6}
- **Vault1**: castorsCTF{r1cK_D1e_R1cKp3aT_x0r}