with open("basis") as f:
    lines = [line.strip() for line in f.readlines()]
    SECRET_BASIS = [list(map(int, row)) for row in lines]

f.close()