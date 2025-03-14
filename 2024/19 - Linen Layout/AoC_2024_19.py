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
    patterns = None
    design = None
    patternsCombination = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():

    data.patterns = data.rawInput[0].replace(" ", "").split(",")
    data.design = []
    for line in data.rawInput[2:]:
        data.design.append(line)

    # print("patterns:", data.patterns)
    # print("design:", data.design)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def checkMatchWithArrangement(design, arrangement=[], curPos=0, depth=0):
    tab = "  " * depth
    res = []
    for elt in data.patterns:
        # print(design[curPos : curPos + len(elt)], elt)
        if design[curPos : curPos + len(elt)] == elt:
            # print(f"{tab}{Ansi.yellow}{elt}  MATCH{Ansi.norm}")
            if curPos + len(elt) >= len(design):
                # print(f"{tab}ARR: {arrangement + [elt]}")
                return res + [arrangement + [elt]]
            tmpRes = checkMatch(
                design, arrangement + [elt], curPos + len(elt), depth + 1
            )
            if len(tmpRes) > 0:
                res = res + tmpRes
                # print(f"{tab}RES: {tmpRes}")
        # print(f"{tab}{Ansi.grey}{elt}  NO MATCH: {elt} <-> {design[curPos : curPos + len(elt)]}{Ansi.norm}")
    # print(f"{tab}{Ansi.red}IMPOSSIBLE{Ansi.norm}")
    # print(f"{tab}{Ansi.yellow}RES2: {tmpRes}{Ansi.norm}")
    return res


def checkMatch(design):
    res = 0
    for elt in data.patterns:
        if design[: len(elt)] == elt:
            if len(design) == len(elt):
                return res + 1
            tmpRes = checkMatch(design[len(elt) :])
            if tmpRes > 0:
                res = res + tmpRes
    return res


def resolve_bothpart():

    possibleDesign1 = 0
    possibleDesign2 = 0
    for design in data.design:
        print(f"{Ansi.blue}{design:10}{Ansi.norm}", end="")
        res = checkMatch(design)
        if res > 0:
            print(f"{Ansi.green} FULL MATCH{Ansi.norm} ", end="")
            possibleDesign1 += 1
        else:
            print(f"{Ansi.red} IMPOSSIBLE{Ansi.norm} ", end="")
        possibleDesign2 += res
        print(res)

    return possibleDesign1, possibleDesign2


def checkMatch2(design):
    res = 0
    for elt in data.patterns:
        if design[: len(elt)] == elt:
            if len(design) == len(elt):
                return res + 1
            tmpRes = checkMatch(design[len(elt) :])
            if tmpRes > 0:
                res = res + tmpRes
    return res


def resolve_bothpart2():
    # compute sub combination for the different patterns

    possibleDesign1 = 0
    possibleDesign2 = 0
    for design in data.design:
        print(f"{Ansi.blue}{design:10}{Ansi.norm}", end="")
        res = checkMatch(design)
        if res > 0:
            print(f"{Ansi.green} FULL MATCH{Ansi.norm} ", end="")
            possibleDesign1 += 1
        else:
            print(f"{Ansi.red} IMPOSSIBLE{Ansi.norm} ", end="")
        possibleDesign2 += res
        print(res)

    return possibleDesign1, possibleDesign2


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
# inputFile = "sample2.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.gridLst = loadMatrix2d(inputFile)


### PART 1 ###
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)
initData()
startTime = time.time()
# res1 = resolve_part1()
res1, res2 = resolve_bothpart2()
endTime = time.time()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)
initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
