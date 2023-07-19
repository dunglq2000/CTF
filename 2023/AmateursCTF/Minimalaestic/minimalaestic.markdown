---
title: 'Minimalaestic'
---

```python
# based on https://github.com/boppreh/aes/blob/master/aes.py
from flag import flag, key
import copy
KEY_SIZE = 2
ROUNDS = 100

def sub_bytes(s):
    for i in range(2):
        s[i][0] = sbox[s[i][0]]

def final_sub(s):
    for i in range(2):
        s[i][1] = sbox[s[i][1]]

sbox = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]

def shift_rows(s):
    s[0][0], s[1][0] = s[1][0], s[0][0]

def final_shift(s):
    s[0][1], s[1][1] = s[1][1], s[0][1]

def mix_column(column):
    column[0] = column[0] ^ column[1]
  
def mix_columns(state):
    for i in range(2):
        column = []
        for j in range(2): column.append(state[i][j])
        mix_column(column)
        for j in range(2): state[i][j] = column[j]

def add_round_key(s, k):
    for i in range(2):
        for j in range(2):
            s[i][j] ^= k[k[k[k[i*2+j]%4]%4]%4]

def final_add(s, k):
    for i in range(2):
        s[i][1] ^= k[k[k[k[i*2+1]%4]%4]%4]

def schedule_key(k):
    for i in range(4):
        for j in range(2*ROUNDS):
            k[i] = pow(pow(sbox[sbox[sbox[((((k[i] << 4) ^ k[i]) << 4) ^ k[i]) % 256]]], pow(k[i], k[i]), 256), pow(sbox[k[i]], sbox[k[i]]), 256)

def final_schedule(k):
    for i in range(4):
        k[i] = sbox[k[i]]

def bytes2matrix(text):
    return [list(text[i:i+2]) for i in range(0, len(text), 2)]

def matrix2bytes(matrix):
    return bytes(sum(matrix, []))

def pad(plaintext):
    padding_len = 4 - (len(plaintext) % 4)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(plaintext):
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message

def split_blocks(message, block_size=4, require_padding=True):
        assert len(message) % block_size == 0 or not require_padding
        return [message[i:i+4] for i in range(0, len(message), block_size)]

def encrypt(p, k):
    ciphertext = b""
    for i in split_blocks(pad(p)):
        key = k.copy()
        i = bytes2matrix(i)
        add_round_key(i, key)
        for j in range(ROUNDS):
            schedule_key(key)
            sub_bytes(i)
            shift_rows(i)
            mix_columns(i)
            add_round_key(i, key)
        final_schedule(key)
        final_sub(i)
        final_shift(i)
        final_add(i, key)
        ciphertext += matrix2bytes(i)
    return ciphertext


print(encrypt(flag, key).hex())
```

# 1. Phân tích hiện trường

Đây là một bài AES nhưng trên ma trận $2 \times 2$. Ma trận đầu vào có dạng $$\begin{pmatrix}s_{00} & s_{01} \\ s_{10} & s_{11}\end{pmatrix}$$

Các động tác cơ bản giống với AES gốc, bao gồm: add round key, shift rows, mix columns và sub bytes. Đối với vòng cuối sử dụng một biến thể của sub byte, shift rows và add round key. Ở bài này có 100 vòng biến đổi bình thường và 1 vòng cuối sử dụng các biến thể trên.

## 1.1. Sub Bytes và Final Sub Bytes

SBox được sử dụng trong bài là SBox của AES gốc. Do đó mình cũng không nghĩ rằng sẽ khai thác được gì ở đây. Ở đây có một điều mình cần nhớ là Sub Bytes biến đổi trên cột đầu, và Final Sub Bytes biến đổi trên cột sau.

Đối với Sub Bytes thì

$$\begin{pmatrix} s_{00} & s_{01} \\ s_{10} & s_{11} \end{pmatrix} \to \begin{pmatrix} s_{00} & S(s_{01}) \\ s_{10} & S(s_{11}) \end{pmatrix}$$

Đối với Final Sub Bytes thì

$$\begin{pmatrix} s_{00} & s_{01} \\ s_{10} & s_{11} \end{pmatrix} \to \begin{pmatrix} S(s_{00}) & s_{01} \\ S(s_{10}) & s_{11} \end{pmatrix}$$

