import math
import random
from typing import List

def cliffsDelta(lst1: List[float], lst2: List[float], d: float = 0.147) -> bool:
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

def push(lst: List[float], val: float):
    lst.append(val)

def map(lst: List[float], f):
    return [f(x) for x in lst]

def rnd(num: float):
    return round(num, 3)

def go(arg1, arg2, func):
    func([], [], [])
    print("All tests passed")
    return True

def test_cliffsDelta(t1, t2, t3):
    assert cliffsDelta([8,7,6,2,5,8,7,3], [8,7,6,2,5,8,7,3]) == False, "1"
    assert cliffsDelta([8,7,6,2,5,8,7,3], [9,9,7,8,10,9,6]) == True, "2"

    t1, t2 = [], []
    for i in range(1000):
        t1.append(random())
        t2.append(math.sqrt(random()))

    assert cliffsDelta(t1, t1) == False, "3"
    assert cliffsDelta(t1, t2) == True, "4"

    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x * j, t1))
        diff = cliffsDelta(t1, t3)
        print(">", round(j, 2), diff)
        j *= 1.025


go("cliffs","stats tests", test_cliffsDelta)
