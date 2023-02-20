from list import *
from utility import *
import utility as util
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

def stats(data, fun = None, cols = None, nPlaces = 2):
    """
    Function:
        stats
    Description:
        Gets a given statistic and returns the rounded answer
    Input:
        self - current DATA instance
        what - statistic to be returned
        cols - cols to use as the data for statistic
        nPlaces - # of decimal places stat is rounded to
    Output:
        map of cols y position and anonymous function that calculates the rounded stat
    """
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
    for x, n in has.items():
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
        if hasattr(col, "isSym"):
            return 0 if x == y else 1
        else:
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
        d += dist1(col.col, float(t1[col.col.at]), float(t2[col.col.at]))**util.args.p
    return (d / n)**(1 / util.args.p)

def better(data, row1, row2):
    s1, s2, ys = 0, 0, data.cols.y
    for col in ys:
        x = norm(col.col, float(row1[col.col.at]) if row1[col.col.at] != "?" else row1[col.col.at])
        y = norm(col.col, float(row2[col.col.at]) if row2[col.col.at] != "?" else row2[col.col.at])

        s1 = s1 - math.exp(col.col.w * (x-y)/len(ys))
        s2 = s2 - math.exp(col.col.w * (y - x)/len(ys))

    return s1/len(ys) < s2 / len(ys)
