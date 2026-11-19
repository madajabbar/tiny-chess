import json, os, sys, urllib.request, urllib.error

V = [0, 100, 320, 330, 500, 900, 0]

PA = [0,0,0,0,0,0,0,0, 50,50,50,50,50,50,50,50, 10,10,20,30,30,20,10,10,
      5,5,10,25,25,10,5,5, 0,0,0,20,20,0,0,0, 5,-5,-10,0,0,-10,-5,5,
      5,10,10,-20,-20,10,10,5, 0,0,0,0,0,0,0,0]
PN = [-50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,0,0,0,-20,-40, -30,0,10,15,15,10,0,-30,
      -30,5,15,20,20,15,5,-30, -30,0,15,20,20,15,0,-30, -30,5,10,15,15,10,5,-30,
      -40,-20,0,5,5,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50]
PB = [-20,-10,-10,-10,-10,-10,-10,-20, -10,0,0,0,0,0,0,-10, -10,0,5,10,10,5,0,-10,
      -10,5,5,10,10,5,5,-10, -10,0,10,10,10,10,0,-10, -10,10,10,10,10,10,10,-10,
      -10,5,0,0,0,0,5,-10, -20,-10,-10,-10,-10,-10,-10,-20]
PR = [0,0,0,0,0,0,0,0, 5,10,10,10,10,10,10,5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5,
      -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, 0,0,0,5,5,0,0,0]
PQ = [-20,-10,-10,-5,-5,-10,-10,-20, -10,0,0,0,0,0,0,-10, -10,0,5,5,5,5,0,-10,
      -5,0,5,5,5,5,0,-5, 0,0,5,5,5,5,0,-5, -10,5,5,5,5,5,0,-10,
      -10,0,5,0,0,0,0,-10, -20,-10,-10,-5,-5,-10,-10,-20]
PK = [-30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
      -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10,
      20,20,0,0,0,0,20,20, 20,30,10,0,0,10,30,20]
PST = [None, PA, PN, PB, PR, PQ, PK]

bd = [0]*128
K = [0, 0]
EP = 0
CA = 0
HS = []

NVEC = (18,33,31,14,-18,-33,-31,-14)
KVEC = (16,-16,1,-1,17,15,-17,-15)

def lf(fen):
    global bd, K, EP, CA
    ps = fen.split()
    bd = [0]*128
    K = [0, 0]
    r = 7; fi = 0
    for c in ps[0]:
        if c == '/':
            r -= 1; fi = 0
        elif c.isdigit():
            fi += int(c)
        else:
            s = r*16+fi
            v = " PNBRQK".index(c.upper())
            if c.isupper():
                bd[s] = v
                if v == 6: K[0] = s
            else:
                bd[s] = -v
                if v == 6: K[1] = s
            fi += 1
    CA = 0
    if 'K' in ps[2]: CA |= 1
    if 'Q' in ps[2]: CA |= 2
    if 'k' in ps[2]: CA |= 4
    if 'q' in ps[2]: CA |= 8
    EP = 0
    if ps[3] != '-':
        EP = (int(ps[3][1])-1)*16 + ord(ps[3][0]) - 97
    return ps[1]

def at(s, a):
    for d in NVEC:
        n = s + d
        if not n & 0x88 and bd[n] == 2*a: return 1
    for d in KVEC:
        n = s + d
        if not n & 0x88 and bd[n] == 6*a: return 1
    for d in (17,15,-17,-15):
        n = s + d
        while not n & 0x88:
            o = bd[n]
            if o:
                if o*a > 0 and (o == 3*a or o == 5*a): return 1
                break
            n += d
    for d in (16,-16,1,-1):
        n = s + d
        while not n & 0x88:
            o = bd[n]
            if o:
                if o*a > 0 and (o == 4*a or o == 5*a): return 1
                break
            n += d
    for d in (15,17):
        n = s - d*a
        if not n & 0x88 and bd[n] == a: return 1
    return 0

