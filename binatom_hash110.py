
tab = {}

def rule110(a, b, c):
    cond = ((a or b or c)
            and ((not a) or b or c)
            and ((not a) or (not b) or (not c)))
    return 1 if cond else 0

def nbit(x, n):
    return 1 & (x >> n)

def seed():
    for i in range(16):
        a = nbit(i, 3)
        b = nbit(i, 2)
        c = nbit(i, 1)
        d = nbit(i, 0)
        key = ((a << 1) + b, (c << 1) + d) 
        val = (rule110(a, b, c) << 1) + rule110(b, c, d)
        tab[key] = val
seed()
print(tab)


