from cols import COLS
from utility import *
import random

def row(data, t):
    if data.cols:
        data.rows.append(t)
        for cols in [data.cols.x, data.cols.y]:
            for col in cols:
                add(col, t[col.at])
    else:
        data.cols = COLS(t)
    return data


def add(col, x, n = 1):
    if x != "?":
        col.n = col.n + n # Source of variable 'n'
        if col.isSym:
            col.has[x] = n + (col.has.get(x, 0) or 0)
            if col.has[x] > col.most:
                col.most = col.has[x]
                col.mode = x
        else:
            col.lo = min(x, col.lo)
            col.hi = max(x, col.hi)
            all = len(col.has)
            if all < args.Max:
                pos = all + 1
            elif random.random() < args.Max / col.n:
                pos = rint(1, all)
            else:
                pos = None
            if pos:
                col.has[pos] = x
                col.ok = False

def adds(col, t):
    for value in t or []:
        add(col, value)
    return col

def extend(range, n, s):
    range.lo = min(n, range.lo)
    range.hi = max(n, range.hi)
    add(range.y, s)

