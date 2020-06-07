from binascii import unhexlify
f = open('pooh.jpg', 'rb')
data = f.read().split(b'  ')
print(data)
f.close()
dec = b''
for i in data:
	tmp = i.split(b'\n')[-1]
	if tmp != b'':
		hexcode = tmp.split(b' ')[1:]
		for j in hexcode:
			dec += unhexlify(j)

dec = dec[-16:] + dec[:-16]
f = open('manipulate.jpg', 'wb')
f.write(dec)
f.close()

# flag: castorsCTF{H3r3_Is_y0uR_Fl4gg}