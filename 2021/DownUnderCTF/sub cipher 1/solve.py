enc = '𖿫𖝓玲𰆽𪃵𢙿疗𫢋𥆛🴃䶹𬑽蒵𜭱𫢋𪃵蒵🴃𜭱𩕑疗𪲳𜭱窇蒵𱫳'
flag = []
print(len(enc))
for c in enc:
    print(c)
    for i in range(256):
        # print(hex(13*i*i+3*i+7))
        if 13*i*i+3*i+7 == ord(c):
            flag.append(i)
            break
print(bytes(flag))
