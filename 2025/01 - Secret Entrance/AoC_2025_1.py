import copy
import math
import time
from collections import defaultdict

from tools import *

# import re

# from collections import deque

import operator

opFunc = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

# from functools import reduce
# from functools import cache

# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None
    lineFields = None
    gridLst = None
    grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *
# from graph import *


def initData():
    data.lineFields = []

    opFuncDic = {
        "R": operator.add,
        "L": operator.sub,
    }
    for line in data.rawInput:
        data.lineFields.append((line[0], int(line[1:]), opFuncDic[line[0]]))


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def resolve_bothpart():
    code = 50
    zeroCount, zeroCount2 = 0, 0
    for rot, offset, opFunc in data.lineFields:
        if offset > 99:
            print(f"{code:02}", end="")
        tmpCode = opFunc(code, offset)
        if code != 0 and (tmpCode > 100 or tmpCode < 0):
            zeroCount2 == zeroCount2 + (code + offset % 100)
        code = tmpCode % 100
        if code == 0:
            zeroCount += 1
        if offset > 99:
            print(
                f" {rot} {offset:03} {code:02} -> {zeroCount}, {tmpCode:03} -> {zeroCount2} / {code + offset % 100}",
            )

    return zeroCount, zeroCount + zeroCount2


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.gridLst = loadMatrix2d(inputFile)


### PART 1 ###
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)
initData()
startTime = time.time()
# res1 = resolve_part1()
res1, res2 = resolve_bothpart()
endTime = time.time()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")

### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)
# initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
