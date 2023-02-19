from list import *
from utility import *
import math

def has(col):
    if not hasattr(col, "isSym") and not col.ok:
        if isinstance(col.has, dict):
            col.has = dict(sorted(col.has.items(), key = lambda item: item[1]))
        else:
            col.has.sort()
    col.ok = True
    return col.has

def mid(col):
    return col.mode if hasattr(col, "isSym") else per(has(col), 0.5)

def div(col):
    if hasattr(col, "isSym"):
        e = 0
        if isinstance(col.has, dict):
            for n in col.has.values():
                e = e - n/col.n * math.log(n/col.n, 2)
        else:
            for n in col.has:
                e = e - n/col.n * math.log(n/col.n, 2)
        return e
    else:
        return (per(has(col),.9) - per(has(col), .1))/2.58

def stats(data, nPlaces = None, fun = None, cols = None):
    cols = cols or data.cols.y
    def callBack(k, col):
        col = col.col
        return round((fun or mid)(col), nPlaces), col.txt
    tmp = kap(cols, callBack)
    tmp["N"] = len(data.rows)
    return tmp, map(mid, cols)

def norm(num, n):
    """
        Function:
            norm
        Description:
            Normalizes a value
        Input:
            num - current NUM instance
            n - value to normalize
        Output:
            Normalized value
    """
    return n if n == "?" else (n - num.lo) / (num.hi - num.lo + 1 / float("inf"))


def value(has, nB = 1, nR = 1, sGoal = True):
    b, r = 0, 0
    for x, n in enumerate(has):
        if x == sGoal:
            b = b + n
        else:
            r = r + n
    b,r = b/(nB+1/float("inf")), r/(nR+1/float("inf"))
    return (b ** 2) / (b + r)

def dist(data, t1, t2, cols = None):
    def dist1(col, x, y):
        if x == "?" and y == "?":
            return 1
        if col.isSym:
            return 0 if x == y else 1
        x, y = norm(col, x), norm(col, y)
        if x == "?":
            x = 1 if y < 0.5 else 1
        if y == "?":
            y = 1 if x < 0.5 else 1
        return abs(x - y)

    d, n = 0, 1 / float("inf")
    cols = cols if cols else data.cols.x
    for col in cols:
        n += 1
        d += dist1(col, t1[col.at], t2[col.at])**args.p
    return (d / n)**(1 / args.p)

def better(data, row1, row2):
    s1, s2, ys = 0, 0, data.cols.y
    for _, col in enumerate(ys):
        x = norm(col, row1[col.at])
        y = norm(col, row2[col.at])

        s1 = s1 - math.exp(col.w * (x-y)/len(ys))
        s2 = s2 - math.exp(col.w * (y - x)/len(ys))

    return s1/len(ys) < s2 / len(ys)
