import utility as util
from cluster import *
import query as query

def sway(data):
    """
    Function: 
        sway
    Description:
        Partitions the rows of a dataset into two groups: best and rest. 
        The partitioning is done recursively until a stopping criterion is met. 
        The partitioning is done using a function called worker. The function starts by 
        passing all rows of the dataset to worker. worker then recursively partitions 
        the rows based on some criterion until it determines the best 
        rows (a subset of the original rows that meets the criterion) and the rest of the rows. 
        The criterion is determined by a function called better.
    Input:
        data: a dataset object.
    Output:
        best: a dataset object containing the best rows.
        rest: a dataset object containing the rest of the rows.
    Sub-functions:
    worker: 
        recursive function that partitions the rows based on some criterion until it determines
        the best rows and the rest of the rows.
    better: 
        a function that determines whether one subset of rows is better than another based 
        on some criterion. This function is used by worker to determine the best rows.
    """
    def worker(rows, worse, above = None):
        if len(rows) <= len(data.rows) ** util.args.min:
            return rows, many(worse, util.args.rest*len(rows))
        else:
            l , r, A, B,_ = half(data, rows, None, above)
            if query.better(data, B, A):
                l, r, A, B = r, l, B, A
            for row in r:
                worse.append(row)
            return worker(l, worse, A)
    best, rest = worker(data.rows, [])
    return data.clone(data, best), data.clone(data, rest)
