
tab = {}
ctr = 0


def head(b):
    return b[1]

def tail(b):
    return b[2]

def width(b):
    if type(b) is tuple:
        return b[0]
    return 1

def cons(a, b):
    return (width(a) + width(b), a, b)

def rule110(a, b, c):
    cond = ((a or b or c)
            and ((not a) or b or c)
            and ((not a) or (not b) or (not c)))
    return int(cond)


def nbit(x, n):
    return 1 & (x >> n)


def init_tab():
    for i in range(16):
        a = nbit(i, 3)
        b = nbit(i, 2)
        c = nbit(i, 1)
        d = nbit(i, 0)
        key = cons(cons(a, b), cons(c, d)) 
        val = cons(rule110(a, b, c), rule110(b, c, d))
        tab[key] = val


def print_block(b):
    if type(b) is tuple:
        print_block(b[1])
        print_block(b[2])
    else:
        print('#' if b else '.', end='')


def print_tab():
    for key, val in tab.items():
        print_block(key)
        print()
        print(' ' * (width(val) // 2), end='')
        print_block(val)
        print('\n')

        
def hash110(block):
    global ctr
    ctr += 1
    if (block) in tab:
        return tab[block]
    #print(f"didn't find width {width(block)} block")
    h = head(block)
    t = tail(block)
    left = hash110(h)
    mid = hash110(cons(tail(h), head(t)))
    right = hash110(t)
    val = cons(hash110(cons(left, mid)), hash110(cons(mid, right)))
    tab[block] = val
    return val

def seed0(n):
    res = 0
    for i in range(n):
        res = cons(res, res)
    return res

def seed1(n):
    res = 1
    pad = 0
    for i in range(n):
        res = cons(pad, res)
        pad = cons(pad, pad)
    return cons(res, pad)

init_tab()
print(width(hash110(seed1(14))))
#print_tab()
print(ctr)

'''
print()
print_block(seed1(4))
print()
'''
