from utility import *
# from list import many : defined many here to avoid circular import error
import re
import math
import utility as util

Seed = 937162211

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


def itself(x):
    return x

def cliffsDelta(lst1, lst2, d: float = 0.147) -> bool:
    n1, n2 = len(lst1), len(lst2)
    m, sum = 0, 0
    for i in range(n1):
        for j in range(n2):
            if lst1[i] < lst2[j]:
                m += 1
            elif lst1[i] > lst2[j]:
                m -= 1
    if m == 0:
        return False
    else:
        x = n1 * n2
        d = abs(m) / x
        return d >= 0.147

def diffs(nums1, nums2):
    def kap(nums, fn):
        return [fn(k, v) for k, v in enumerate(nums)]
    return kap(nums1, lambda k, nums: (cliffsDelta(nums['has'], nums2[k]['has']), nums['txt']))

def coerce(s):
    def fun(s1):
        if s1 == "true":
            return True
        elif s1 == "false":
            return False
        return s1

    return math.tointeger(s) or float(s) or fun(s.strip())

def cells(s):
    t = []
    for s1 in re.findall("[^,]+", s):
        t.append(coerce(s1))
    return t

def lines(sFilename, fun):
    with open(sFilename, "r") as src:
        for s in src:
            s = s.rstrip("\r\n")
            fun(s)
    src.close()

def csv(sFilename, fun):
    lines(sFilename, lambda line: fun(cells(line)))

def rand(low, high):
    """
    Function:
        rand
    Description:
        Creates a random number
    Input:
        low - low value
        high - high value
    Output:
        Random number
    """
    global Seed
    low, high = low or 0, high or 1
    Seed = (16807 * Seed) % 2147483647
    return low + (high - low) * Seed / 2147483647

def rint(lo = None, hi = None):
    """
    Function:
        rint
    Description:
        Makes a random number
    Input:
        low - low value
        high - high value
    Output:
        Random number
    """
    return math.floor(0.5 + rand(lo, hi))
