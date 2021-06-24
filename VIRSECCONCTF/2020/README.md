# VIRSECCON CTF 2020

Okay giải này mình không tham gia nhiều, chỉ 1 bài crypto thôi :v

## Old monitor

**Description**:

I have this old CRT monitor that I use for my desktop computer. It crashed on me and spit out all these weird numbers…

**Solution**:

CRT là Chinese Remainder Theorem (định lý số dư Trung Quốc). Các bạn có thể tham khảo ở [đây](https://en.wikipedia.org/wiki/Chinese_remainder_theorem)

Đầu tiên ta cần viết lại đề dưới dạng các phương trình đồng dư để sử dụng CRT.

- m^3 = c1 (mod n1)
- m^3 = c2 (mod n2)
- m^3 = c3 (mod n3)

Ở đây m^3 chính là ẩn ta cần tìm. Và ta nhận thấy rằng n1, n2, n3 đôi một nguyên tố cùng nhau (có ước chung lớn nhất là 1) nên việc sử dụng CRT là khả thi.

Cách tính nghiệm của hệ thặng dư trên như sau:

- Tính N = n1 * n2 * n3
- Với mỗi ni thuộc {n1, n2, n3}, ta tính Ni = N / ni, và tìm nghịch đảo của Ni trong modulo ni. Sở dĩ có thể tính được là do n1, n2, n3 nguyên tố cùng nhau đôi một, nên trong Ni = N / ni sẽ không có ni nên Ni cũng nguyên tố cũng nhau với ni luôn. Ta gọi nghịch đảo của Ni là Ni_inv.
- Dùng công thức m^3 = (c1 * N1 * N1_inv + c2 * N2 * N2_inv + c3 * N3 * N3_inv) (mod N)
- Do m < n1, m < n2 và m < n3 nên m^3 < (n1 * n2 * n3)
- Từ đó, kết quả tính được từ công thức trên bằng đúng m^3 chứ không phải đồng dư của m^3 trong modulo N
- Lấy căn bậc 3 ta có kết quả

**Hàm tính nghiệm của hệ thặng dư**
```python
def solve_crt(t, n):
    N = 1
    x = 0
    for i in n:
        N *= i
    for i in range(len(n)):
        Ni = N // n[i]
        Ni_inv = common.inverse(Ni, n[i])
        x = x + (t[i] * Ni * Ni_inv)
    return x % N
```

**Lấy căn bậc 3**:
```python
#from http://python.6.x6.nabble.com/cube-root-tp1733498p1733529.html
def root3rd(x):
    y, y1 = None, 2
    while y != y1:
        y = y1
        y3 = y**3
        d = (2*y3+x)
        y1 = (y*(y3+2*x)+d//2)//d
        print(y, y1)
    return y
```

**Giải**:
```python
n1 = 7156756869076785933541721538001332468058823716463367176522928415602207483494410804148006276542112924303341451770810669016327730854877940615498537882480613
n2 = 11836621785229749981615163446485056779734671669107550651518896061047640407932488359788368655821120768954153926193557467079978964149306743349885823110789383
n3 = 7860042756393802290666610238184735974292004010562137537294207072770895340863879606654646472733984175066809691749398560891393841950513254137326295011918329
c1 = 816151508695124692025633485671582530587173533405103918082547285368266333808269829205740958345854863854731967136976590635352281190694769505260562565301138
c2 = 8998140232866629819387815907247927277743959734393727442896220493056828525538465067439667506161727590154084150282859497318610746474659806170461730118307571
c3 = 3488305941609131204120284497226034329328885177230154449259214328225710811259179072441462596230940261693534332200171468394304414412261146069175272094960414
n = [n1, n2, n3]
c = [c1, c2, c3]
sol = solve_crt(c, n)
from Crypto.Util.number import *
print(long_to_bytes(root3rd(sol)))
```

**Flag**: LLS{the_chinese_remainder_theorem_is_so_cool}
