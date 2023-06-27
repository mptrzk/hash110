import random
import blessed

tab = {}
ctr = 0

class cons:
    def __init__(s, a, b):
        s.h = a
        s.t = b
        if (type(a) is not int and type(a) is not cons
            or type(a) is not type(b)):
            raise TypeError(f"wrong types ({type(a)}, {type(b)})")
        if type(a) is cons: 
            if a.width != b.width:
                raise ValueError(f"mismatched widths ({a.width}, {b.width})")
            s.hash = hash((a.hash, b.hash))
            s.width = a.width + b.width
        else:
            s.hash = hash((a, b))
            s.width = 2

    


def get_width(a):
    if type(a) is cons:
        return a.width
    return 1


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
        tab[key.hash] = (key, val)


def print_block(a, nl=True):
    if type(a) is cons:
        print_block(a.h, False)
        print_block(a.t, False)
    else:
        print(u'#' if a else '.', end='')
    if nl:
        print()


def print_tab():
    for key, val in tab.values():
        print_block(key)
        print(' ' * (get_width(val) // 2), end='')
        print_block(val)
        print()


        
def hash110(block):
    global ctr
    ctr += 1
    if (block.hash) in tab:
        return tab[block.hash][1]
    #print(f"didn't find width {get_width(block)} block")
    h = block.h
    t = block.t
    left = hash110(h)
    mid = hash110(cons(h.t, t.h))
    right = hash110(t)
    val = cons(hash110(cons(left, mid)), hash110(cons(mid, right)))
    tab[block.hash] = (block, val)
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

def clone(a, n):
    for i in range(n):
        a = cons(a, a)
    return a

def fill(a, w):
    while get_width(a) < w:
        a = cons(a, a)
    return a

def lpad(a, padding, w=0): #is this ugly?
    padding = fill(padding, get_width(a))
    a = cons(padding, a)
    while get_width(a) < w:
        padding = cons(padding, padding)
        a = cons(padding, a)
    return a

def rpad(a, padding, w=0): #is this ugly?
    padding = fill(padding, get_width(a))
    a = cons(a, padding)
    while get_width(a) < w:
        padding = cons(padding, padding)
        a = cons(a, padding)
    return a

def marble(n):
    res = 1
    nop = 0
    for i in range (n):
        if random.choice((1, 0)):
            res = cons(res, nop)
            nop = cons(nop, nop)
        else:
            res = cons(res, res)
            nop = cons(nop, nop)
    return res

def noise(n):
    if n > 0:
        return cons(noise(n-1), noise(n-1))
    return random.choice((0, 1))



def reduce(a, w):
    while get_width(a) > w:
        a = hash110(a)
    return a

#TODO add exceptions for too shallow trees
def delta(a, depth):
    if depth:
        return cons(delta(a.h, depth - 1), delta(a.t, depth - 1))
    else:
        return 1 if a.h != a.t else 0

def delta_barf():
    s = lpad(noise(10), 0, 2**20)
    hsh = hash110(s)
    nul = clone(0, 7)
    i = 1
    while True:
        res = delta(reduce(s, 2**(7 + i)), 7) #TODO stripy mystery
        print_block(res)
        #WUT !!!! it loops because you can't hash110 less than once
        if res.hash == nul.hash or res.hash == delta(hsh, 7).hash:
            break
        i += 1


def vectorize(a, pos=0, size=0, offset=0):
    if not size:
        size = get_width(a)
    if (offset >= pos + size or offset + get_width(a) - 1 < pos): #edge cases?
        return []
    if get_width(a) == 1:
        return [a]
    return (vectorize(a.h, pos, size, offset)
            + vectorize(a.t, pos, size, offset + get_width(a.h)))
 
def print_vector(v, indent=0):
    print(' ' * indent, end='')
    for el in v:
        #print(u'#' if el else '.', end='')
        print(u'\u2588' if el else '.', end='')
    print()

def vector110(v, n=0):
    if not n:
        n = len(v)//2
    res = [v]
    for i in range(n):
        v_new = []
        for j in range(1, len(v) - 1):
            a, b, c = v[j-1], v[j], v[j+1]
            v_new.append(rule110(a, b, c))
        v = v_new
        res.append(v)
    return res

def print_vsim(vsim, pos=0, width=0, depth_offset=0, depth=0):
    if width == 0:
        width = len(vsim[0])
    if depth == 0:
        depth = len(vsim)
    for i in range(depth_offset, depth_offset + depth):
        print_vector(vsim[i][max(pos - i, 0): max(pos - i + width, 0)],
                     max(i - pos, 0))


def getch():
  with term.cbreak(), term.hidden_cursor():
    return term.inkey()


init_tab()

s = seed1(60)
#r = reduce(s, 128)
r = hash110(s)
v = vectorize(r, 80, 256)
vs = vector110(v)

term = blessed.Terminal()

pos = 0
depth_offset = 0
#print_vsim(vs, pos, term.width, depth_offset, term.height - 1)
while True:
    print(term.home + term.clear)
    print_vsim(vs, pos, term.width, depth_offset, term.height - 1)
    c = getch()
    if c == 'q':
        break
    if c == 'h':
        pos -= 1
    if c == 'l':
        pos += 1
    if c == 'k':
        depth_offset -= 1
    if c == 'j':
        depth_offset += 1
    



'''
s = seed1(6)
print_block(s)
print()
v = vectorize(s)
print_vector(v)
print()
print_vsim(vector110(v, len(v)//4))
print_block(hash110(s))
'''


'''
s = marble(30)
res = delta(seed1(16), 1)
print(get_width(res))
print_block(hash110(seed1(6)))
print(ctr)
print_tab()
'''

'''
print()
print_block(seed1(4))
print()
'''