## 1.2. Shift Rows và Final Shift Rows

Đối với Shift Rows thay đổi vị trí 2 bytes ở cột (?) đầu.

$$\begin{pmatrix} s_{00} & s_{01} \\ s_{10} & s_{11}\end{pmatrix} \to \begin{pmatrix}s_{10} & s_{01} \\ s_{00} & s_{11}\end{pmatrix}$$

Đối với Final Shift Rows thay đổi vị trí 2 bytes ở cột (?) sau.

$$\begin{pmatrix} s_{00} & s_{01} \\ s_{10} & s_{11}\end{pmatrix} \to \begin{pmatrix} s_{00} & s_{11} \\ s_{10} & s_{01} \end{pmatrix}$$

Mình thấy rằng phép biến đổi ngược đối với shift rows và final shift rows cũng là chính nó.

## 1.3. Mix Columns

Đối với Mix Columns, cột đầu mới sẽ là cột đầu cũ XOR với cột sau.

$$\begin{pmatrix} s_{00} & s_{01} \\ s_{10} & s_{11} \end{pmatrix} \to \begin{pmatrix} s_{00} \oplus s_{01} & s_{01} \\ s_{10} \oplus s_{11} & s_{11} \end{pmatrix}$$

Tương tự shift rows, phép biến đổi ngược của mix columns cũng là chính nó.

## 1.4. Add Round Keys

Phép Add Round Keys ở bài này khá thú vị (mặc dù mình cũng không khai thác từ đó).

```python
def add_round_key(s, k):
    for i in range(2):
        for j in range(2):
            s[i][j] ^= k[k[k[k[i*2+j]%4]%4]%4]
```

Đối với final add round keys thì chỉ thực hiện phép XOR trên cột sau.

Okay, tới đây thì việc phân tích mã hóa của bài này đã tạm xong và mình cũng không thấy điểm nào có thể dùng để khai thác (hoặc chưa thấy). Điều làm mình quan tâm là hàm `schedule_key`.

## 1.5. Key Schedule

```python
def schedule_key(k):
    for i in range(4):
        for j in range(2*ROUNDS):
            k[i] = pow(pow(sbox[sbox[sbox[((((k[i] << 4) ^ k[i]) << 4) ^ k[i]) % 256]]], pow(k[i], k[i]), 256), pow(sbox[k[i]], sbox[k[i]]), 256)

def final_schedule(k):
    for i in range(4):
        k[i] = sbox[k[i]]
```

Hàm sinh khóa con khá lạ. Do đó mình thử in ra khóa con ở các vòng với một chút điều chỉnh ở hàm `encrypt` với các khóa được random.

```python
def encrypt(p, k):
    ciphertext = b""
    for i in split_blocks(p):
        key = k.copy()
        i = bytes2matrix(i)
        add_round_key(i, key)
        for j in range(ROUNDS):
            schedule_key(key)
            print(f"{j}, {key}")
            sub_bytes(i)
            shift_rows(i)
            mix_columns(i)
            add_round_key(i, key)
        final_schedule(key)
        print(f"100, {key}")
        final_sub(i)
        final_shift(i)
        final_add(i, key)
        ciphertext += matrix2bytes(i)
    return ciphertext

pt = b"haha"
for _ in range(1000):
    key = [random.choice(range(256)) for _ in range(4)]
    encrypt(pt, key)
```

Các khóa con trong các vòng từ 0 tới 99 đều có vẻ như nằm trong một tập hợp nhất định là $\{ 0, 1, 175 \}$. Từ đó khóa con ở vòng 100 (vòng final) cũng nằm trong một tập hợp nhất định do đã đi qua hàm sbox (`final_schedule`) và kết quả là tập $\{99, 121, 124 \}$.

# 2. Truy tìm đầu mối

## 2.1. Nơi tình yêu ~~cryptanalysis~~ bắt đầu

Chiến thuật của mình là tìm khóa trước khi đi vào vòng lặp với known-plaintext là format của flag. Chú ý rằng ở đây không cần phải tìm khóa ban đầu mà chỉ cần tìm khóa trước khi vào vòng lặp, tức là khóa tham gia vào phép XOR `add_round_key` đầu tiên.

