from sock import Sock

so = Sock('05.cr.yp.toc.tf:14010')

so.read_until(b'[Q]uit\n')
so.send_line(b'g')
n, f, v = so.read_line().strip().split(b' ')[-3:]
n, f, v = int(n[1: -1]), int(f[:-1]), int(v[:-1])

so.read_until(b'[Q]uit\n')
so.send_line(b't')
so.read_line()
so.send_line(b'15')
print(so.read_line())

so.read_until(b'[Q]uit\n')
so.send_line(b't')
so.read_line()
so.send_line(str(-15 + n ** 2).encode())
print(so.read_line())

so.read_until(b'[Q]uit\n')
so.send_line(b'r')
so.read_line()
so.send_line(b'15,'+str(-15+n**2).encode())
print(so.read_line())
so.close()