Lại một lần nữa tạ team :((( sau đây là writeup các bài mình giải trong kì angstromCTF 2020

# Keysar

**Description:**

Hey! My friend sent me a message... He said encrypted it with the key ANGSTROMCTF.

He mumbled what cipher he used, but I think I have a clue.

Gotta go though, I have history homework!!

agqr{yue_stdcgciup_padas}

**Solution:**

Mình đã biết format của flag là actf{cai_gi_do}, vậy từ đề bài và đáp án mình suy ra được (theo chiều giải mã) là a -> a, g -> c, q -> t, r -> f. Mình thử viết bảng chữ cái tiếng Anh ra xem.

```python
a b c d e f g h i j k l m n o p q r s t u v w x y z

A N G S T R O M =======> key nè
```
Đối chiếu từ dưới (ANSTROM) lên trên, mình có G -> c, A -> a, R -> f, giống phía trên mình suy ra tới 3/4 rồi. Nhưng mình vẫn chưa viết hết key, và còn những chữ cái khác thì sao? Rồi còn "CTF" thì T lặp lại nữa ("ANGSTROM" có T rồi). Vậy là mình quyết định viết hết những chữ còn thiếu trong bảng chữ cái và không lặp lại, như sau:

```python
a b c d e f g h i j k l m n o p q r s t u v w x y z

A N G S T R O M C F B D E H I J K L P Q U V W X Y Z 
```

Tới đây mình đối chiếu ngược lên, agqr{yue_stdcgciup_padas} sẽ thành actf{yum_delicious_salad}

**Flag:** actf{yum_delicious_salad}

# Confused Streaming

**Description**
I made a stream cipher!

nc crypto.2020.chall.actf.co 20601

**Soltion**

```python
from __future__ import print_function
import random,os,sys,binascii
from decimal import *
try:
	input = raw_input
except:
	pass
getcontext().prec = 1000
def keystream(key):
	random.seed(int(os.environ["seed"]))
	e = random.randint(100,1000)
	while 1:
		d = random.randint(1,100)
		ret = Decimal('0.'+str(key ** e).split('.')[-1])
		for i in range(d):
			ret*=2
		yield int((ret//1)%2)
		e+=1
try:
	a = int(input("a: "))
	b = int(input("b: "))
	c = int(input("c: "))
	# remove those pesky imaginary numbers, rationals, zeroes, integers, big numbers, etc
	if b*b < 4*a*c or a==0 or b==0 or c==0 or Decimal(b*b-4*a*c).sqrt().to_integral_value()**2==b*b-4*a*c or abs(a)>1000 or abs(b)>1000 or abs(c)>1000:
		raise Exception()
	key = (Decimal(b*b-4*a*c).sqrt() - Decimal(b))/Decimal(a*2)
except:
	print("bad key")
else:
	flag = binascii.hexlify(os.environ["flag"].encode())
	flag = bin(int(flag,16))[2:].zfill(len(flag)*4)
	ret = ""
	k = keystream(key)
	for i in flag:
		ret += str(next(k)^int(i))
	print(ret)
```

Ở đây chương trình yêu cầu nhập 3 số nguyên a, b, c, với kha khá điều kiện, mình cần lưu ý chỗ `Decimal(b*b-4*a*c).sqrt().to_integral_value()**2==b*b-4*a*c`, đoạn này có nghĩa là biểu thức `b*b-4*a*c` không phải là bình phương của 1 số nguyên (không là số chính phương).

key được tính bằng cách `(Decimal(b*b-4*a*c).sqrt() - Decimal(b))/Decimal(a*2)`, đây là công thức nghiệm phương trình bậc 2 (nghiệm lớn hơn) =))))

Mỗi ký tự trong cách biểu diễn binary của flag sẽ xor với keystream tiếp theo của key (lệnh **yield**). Hàm keystream nhận tham số là key (cái công thức nghiệm gì gì mình mới nói ấy), chọn 1 số nguyên e random từ 100 tới 1000. Mỗi lần lặp hàm này chọn 1 số nguyên d random từ 1 tới 100, tính key^e và chỉ lấy phần thập phân của kết quả là **ret**. Biến ret này sau đó được nhân với 2^d (bằng vòng for) và kết quả cuối cùng lấy phần nguyên của ret modulo 2.

Cứ mỗi lần yield, theo mình hiểu, hàm keystream sẽ quay lại vòng lặp `while 1` và random d mới, tính ret mới nhưng e cũ. Xong, giờ thì ......... làm sao giải??!!??

Câu chuyện khá là căng khi có 2 số random e và d, nên mình không thể *kiểm soát* đầu ra được. Từ đây mình nghĩ ra 1 ý tưởng, việc tính key^e nếu mình chọn key < 1 thì sao? e càng lớn thì key^e càng nhỏ, và phần nguyên luôn là 0. :))) Vậy code *chỉ* lấy phần thập phân vô dụng với mình. Tiếp đó, biến ret được nhân với 2^d.... Để sau vậy :)))

Phương trình ax^2 + bx + c = 0 với a, b, c nguyên. key chính là nghiệm lớn của phương trình và mình muốn key < 1. Theo định lý Viete thì:
```
x1 + x2 = -b/a

x1*x2 = c/a
```

và mình cần x1 < 1, x2 < 1 => x1 + x2 < 2 và (x1-1)(x2-1) > 0. Tức là -b/a < 2 và c+b>-a. Tiếp nữa, mình cần (x2^e) * (2^d) < 1, mình chỉ cần quan tâm e=100 (nhỏ nhất) và d=100(lớn nhất), tức là (x2 * 2)^100 < 1, điều này luôn đúng =)))) các bạn có thể tự kiểm chứng.

Giờ thì ............ chọn số thôi :))) Mình chọn a=6, b=8 và c=-3, và kết quả của hàm keystream luôn trả về 0 (kết quả có bao giờ vượt qua 0 đâu :v). 

```python
# p receive from server
p = '01100001011000110111010001100110011110110110010001101111011101110110111001011111011101000110111101011111011101000110100001100101010111110110010001100101011000110110100101101101011000010110110001111101'
plain = ''
for i in p:
	plain += str(0 ^ int(i))
from Crypto.Util.number import *
print(long_to_bytes(int(plain, 2)))
```
**Flag:** actf{down_to_the_decimal}