```python
def encrypt(p, k):
    ciphertext = b""
    for i in split_blocks(p):
        key = k.copy()
        i = bytes2matrix(i)
        add_round_key(i, key)
        #   Find intermediate key used in add_round_key #
        for j in range(ROUNDS):
            schedule_key(key)
            sub_bytes(i)
            shift_rows(i)
            mix_columns(i)
            add_round_key(i, key)
        final_schedule(key)
        final_sub(i)
        final_shift(i)
        final_add(i, key)
        ciphertext += matrix2bytes(i)
    return ciphertext
```

Để tìm khóa ở điểm được đánh dấu, mình sẽ đi ngược từ ciphertext lên. Mình bruteforce các khóa con dùng trong vòng lặp ($3^4 = 81$ trường hợp). Ứng với mỗi khóa con cho vòng lặp mình có một khóa con cho vòng cuối cùng (final). Kết hợp hai khóa đó và ciphertext mình sẽ tìm được state trước khi vào vòng lặp. Cuối cùng mình XOR kết quả đó cho known-plaintext thì sẽ được khóa ở điểm được đánh dấu.

Từ nhận xét bên trên, 100 vòng (0 tới 99) sử dụng cùng một khóa con, mình đặt là $k_1$. Ở vòng final sử dụng một khóa con, mình đặt là $k_2$. Quan hệ giữa chúng là `k_2 = final_schedule(k_1)`.

## 2.2. Man-In-The-Middle

Với mỗi block 4 bytes ciphertext và known-plaintext tương ứng, mình đi ngược từ dưới lên để tìm key trung gian. Lưu ý rằng mình chỉ cần xây dựng bảng `inv_sbox` vì các phép biến đổi khác có phép biến đổi ngược là chính nó.

```python
final_add(ciphertext, k2_)
final_shift(ciphertext)
inv_final_sub(ciphertext)
for j in range(ROUNDS):
    add_round_key(ciphertext, k1_)
    mix_columns(ciphertext)
    shift_rows(ciphertext)
    inv_sub_bytes(ciphertext)

pt = matrix2bytes(plaintext)
ct = matrix2bytes(ciphertext)
key = xor(pt, ct)
```

Với format flag là `amateursCTF{` có 12 bytes tương ứng 3 block, mình thực hiện biến đổi trên với 12 bytes ciphertext tương ứng. Với mỗi block mình sẽ tìm ra được tập hợp các key tương ứng với các $k_1$ (và $k_2$ tương ứng với $k_1$). Sau đó mình giao các tập hợp key lại sẽ được key ban đầu.

Nói cách khác

```python
candidates1 = set()
candidates2 = set()
candidates3 = set()

for k1 in product(K1, repeat=4):
    k2 = final_schedule_(list(k1))

    k1_ = list(k1).copy()
    k2_ = list(k2).copy()

    # Phase 1
    plaintext = bytes2matrix(flag[:4])
    ciphertext = bytes2matrix(ctx[:4])
    final_add(ciphertext, k2_)
    final_shift(ciphertext)
    inv_final_sub(ciphertext)
    for j in range(ROUNDS):
        add_round_key(ciphertext, k1_)
        mix_columns(ciphertext)
        shift_rows(ciphertext)
        inv_sub_bytes(ciphertext)

    pt = matrix2bytes(plaintext)
    ct = matrix2bytes(ciphertext)
    key = xor(pt, ct)
    candidates1.add(bytes(key))
    
    # Phase 2
    plaintext = bytes2matrix(flag[4:8])
    ciphertext = bytes2matrix(ctx[4:8])
    final_add(ciphertext, k2)
    final_shift(ciphertext)
    inv_final_sub(ciphertext)
    for j in range(ROUNDS):
        add_round_key(ciphertext, k1_)
        mix_columns(ciphertext)
        shift_rows(ciphertext)
        inv_sub_bytes(ciphertext)
    
    pt = matrix2bytes(plaintext)
    ct = matrix2bytes(ciphertext)
    key = xor(pt, ct)
    candidates2.add(bytes(key))
    
    # Phase 3
    plaintext = bytes2matrix(flag[8:12])
    ciphertext = bytes2matrix(ctx[8:12])
    final_add(ciphertext, k2_)
    final_shift(ciphertext)
    inv_final_sub(ciphertext)
    for j in range(ROUNDS):
        add_round_key(ciphertext, k1_)
        inv_mix_columns(ciphertext)
        inv_shift_rows(ciphertext)
        inv_sub_bytes(ciphertext)
    
    pt = matrix2bytes(plaintext)
    ct = matrix2bytes(ciphertext)
    key = xor(pt, ct)
    candidates3.add(bytes(key))

key = list(candidates1.intersection(candidates2).intersection(candidates3))
print(key)
```

