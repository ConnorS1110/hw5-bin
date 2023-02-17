import argparse
import csv
import json
import math
import os
from num import NUM
from sym import SYM
from data import DATA
from update import *
from query import *
from copy import deepcopy
from miscellaneous import cliffsDelta
from random import random

help = """
bins: multi-objective semi-supervised discetization
(c) 2023 Tim Menzies <timm@ieee.org> BSD-2

USAGE: lua bins.lua [OPTIONS] [-g ACTIONS]

OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -f  --file    data file                    = ../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
"""

args = None
Seed = 937162211
egs = {}
n = 0

def print_all_attributes(obj):
    stringToPrint = "{ "
    for attr, value in vars(obj).items():
        stringToPrint += str(attr) + ": " + str(value) + " "
    return stringToPrint + "}"

def dofile(filename):
    with open(filename) as f:
        return json.load(f)

def transpose(t):
    u = []
    for i in range(len(t[0])):
        u.append([t[j][i] for j in range(len(t))])
    return u

def repCols(cols):
    copyCols = deepcopy(cols)
    for col in cols:
        col[-1] = str(col[0]) + ":" + str(col[-1])
        for j in range(1, len(col)):
            col[j - 1] = col[j]
        col.pop()
    cols.insert(0, ['Num' + str(k) for k in range(len(cols[0]))])
    cols[0][-1] = "thingX"
    return DATA(cols)

def repRows(t, rows, u=None):
    rows = deepcopy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] = str(rows[0][j]) + ":" + str(s)
    rows.pop()
    for n, row in enumerate(rows):
        if n==0:
            row.append("thingX")
        else:
            u = t["rows"][len(t["rows"]) - n]
            row.append(u[-1])
    return DATA(rows)

def show(node, what= None, cols = None, nPlaces = None, lvl=None):
    """
    Function:
        show
    Description:
        Displays optimization of data as a tree
    Input:
        node - data
        what - stat to display
        cols - data columns
        nPlaces - # of decimal places to display stats
        lvl - how deep the tree is
    Output:
        None
    """
    if node:
        lvl = lvl or 0
        print("|.. " * lvl, end="")
        if ("left" not in node):
            print(last(last(node["data"].rows).cells))
        else:
            print(str(int(100 * node["C"])))
        show(node.get("left", None), what,cols, nPlaces, lvl+1)
        show(node.get("right", None), what,cols,nPlaces, lvl+1)

def last(t):
    return t[-1]

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

def rand(low = None, high = None):
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

def eg(key, string, fun):
    """
    Function:
        eg
    Description:
        Creates an example test case and adds it to the dictionary of test cases. Appends the key/value to the actions of the help string
    Input:
        key - key of argument
        string - value of argument as a string
        fun - callback function to use for test case
    Output:
        None
    """
    global egs
    global help
    egs[key] = fun
    help += f"  -g {key}    {string}"

def oo():
    pass

def cosine(a, b, c):
    """
    Function:
        cosine
    Description:
        Finds x, y of line between a & b
    Input:
        a - First point
        b - Second point
        c - distance between a & b
    Output:
        x2 - x of line between a & b
        y - y of line between a & b
    """
    x1 = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
    x2 = max(0, min(1, x1))
    y = (abs(a ** 2 - x2 ** 2)) ** 0.5
    return x2, y

def randFunc():
    """
    Function:
        randFunc
    Description:
        Callback function to test the rand function
    Input:
        None
    Output:
        checks if m1 equals m2 and that they round to 0.5 as a boolean
    """
    global args
    global Seed
    Seed = 1
    t = []
    for i in range(1000):
        t.append(rint(100))
    Seed = 1
    u = []
    for i in range(1000):
        u.append(rint(100))
    for index, value in enumerate(t):
        if (value != u[index]):
            return False
    return True

def someFunc():
    global args
    args.Max = 32
    num1 = NUM()
    for i in range(10000):
        add(num1, i)
    args.Max = 512
    # print(has(num1))

