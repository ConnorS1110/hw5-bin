import math
import miscellaneous as misc
import utility as util

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
    rintVal = util.rint(None, len(t) - 1)
    return t[rintVal]

def per(t, p):
    """
    Function: 
        per
    Description:
        Returns the value at the specified percentile of the input list t. 
        If the percentile value p is not provided, the default value of 0.5 is used.
        The percentile calculation is performed using the median method.
    Inputs:
        t: a list of values
        p: a value representing the percentile (default is 0.5 if not provided)
    Outputs:
        The value at the pth percentile of t.
    """
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
    """
    Function name: 
        slice

    Description: 
        This function takes a list t and returns a slice of it based on 
        the provided parameters. The go parameter specifies the starting 
        index of the slice (default is 1), the stop parameter specifies 
        the ending index of the slice (default is len(t)), and the inc 
        parameter specifies the step size (default is 1).

    Parameters:
        t: list to be sliced
        go: starting index of the slice (default is 1)
        stop: ending index of the slice (default is len(t))
        inc: step size (default is 1)
    Output:
        A list containing the sliced elements of t.
    """
    if go and go < 0:
        go = len(t) - 1 + go
    if stop and stop < 0:
        stop = len(t) + stop
    u = []
    for j in range(int((go or 1)), int((stop or len(t))), int(inc or 1)):
        u.append(t[j])
    return u
