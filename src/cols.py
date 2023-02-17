from num import NUM
from sym import SYM
from col import COL
import re

def COLS(ss):
    cols={"names": ss, "all": [], "x": [], "y": []}
    for n, s in enumerate(ss):
        col = cols["all"].append(COL(n, s))
        if not col["isIgnored"]:
            if col['isKlass']:
                col['isKlass'] = col
            if col.isGoal:
                col.y.append(col)
            else:
                col.x.append(col)