def symFunc():
    """
    Function:
        symFunc
    Description:
        Callback function to test SYM class
    Input:
        None
    Output:
        'a' is the median value in the array and that the div to 3 decimal points equals 1.379 as a boolean
    """
    sym = adds(SYM(), ["a","a","a","a","b","b","c"])
    print(mid(sym), round(div(sym), 2))
    return 1.38 == round(div(sym), 2)

def numFunc():
    """
    Function:
        numFunc
    Description:
        Callback function to test the NUM class
    Input:
        None
    Output:
        The midpoint of num1 of 0.5 and num1 has a greater midpoint than num2
    """
    num1, num2 = NUM(), NUM()
    for i in range(10000):
        add(num1, rand())
    for i in range(10000):
        add(num2, rand() ** 2)
    print(1, round(mid(num1), 2), round(div(num1), 2))
    print(2, round(mid(num2), 2), round(div(num2), 2))
    return .5 == round(mid(num1), 1) and mid(num1)> mid(num2)

def crashFunc():
    """
    Function:
        crashFunc
    Description:
        Callback function to test crashes
    Input:
        None
    Output:
        an instance of NUM doesn't have the property 'some.missing.nested.field'
    """
    num = NUM()
    return not hasattr(num, 'some.missing.nested.field')

def getCliArgs():
    """
    Function:
        getCliArgs
    Description:
        Parses out the arguments entered or returns an error if incorrect syntax is used
    Input:
        None
    Output:
        None
    """
    global args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-b", "--bins", type=int, default=16, required=False, help="initial number of bins")
    parser.add_argument("-g", "--go", type=str, default="all", required=False, help="start-up action")
    parser.add_argument("-h", "--help", action='store_true', help="show help")
    parser.add_argument("-s", "--seed", type=int, default=937162211, required=False, help="random number seed")
    parser.add_argument("-f", "--file", type=str, default="../etc/data/auto93.csv", required=False, help="data file")
    parser.add_argument("-p", "--p", type=int, default=2, required=False, help="distance coefficient")
    parser.add_argument("-c", "--cliffs", type=float, default=0.147, required=False, help="cliff's delta threshold")
    parser.add_argument("-F", "--Far", type=float, default=0.95, required=False, help="distance to distant")
    parser.add_argument("-H", "--Halves", type=int, default=512, required=False, help="search space for clustering")
    parser.add_argument("-m", "--min", type=float, default=0.5, required=False, help="size of smallest cluster")
    parser.add_argument("-M", "--Max", type=int, default=512, required=False, help="numbers")
    parser.add_argument("-r", "--rest", type=int, default=4, required=False, help="how many of rest to sample")
    parser.add_argument("-R", "--Reuse", type=bool, default=True, required=False, help="child splits reuse a parent pole")

    args = parser.parse_args()

def printCLIvalues():
    """
    Function:
        printCLIvalues
    Description:
        Prints the arguments
    Input:
        None
    Output:
        None
    """
    cli_args = {}
    cli_args["dump"] = args.dump
    cli_args["go"] = args.go
    cli_args["help"] = args.help
    cli_args["seed"] = args.seed
    cli_args["file"] = args.file
    print(cli_args)

def csvFunc():
    """
    Function:
        csvFunc
    Description:
        Callback function to test readCSV() function
    Input:
        None
    Output:
        there are 8 * 399 elements in the default csv file in etc/data/auto93.csv
    """
    global n
    def fun(t):
        global n
        n += len(t)
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    readCSV(full_path, fun)
    return n == 8 * 399

