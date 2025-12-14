import copy
import math
import time
from collections import defaultdict

from tools import *

# import re

# from collections import deque

# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

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

    for line in data.rawInput:
        data.lineFields.append([int(elt) for elt in line])

    print("lineFields:", data.lineFields)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def getJoltage(bank, batCount):
    print("->", bank, batCount)
    batJoltage = ""
    curIndex = 0
    for i in range(batCount):
        if batCount - i - 1 > 0:
            tmpBank = bank[curIndex : -(batCount - i - 1)]
        else:
            tmpBank = bank[curIndex:]
        # print(f"  [{i:02}] {curIndex} {tmpBank}")
        tmpIndex = max(range(len(tmpBank)), key=tmpBank.__getitem__)
        # print(f"       {tmpIndex}, {tmpBank[tmpIndex]}")
        batJoltage = batJoltage + str(tmpBank[tmpIndex])
        curIndex += tmpIndex + 1

    print(f"{batJoltage}")
    return int(batJoltage)


def resolve_bothpart():
    joltage1 = 0
    joltage2 = 0
    for bank in data.lineFields:
        joltage1 += getJoltage(bank, 2)
        joltage2 += getJoltage(bank, 12)

    return joltage1, joltage2


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
