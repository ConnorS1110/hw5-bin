from utility import *
import math
import utility as util
import list as listModule


def itself(x):
    """
    Function:
        itself

    Description:
        The itself function takes an input value x and returns it as output. 
        This function is essentially an identity function, meaning it returns 
        the same value that was passed in.

    Input:
        x - Any value that can be passed as input.

    Output:
        The same value as the input parameter.
"""
    return x

def cliffsDelta(ns1, ns2):
    """
    Function:
        cliffsDelta
    Description:
        Computes the Cliff's delta effect size between two lists of numerical values. 
        The Cliff's delta measures the difference in distribution between the two lists, 
        taking into account both the magnitude of the difference and the size of the lists.
    Input:
        ns1 - First list of numerical values
        ns2 - Second list of numerical values
    Output:
        A boolean value indicating whether the Cliff's delta effect size between the two 
        lists is greater than a specified threshold.
    """
    if len(ns1) > 256: ns1 = listModule.many(ns1, 256)
    if len(ns2) > 256: ns2 = listModule.many(ns2, 256)
    if len(ns1) > (10 * len(ns2)): ns1 = listModule.many(ns1, 10 * len(ns2))
    if len(ns2) > (10 * len(ns1)): ns2 = listModule.many(ns2, 10 * len(ns1))
    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y: gt += 1
            if x < y: lt += 1
    return abs(lt - gt) / n > util.args.cliffs

def diffs(nums1, nums2):
    """
    Function:
        diffs

    Description:
        The diffs function takes two lists of numerical values nums1 and nums2, 
        and returns a list of tuples. Each tuple contains the result of the cliffsDelta 
        function applied to corresponding elements of nums1 and nums2, as well as the 
        original value from nums1. The cliffsDelta function measures the effect size of 
        the difference between two groups of numerical values.

    Input:
        nums1 - A list of numerical values.
        nums2 - A list of numerical values of the same length as nums1.

    Output:
    A list of tuples, where each tuple contains the result of cliffsDelta applied to
    corresponding elements of nums1 and nums2, and the original value from nums1.
    """
    def kap(nums, fn):
        return [fn(k, v) for k, v in enumerate(nums)]
    return kap(nums1, lambda k, nums: (cliffsDelta(nums.col.has, nums2[k].col.has), nums.col.txt))

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
    """
    Function:
        lines
    Description:
        Reads a text file line by line and applies a given function to each line.
    Input:
        sFilename - Name of the text file to read.
        fun - Function to apply to each line of the text file.
    Output:
        None.
    """
    with open(sFilename, "r") as src:
        for s in src:
            s = s.rstrip("\r\n")
            fun(s)
    src.close()

def csv(sFilename, fun):
    """
    Function:
        csv
    Description:
        Reads a CSV file line by line and applies a given function to each line after converting it to a list of cells.
    Input:
        sFilename - Name of the CSV file to read
        fun - Function to apply to each line of the CSV file
    Output:
        None
    """
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
    low, high = low or 0, high or 1
    util.Seed = (16807 * util.Seed) % 2147483647
    return low + (high - low) * util.Seed / 2147483647

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
