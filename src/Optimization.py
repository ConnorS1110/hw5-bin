import utility as util
from cluster import *
from query import *

def sway(data):
    def worker(rows, worse, above = None):
        if len(rows) <= len(data.rows) ** util.args.min:
            return rows, many(worse, util.args.rest*len(rows))
        else:
            l , r, A, B,_ = half(data, rows, None, above)
            if better(data, B, A):
                l, r, A, B = r, l, B, A
            for row in r:
                worse.append(row)
            return worker(l, worse, A)
    best, rest = worker(data.rows, [])
    return data.clone(data, best), data.clone(data, rest)