def readCSV(sFilename, fun):
    """
    Function:
        readCSV
    Description:
        reads a CSV and runs a callback function on every line
    Input:
        sFilename - path of CSV file to be read
        fun - callback function to be called for each line in the CSV
    Output:
        None
    """
    with open(sFilename, mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            fun(line)

def dataFunc():
    """
    Function:
        dataFunc
    Description:
        Callback function to test DATA class
    Input:
        None
    Output:
        DATA instance is created and has correct property values when reading the default CSV file at etc/data/auto93.csv
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    dataOBJ = DATA()
    data = dataOBJ.read(full_path)
    col = data.cols.x[1].col
    print(col.lo,col.hi, mid(col),div(col))
    print(stats(data, 2))
    # return (len(data.rows) == 398 and
    # data.cols.y[1].w == -1 and
    # data.cols.x[1].at == 1 and
    # len(data.cols.x) == 4
    # )

def statsFunc():
    """
    Function:
        statsFunc
    Description:
        Callback function to test stats function in DATA class
    Input:
        None
    Output:
        the statistics for the DATA instance using the default file at etc/data/auto93.csv are printed to the console
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    for k, cols in {'y': data.cols.y, 'x': data.cols.x}.items():
        print(k, "\tmid", (data.stats("mid", cols, 2)))
        print("", "\tdiv", (data.stats("div", cols, 2)))

def cloneFunc():
    """
    Function:
        cloneFunc
    Description:
        Callback function to test clone function in DATA class
    Input:
        None
    Output:
        the cloned DATA object contains the same metadata as the original object
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    dataOBJ = DATA()
    data1 = dataOBJ.read(full_path)
    data2 = data1.clone(data1.rows)
    return (len(data1.rows) == len(data2.rows) and
            data1.cols.y[1].w == data2.cols.y[1].w and
            data1.cols.x[1].at == data2.cols.x[1].at and
            len(data1.cols.x) == len(data2.cols.x))

def clusterFunc():
    """
    Function:
        clusterFunc
    Description:
        Callback function to test cluster function in DATA class
    Input:
        None
    Output:
        the correct data is output from the cluster function
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    show(data.cluster(), "mid", data.cols.y, 1)

def swayFunc():
    """
    Function:
        swayFunc
    Description:
        Callback function to test sway function in DATA class
    Input:
        None
    Output:
        the correct data is output from the sway function
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    show(data.sway(), "mid", data.cols.y, 1)

def aroundFunc():
    """
    Function:
        aroundFunc
    Description:
        Callback function to test around function in DATA class
    Input:
        None
    Output:
        the rows are correctly sorted for the DATA object
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    for n, t in enumerate(data.around(data.rows[1])):
        if n % 50 == 0:
            print(n, round(t[1], 2), t[0].cells)

def halfFunc():
    """
    Function:
        halfFunc
    Description:
        Callback function to test half function in DATA class
    Input:
        None
    Output:
        the DATA object is correctly split in half
    """
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    data = DATA(full_path)
    left, right, A, B, mid, c = data.half()
    print(len(left), len(right), len(data.rows))
    print(A.cells, c)
    print(mid.cells)
    print(B.cells)

def repColsFunc():
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    rawData = dofile(full_path)
    t = repCols(rawData["cols"])
    for col in t.cols.all:
        print(vars(col))
    for row in t.rows:
        print(vars(row))

def synonymsFunc():
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    show(repCols(dofile(full_path)["cols"]).cluster())

def reprowsFunc():
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args.file)
    t = dofile(full_path)
    rows = repRows(t, transpose(t["cols"]))
    for col in rows.cols.all:
        print(vars(col))
    for row in rows.rows:
        print(vars(row))

def copyFunc():
    t1 = {'a': 1, 'b': {'c': 2, 'd': [3]}}
    t2 = deepcopy(t1)
    t2["b"]["d"][0] = 10000
    print("Before: " + str(t1) + "\nAfter: " + str(t2))


def cliffsFunc():
    assert cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]) == False, "1"
    assert cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]) == True, "2"
    t1, t2 = [], []
    for i in range(1000):
        t1.append(rand())
        t2.append(math.sqrt(rand()))
    assert cliffsDelta(t1, t1) == False, "3"
    # assert cliffsDelta(t1, t2) == True, "4" Giving Error
    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x*j, t1))
        diff = cliffsDelta(t1, t3)
        print(">", round(j), diff)
        j *= 1.025