def gen(a):
    ms = []
    for f in range(128):
        if f & 0x88: continue
        p = bd[f]
        if p*a <= 0: continue
        t = abs(p)
        if t == 1:
            d = 16*a
            n = f + d
            if not n & 0x88 and not bd[n]:
                if n >> 4 in (0, 7):
                    for q in (5, 4, 3, 2): ms.append(f | n<<8 | q<<16)
                else:
                    ms.append(f | n<<8)
                    n2 = n + d
                    if f >> 4 in (1, 6) and not bd[n2]: ms.append(f | n2<<8)
            for e in (-1, 1):
                n = f + d + e
                if n & 0x88: continue
                if bd[n]*a < 0:
                    if n >> 4 in (0, 7):
                        for q in (5, 4, 3, 2): ms.append(f | n<<8 | q<<16)
                    else: ms.append(f | n<<8)
                elif n == EP and n:
                    ms.append(f | n<<8)
        elif t == 2:
            for d in NVEC:
                n = f + d
                if not n & 0x88 and bd[n]*a <= 0: ms.append(f | n<<8)
        elif t == 6:
            for d in KVEC:
                n = f + d
                if not n & 0x88 and bd[n]*a <= 0: ms.append(f | n<<8)
            if a > 0:
                if CA & 1 and not bd[5] and not bd[6] and bd[7] == 4 and not at(4,-1) and not at(5,-1) and not at(6,-1): ms.append(4 | 6<<8)
                if CA & 2 and not bd[3] and not bd[2] and not bd[1] and bd[0] == 4 and not at(4,-1) and not at(3,-1) and not at(2,-1): ms.append(4 | 2<<8)
            else:
                if CA & 4 and not bd[117] and not bd[118] and bd[119] == -4 and not at(116,1) and not at(117,1) and not at(118,1): ms.append(116 | 118<<8)
                if CA & 8 and not bd[115] and not bd[114] and not bd[113] and bd[112] == -4 and not at(116,1) and not at(115,1) and not at(114,1): ms.append(116 | 114<<8)
        else:
            if t == 3: ds = (17,15,-17,-15)
            elif t == 4: ds = (16,-16,1,-1)
            else: ds = KVEC
            for d in ds:
                n = f + d
                while not n & 0x88:
                    o = bd[n]
                    if not o: ms.append(f | n<<8)
                    else:
                        if o*a < 0: ms.append(f | n<<8)
                        break
                    n += d
    return ms

def mk(m):
    global EP, CA
    f = m & 255; t = (m >> 8) & 255; q = (m >> 16) & 255
    p = bd[f]; cap = bd[t]
    hs = (m, p, cap, CA, EP, 0, 0, 0, 0)
    bd[f] = 0; bd[t] = 0
    if abs(p) == 1 and not cap and (f & 7) != (t & 7):
        cs = t - 16 if p > 0 else t + 16
        cp = bd[cs]
        bd[cs] = 0
        hs = (m, p, cap, CA, EP, cs, cp, 0, 0)
    if abs(p) == 6:
        K[0 if p > 0 else 1] = t
        if abs(f - t) == 2:
            rf = t+1 if t > f else t-2
            rt = t-1 if t > f else t+1
            bd[rt] = bd[rf]; bd[rf] = 0
            hs = hs[:7] + (rf, rt)
    bd[t] = (q if p > 0 else -q) if q else p
    EP = (f+t)//2 if abs(p) == 1 and abs(t-f) == 32 else 0
    if abs(p) == 6: CA &= ~(3 if p > 0 else 12)
    if f == 0 or t == 0: CA &= ~2
    if f == 7 or t == 7: CA &= ~1
    if f == 112 or t == 112: CA &= ~8
    if f == 119 or t == 119: CA &= ~4
    HS.append(hs)

