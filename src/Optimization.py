from utility import *
from cluster import *
from query import *

def sway(data):
    def worker(rows, worse, above = None):
        if len(rows) <= len(data.rows)**args.min:
            return rows, many(worse, args.rest*len(rows))
        else:
            l , r, A, B,_ = half(data, rows, None, above)
            if better(data, B, A):
                l, r, A, B = r, l, B, A
            map(r, lambda row: worse.append(row))
            return worker(l, worse, A)
    best, rest = worker(data.rows, [])
    return DATA.clone(data, best), DATA.clone(data, rest)

