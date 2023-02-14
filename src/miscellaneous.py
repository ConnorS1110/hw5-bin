from utility import *
from list import *
import re
import math


def itself(x):
    return x

def cliffsDelta(ns1, ns2):
    if len(ns1) > 256:
        ns1 = many(ns1, 256)
    if len(ns2) > 256:
        ns2 = many(ns2, 256)
    if len(ns1) > 10 * len(ns2):
        ns1 = many(ns1, 10 * len(ns2))
    if len(ns2) > 10 * len(ns1):
        ns2 = many(ns2, 10 * len(ns1))
    
    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1
                
    return abs(lt - gt) / n > args.cliffs

def diffs(nums1, nums2):
    def kap(nums, fn):
        return [fn(k, v) for k, v in enumerate(nums)]
    return kap(nums1, lambda k, nums: (cliffsDelta(nums['has'], nums2[k]['has']), nums['txt']))

import math

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