def um():
    global EP, CA
    m, p, cap, CA, EP, cs, cp, rf, rt = HS.pop()
    f = m & 255; t = (m >> 8) & 255
    bd[f] = p; bd[t] = cap
    if cs:
        bd[cs] = cp
    if rt:
        bd[rf] = bd[rt]; bd[rt] = 0
    if abs(p) == 6: K[0 if p > 0 else 1] = f

def ev(a):
    s = 0
    for f in range(120):
        if f & 0x88: continue
        p = bd[f]
        if not p: continue
        t = p if p > 0 else -p
        if p > 0: i = (7 - (f >> 4))*8 + (f & 7); s += V[t] + PST[t][i]
        else: i = (f >> 4)*8 + (f & 7); s -= V[t] + PST[t][i]
    return s*a

KL = [0]*64
KD = 0

def keyf(m):
    f = m & 255; t = (m >> 8) & 255; q = (m >> 16) & 255
    cap = bd[t]
    if not cap:
        return -1 if m == KL[KD] else (0 if not q else -V[q])
    return -(V[cap if cap > 0 else -cap]*16 - V[abs(bd[f])])

NODES = 0
LIMIT = 0

class Stop(Exception):
    pass

def qs(a, al, be):
    global NODES
    NODES += 1
    if NODES > LIMIT: raise Stop
    chk = at(K[0 if a > 0 else 1], -a)
    if not chk:
        s = ev(a)
        if s >= be: return be
        if s > al: al = s
    for m in gen(a):
        f = m & 255; t = (m >> 8) & 255; q = (m >> 16) & 255
        if not chk and not bd[t] and not q and t != EP: continue
        mk(m)
        if at(K[0 if a > 0 else 1], -a):
            um(); continue
        v = -qs(-a, -be, -al)
        um()
        if v >= be: return be
        if v > al: al = v
    return al

def ne(a, d, al, be):
    global NODES, KD
    NODES += 1
    if NODES > LIMIT: raise Stop
    if d <= 0: return qs(a, al, be)
    KD = d
    ms = gen(a)
    ms.sort(key=keyf)
    n = 0
    for m in ms:
        mk(m)
        if at(K[0 if a > 0 else 1], -a):
            um(); continue
        n += 1
        v = -ne(-a, d-1, -be, -al)
        um()
        if v >= be:
            if not bd[(m >> 8) & 255] and not (m >> 16) & 255: KL[d] = m
            return be
        if v > al: al = v
    if not n: return -30000
    return al

import json as _j

CAP = 40000

def search(fen, legs, cap=CAP):
    global NODES, LIMIT
    a = 1 if lf(fen) == 'w' else -1
    KL[:] = [0]*64
    HS.clear()
    rs = []
    for u in legs:
        f = (int(u[1])-1)*16 + ord(u[0]) - 97
        t = (int(u[3])-1)*16 + ord(u[2]) - 97
        q = '  nbrq'.index(u[4]) if len(u) > 4 else 0
        rs.append(f | t<<8 | q<<16)
    rs.sort(key=keyf)
    bm = rs[0]
    for D in range(1, 64):
        NODES = 0; LIMIT = cap
        al = -10**9; cur = bm
        try:
            for m in rs:
                mk(m)
                v = -ne(-a, D-1, -10**9, -al)
                um()
                if v > al: al = v; cur = m
        except Stop:
            break
        bm = cur
    f = bm & 255; t = (bm >> 8) & 255; q = (bm >> 16) & 255
    return chr(97+f%16)+str(f//16+1)+chr(97+t%16)+str(t//16+1)+('  nbrq'[q] if q else '')

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

def post(path, body):
    req = urllib.request.Request(ENV_URL + path, data=_j.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return _j.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")

def main():
    while True:
        g = post("/game", {})
        if g["status"] == "done":
            break
        while g["status"] == "your_move":
            g = post("/move", {"game": g["game"], "move": search(g["fen"], g["legal_moves"])})
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)

if __name__ == "__main__":
    main()
