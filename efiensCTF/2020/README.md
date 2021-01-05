# Efiens CTF 2020

## Crypto

### 1. BabyRSA

Các bạn xem đề bài ở [đây](babysra.py)

Ở đây người ra đề cho RSA với e=65537, n=p * q với p, q là số nguyên tố 512 bit và ẩn đi 45% số bit đó bằng hàm **leak**. Mình dựa trên các bit không bị ẩn đi để tìm lại p và q.

Nhận xét rằng k bits thấp nhất của n (LSB) sẽ chỉ bị ảnh hưởng bởi k bits thấp nhất của p và q. Từ đó mình viết hàm bruteforce các bit của p và q từ thấp lên cao cho tới khi nhận được tích pq đúng bằng n.

Code của mình ở [đây](babyrsa_solve.py)

Flag: **EFIENSCTF{\_\_\_Basic_RSA_chall_:)___}**

### 2. ECBC

Các bạn xem đề bài ở [đây](ecbc.py)

Hàm **encrypt** sẽ theo biểu diễn nhị phân của flag mà mã hóa input của mình. Với mỗi bit của flag, nếu là 0 thì sẽ mã hóa input bằng AES với mode là CBC, nếu là 1 sẽ mã hóa bằng AES với mode ECB. Mỗi lần như vậy key random. Tuy nhiên, nếu mình truyền vào 2 blocks plaintext P1 và P2 giống nhau (P1 và P2 là các block 16 bytes) thì AES sẽ cho 2 ciphertext C1 và C2 giống nhau, còn CBC thì không. Vì vậy mình gửi lên server 32 ký tự giống nhau =)))) Ở đây mình truyền b'a' * 32.


Dựa vào nhận xét trên, mình recover được flag

Code của mình ở [đây](ecbc_solve.py)

Flag: **EFIENSCTF{Now_you_know_ECB_is_weak_;)_}**

### 3. Four Time Pad

Các bạn xem đề ở [đây](fourtimepad.py)

Đề bài sử dụng 4 seed bị giấu để sinh ra 4 số random a, b, c, d và cho chúng ta biết *magic number* là ~(a)^(b&c)^(c|d) và *ciphertext* là ct=flag^a^b^c^d. Ở đây mình bruteforce b, c, d và dựa trên hàm **twist** để tìm lại a. Tức là a=~(magic_number ^ (b&c) ^ (c|d))

Code của mình ở [đây](fourtimepad_solve.py)

Flag: **EFIENSCTF{Kowalski_Analy5isss!!}**

### 4. ROT1000

Các bạn xem đề ở [đây](rot1000.py)

Đề bài mã hóa flag như sau:

- Mã hóa Caesar flag x lần (x random từ 1 tới 1000). Mỗi lần rotate 1 số random từ 1 tới 26. Kết quả cuối cùng vẫn là rotate flag 1 số nào đó từ 1 tới 26. 

- Encode base64 chuỗi vừa nhận được và lưu thành biến **cipher**

- Biến kết quả **l** được tạo ra từ công thức l[i]=cipher[i]^cipher[(i+1)%len(cipher)]

- Trả về base64 của **l**

Đầu tiên mình decode base64 của ciphertext. Mình bruteforce để xem ký tự cuối của biến **cipher** ở trên là gì. Do đó là ký tự in được nên mình cho từ 32 tới 128, từ đó dựa vào **l** mình khôi phục lại biến **cipher** và thử decode và tìm được flag

Code của mình ở [đây](rot1000_solve.py)

Flag: **EFIENSCTF{\_WARMUP_BABE_:)_ENJOY_THE_CTF_}**