from num import NUM
from sym import SYM

def COL(n, s):
    col = NUM(n, s) if s[0].isupper() else SYM(n, s)
    # col['isIgnored'] = 'X' in col['txt']
    # col['isKlass'] = '!' in col['txt']
    # col['isGoal'] = any(x in col['txt'] for x in ['!', '+', '-'])
    return col