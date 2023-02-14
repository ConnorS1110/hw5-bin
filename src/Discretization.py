from range import *
from update import *

def bins(cols, rowss):
    out = []
    for col in cols:
        ranges = []
        for y, rows in enumerate(rowss):
            for row in rows:
                x, k = row[col.at]
                if x != "?":
                    k = bin(col, x)
                    ranges[k] = ranges[k] if ranges[k] else RANGE(col.at, col.txt, x)
                    extend(ranges[k], x, y)
        ranges = sorted(map(ranges, itself))
        out.append(ranges if col.isSym else mergeAny(ranges))
    return out

