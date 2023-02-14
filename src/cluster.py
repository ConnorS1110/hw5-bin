from query import *
from data import *



def half(data, rows = None, cols = None, above = None):
        """
        Function:
            half
        Description:
            Splits data in half
        Input:
            self - current DATA instance
            rows - rows to split
            cols - cols to split
            above - previous point of split
        Output:
            left - list of rows to the left of split
            right - list of rows to the right of split
            A - far left point
            B - far right point
            mid - mid point where split occurs
            c - Distance between A and B
        """
        def gap(r1, r2):
            return dist(data, r1, r2, cols)
        def cos(a, b, c):
            return (a**2 + c**2 - b**2)/(2*c)
        def proj(r):
            return {'row': r, 'x': cos(gap(r, A), gap(r, B), c)}
        rows = rows or data.rows
        some = many(rows, args.Halves)
        A = above if args.Reuse else any(some)
        tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
        far = tmp[int(len(tmp)*args.Far)]
        B, c = far["row"], far["d"]
        sorted_rows = sorted(map(rows, proj), key=lambda x: x["x"])
        left, right = [], []
        for n, two in enumerate(sorted_rows):
            if n <= (len(rows) - 1) / 2:
                left.append(two["row"])
            else:
                right.append(two["row"])
        return left, right, A, B, c

def tree(data, cols, above, rows = None):
    rows = rows if rows else data.rows
    here = {"data" : DATA.clone(data, rows)}
    if len(rows)>=2*(len(data.rows)**args.min):
        left, right, A, B, _ = half(data, rows, cols, above)
        here["left"] = tree(data, left, cols, A)
        here["right"] = tree(data, right, cols, B)
    return here

def showTree(tree, lvl=0, post=None):
    if tree:
        print("{}[{}]".format("|.. " * lvl, len(tree.data.rows)), end="")
        if lvl == 0 or not tree.left:
            print(stats(tree.data))
        else:
            print("")
        showTree(tree.left, lvl + 1)
        showTree(tree.right, lvl + 1)