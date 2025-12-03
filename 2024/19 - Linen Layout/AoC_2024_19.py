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
    patternsExtended = None


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

    # tri par longueur et alpha
    data.patterns.sort()
    data.patterns.sort(key=lambda item: len(item), reverse=True)
    print("patterns:", data.patterns)
    tmpSet = set()
    for pattern in data.patterns:
        if len(pattern) == 1:
            break
        suff = pattern[len(pattern) - 1]
        for pattern2 in data.patterns:
            if len(pattern2) == 1:
                break
            if pattern2 == pattern:
                continue
            pref = pattern2[0]
            if pref == suff:
                # print(pattern, pattern2)
                tmpSet.add(pattern + pattern2[1:])
    data.patternsExtended = data.patterns.copy() + list(tmpSet)
    data.patternsExtended.sort()
    data.patternsExtended.sort(key=lambda item: len(item), reverse=True)
    # print("patternsExtended:", data.patternsExtended)

    # print("patterns sorted:", data.patterns)
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
                res = res + [arrangement + [elt]]
            tmpRes = checkMatchWithArrangement(
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
                res = res + 1
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


def checkMatchOptim(design):
    res = 0
    for elt in data.patterns:
        if design[: len(elt)] == elt:
            if len(design) == len(elt):
                res = res + 1
            tmpRes = checkMatch(design[len(elt) :])
            if tmpRes > 0:
                res = res + tmpRes
    return res


def resolve_bothpart2():
    # compute sub combination for the different patterns
    combination = {}
    # print(len(data.patterns))
    # print(len(data.patternsExtended))
    for pattern in data.patterns:
        combination[pattern] = checkMatch(pattern)
        # print(pattern, combination[pattern])
    # exit()
    # print(combination)
    # data.patterns = data.patternsExtended

    possibleDesign1 = 0
    possibleDesign2 = 0
    for design in data.design[:]:
        print(f"{Ansi.blue}{design:10}{Ansi.norm}", end="")
        arrangement = []
        # res = checkMatchWithArrangement(design)
        while len(design) > 0:
            matchFlag = False
            """
            for pattern in data.patternsExtended:
                # print(pattern)
                if design[: len(pattern)] == pattern:
                    design = design[len(pattern) :]
                    arrangement.append(combination[pattern])
                    matchFlag = True
                    break
            if matchFlag == False:
                break
            """
            for span in range(len(data.patternsExtended[0]), 0, -1):
                if design[:span] in combination:
                    # print("bingo", span, design[:span])
                    arrangement.append(combination[design[:span]])
                    design = design[span:]
                    matchFlag = True
                    break
            if matchFlag == False:
                break

        if matchFlag == True:
            print(f"{Ansi.green} FULL MATCH{Ansi.norm} ", end="")
            possibleDesign1 += 1
            possibleDesign2 += math.prod(arrangement)
        else:
            print(f"{Ansi.red} IMPOSSIBLE{Ansi.norm} ", end="")
        print(math.prod(arrangement), arrangement, end="")
        # print(res)
        print()

    return possibleDesign1, possibleDesign2


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"

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
