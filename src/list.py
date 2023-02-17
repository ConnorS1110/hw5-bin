import math
from miscellaneous import *

def many(t, n):
    """
    Function:
        many
    Description:
        Creates a list of random rows
    Input:
        t - DATA object
        n - Number of row samples
    Output:
        u - list of random n rows from t
    """
    u = []
    for i in range(1, n + 1):
        u.append(any(t))
    return u

def any(t):
    """
    Function:
        any
    Description:
        Selects a random row
    Input:
        t - DATA object
    Output:
        Random row from t
    """
    rintVal = rint(None, len(t) - 1)
    return t[rintVal]

def per(t, p):
    p = math.floor(((p or 0.5) * len(t)) + 0.5)
    return t[max(1, min(len(t), p))]

def kap(listOfCols, fun):
    """
    Function:
        kap
    Description:
        Creates map that stores functions as value
    Input:
        listOfCols - list of columns
        fun - anonymous function to be used as value in map
    Output:
        u - map of anonymous functions
    """
    u = {}
    for k, v in enumerate(listOfCols):
        v, k = fun(k, v)
        u[k or len(u)+1] = v
    return u

def slice(t, go = None, stop = None, inc = None):
    if go and go < 0:
        go = len(t) - 1 + go
    if stop and stop < 0:
        stop = len(t) + stop
    u = []
    for j in range(int((go or 1)), int((stop or len(t))), int(inc or 1)):
        u.append(t[j])
    return u
