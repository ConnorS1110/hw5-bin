from cols import COLS
import utility as util
import miscellaneous as misc
import random

def row(data, t):
    """
    Function: 
        row
    Description:
        Adds a row t to the data object. If the data.cols attribute 
        is already set, it adds the row to the data.rows list and updates 
        the columns of the data.cols object using the add function. If 
        data.cols is not set, it creates a new data.cols object using the 
        COLS class and then adds the row and updates the columns of the new 
        data.cols object.

    Input:
        data: an object of the DATA class
        t: a list representing a row to be added to data
    Output:
        data: an updated object of the DATA class
    """
    if data.cols:
        data.rows.append(t)
        for cols in [data.cols.x, data.cols.y]:
            for col in cols:
                add(col.col, t[col.col.at])
    else:
        data.cols = COLS(t)
    return data


def add(col, x, n = 1):
    """
    Function: 
        add
    Description:
        Updates the col object based on the given value x. If x is not "?", 
        it increments the col.n attribute by n and if the column is symbolic, 
        it updates the col.has dictionary with the count of the x value. 
        If the column is numeric, it updates the col.lo and col.hi attributes 
        and if the number of unique values in the col.has dictionary is less 
        than util.args.Max, it adds the x value to the col.has dictionary. 
        Otherwise, it has a probability of util.args.Max / col.n to add the x value to the col.has dictionary.
    Input:
        col: an object of the NUM or SYM class
        x: a value to be added to the column col
        n (optional): a positive integer representing the count of x in the data. Default is 1.
    Output: None
    """
    if x != "?":
        col.n += n # Source of variable 'n'
        if hasattr(col, "isSym") and col.isSym:
            col.has[x] = n + (col.has.get(x, 0))
            if col.has[x] > col.most:
                col.most = col.has[x]
                col.mode = x
        else:
            x = float(x)
            col.lo = min(x, col.lo)
            col.hi = max(x, col.hi)
            all = len(col.has)
            if all < util.args.Max:
                pos = all + 1
            elif random.random() < util.args.Max / col.n:
                pos = util.rint(1, all)
            else:
                pos = None
            if pos:
                if isinstance(col.has, dict):
                    col.has[pos] = x
                else:
                    col.has.append(x)
                col.ok = False

def adds(col, t):
    """
    Function: 
        adds
    Description:
        Iterates over the values in the list t and calls the add function to update the col object for each value.
    Input:
        col: an object of the NUM or SYM class
        t: a list of values to be added to the col object
    Output:
        col: an updated object of the NUM or SYM class
    """
    for value in t or []:
        add(col, value)
    return col

def extend(range, n, s):
    """
    Function: 
        extend
    Description:
        Updates the range object with a new minimum and maximum value n, and adds the string s to the range.y column using the add function.
    Input:
        range: an object of the RANGE class
        n: a numeric value to be added to range
        s: a string value to be added to range.y
    Output: None
    """
    range.lo = min(n, range.lo)
    range.hi = max(n, range.hi)
    add(range.y, s)
