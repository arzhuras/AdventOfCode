import copy
import math
import time
from collections import defaultdict
import locale

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
    freshRange = None
    ingedients = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *
# from graph import *
from range import *


def initData():
    data.freshRange = []
    data.ingredients = []
    # data.rules = defaultdict(lambda: set())
    # data.line = "".join(data.rawInput)

    i = 0
    line = data.rawInput[i]
    while line.strip() != "":
        i += 1
        min, max = map(int, line.split("-"))
        data.freshRange.append((min, max, max - min + 1))  # min, max, span
        line = data.rawInput[i]

    # data.freshRange.sort(key=lambda x: x[0])
    # print("freshRange:", data.freshRange)

    """ print("freshRange:")
    locale.setlocale(locale.LC_NUMERIC, "fr_FR.UTF-8")
    for min, max, span in data.freshRange:
        print(f"  [{min:n}, {max:n}] = {span:n}")
    """
    i += 1
    while i < len(data.rawInput):
        data.ingredients.append(int(data.rawInput[i].strip()))
        i += 1
    # print("ingredients:", data.ingredients)


##################
### PROCEDURES ###
##################


def resolve_part1():
    freshCount = 0
    for ingredient in data.ingredients:
        found = False
        for min, max, span in data.freshRange:
            if min <= ingredient <= max:
                found = True
                break
        if found:
            freshCount += 1

    return freshCount


def resolve_part2():

    freshCount = 0
    fresh = data.freshRange

    i = 0
    while i < len(fresh):
        range1 = fresh[i]
        if range1 is None:
            i += 1
            continue
        j = i + 1
        while j < len(fresh):
            range2 = fresh[j]
            if range2 is None:
                j += 1
                continue
            overlap, before, after = getOverlapRange(range1, range2)
            if overlap is not None:
                # showGetOverlap(range1, range2, overlap, before, after)
                # checkOverlap(range1, range2, overlap, before, after)
                fresh[i] = None
                fresh[j] = None
                if before is not None:
                    fresh.append(before)
                fresh.append(overlap)
                if after is not None:
                    fresh.append(after)
                break
            j += 1
        i += 1

    # print("fresh final:", fresh)
    print("fresh final sorted:")
    fresh.sort(key=lambda x: x[0] if x is not None else math.inf)
    prevRMax = 0
    for range in fresh:
        if range != None:
            # print(f"[{range[0]}, {range[1]}] = {range[2]}")
            if range[0] <= prevRMax:
                print("ERREUR DE RECALCUL DES RANGES")
            prevRMax = range[1]
            freshCount += range[2]

    return f"{freshCount}"


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"

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
res1 = resolve_part1()
# res1, res2 = resolve_bothpart()
endTime = time.time()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)
# initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