Kết quả khi giao ba tập hợp chỉ có đúng một key `b'\x00**\x00'`. Quá tốt!!!

Ờ mà khoan, từ từ đã :)))) Có gì đó không đúng lắm. Cụ thể là khi mình encrypt hai block plaintext đầu thì nó không ra đúng ciphertext. Cụ thể hơn nữa, encrypt ra đúng ở vị trí 0 và 2, sai ở vị trí 1 và 3 cho mỗi block (?!?!).

## 2.3. Sửa chữa lỗi lầm

Mình mất cả ngày để tìm lỗi sai nhưng thất bại. Và mình đã chuyển sang *tấn công cưỡng ép*. Vì encrypt đúng ở vị trí 0 và 2 còn sai ở vị trí 1 và 3 nên mình kết luận được là $k_2$ có vấn đề, tức là key ở bước `final_add`.

Mình thử in ra $k_1$ và $k_2$ tương ứng với khóa tìm được bên trên `b'\x00**\x00'`.

```python
for k1 in product(K1, repeat=4):
    k2 = final_schedule_(list(k1))

    k1_ = list(k1).copy()
    k2_ = list(k2).copy()

    # Phase 1
    plaintext = bytes2matrix(flag[:4])
    ciphertext = bytes2matrix(ctx[:4])
    final_add(ciphertext, k2_)
    final_shift(ciphertext)
    inv_final_sub(ciphertext)
    for j in range(ROUNDS):
        add_round_key(ciphertext, k1_)
        mix_columns(ciphertext)
        shift_rows(ciphertext)
        inv_sub_bytes(ciphertext)

    pt = matrix2bytes(plaintext)
    ct = matrix2bytes(ciphertext)
    key = xor(pt, ct)
    candidates1.add(bytes(key))
    if bytes(key) == b'\x00**\x00':
        print(k1, k2)
```

Hai trường hợp có thể xảy ra cho cặp $(k_1, k_2)$ là $([1, 0, 0, 1], [124, 99, 99, 124])$ và
$([1, 0, 175, 1], [124, 99, 121, 124])$. Mình chỉ cần xét trường hợp 1 là được.

Khi nhìn vào hàm `final_add` thì mình biết chắc rằng `k[k[k[k[i*2+1]]]` chắc chắn nằm trong `[124, 99]` nên mình *bốc* đại $k_2 = [124, 124, 124, 124]$, và nó đã thành công (????).

Hàm `decrypt` mình fix cứng $k_1$ và $k_2$ luôn, và decrypt ra toàn bộ flag ban đầu.

```python
def decrypt(c, k):
    plaintext = b""

    for i in split_blocks(c):
        key = k.copy()
        k1, k2 = [1, 0, 0, 1], [124, 124, 124, 124]

        i = bytes2matrix(i)

        final_add(i, k2)
        final_shift(i)
        inv_final_sub(i)
        for j in range(ROUNDS):
            add_round_key(i, k1)
            mix_columns(i)
            shift_rows(i)
            inv_sub_bytes(i)

        plaintext += bytes(xor(matrix2bytes(i), key))
    return plaintext
```

Flag `b'amateursCTF{th1s_1s_wh4t_bad_k3y_sch3dul1ng_d03s_t0_a_p3rson_109bcd1f}\x02\x02`

Nếu bạn nhìn thấy được điểm sai nào đó trong bài làm của mình dẫn tới *tấn công cưỡng ép* thì có thể nói cho mình biết. Thực sự thì mình không biết mình đang lag chỗ nào :confused: