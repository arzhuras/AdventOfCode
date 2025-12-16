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


# arg range1: (start , end, span) range2: (start , end, span), pas forcément dans l'ordre
# return: range overlap, range before, range after
# return None if range is empty
def getOverlapRange(range1: tuple, range2: tuple) -> tuple:

    if range1[0] < range2[0] and range1[1] < range2[0]:
        return None, range1, range2  # disjoint
    if range2[0] < range1[0] and range2[1] < range1[0]:
        return None, range2, range1  # disjoint inversé

    rmin = max(range1[0], range2[0])
    rmax = min(range1[1], range2[1])
    rangeOverlap = (rmin, rmax, rmax - rmin + 1)

    rangeBefore = None
    if range1[0] != range2[0]:
        rmin = min(range1[0], range2[0])
        rmax = rangeOverlap[0] - 1
        rangeBefore = (rmin, rmax, rmax - rmin + 1)

    rangeAfter = None
    if range1[1] != range2[1]:
        rmin = rangeOverlap[1] + 1
        rmax = max(range1[1], range2[1])
        rangeAfter = (rmin, rmax, rmax - rmin + 1)

    return rangeOverlap, rangeBefore, rangeAfter

    """
    # test_overlap()
    for elt1, elt2 in (
        [(1, 3), (2, 4)],  # A cheval
        [(2, 4), (1, 3)],
        [(1, 3), (3, 5)],  # Bord à bord
        [(3, 5), (1, 3)],
        [(1, 5), (2, 4)],  # Milieux
        [(2, 4), (1, 5)],
        [(1, 3), (1, 5)],  # Limite gauche
        [(1, 5), (1, 3)],
        [(3, 5), (1, 5)],  # Limite droite
        [(1, 5), (3, 5)],
        [(1, 5), (1, 5)],  # Identique
        [(1, 2), (3, 4)],  # Disjoint
        [(3, 4), (1, 2)],
    ):
        print(elt1, elt2, getOverlapRange(elt1, elt2))
    """


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
                # showGetOverlap(i, range1, j, range2, overlap, before, after)
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


def checkOverlap(range1, range2, overlap, before, after):
    if (
        (overlap[2] if overlap is not None else 0) * 2
        + (before[2] if before is not None else 0)
        + (after[2] if after is not None else 0)
    ) != (range1[2] + range2[2]):
        print(
            "bef",
            before,
            "over",
            overlap,
            "aft",
            after,
            (overlap[2] if overlap is not None else 0) * 2
            + (before[2] if before is not None else 0)
            + (after[2] if after is not None else 0),
        )
        print(range1, range2, range1[2] + range2[2])
        print("ERREUR DE CALCUL DES SPANS")
        exit()


def showGetOverlap(i, range1, j, range2, overlap, before, after):
    print(
        f"{i} {j} [{range1[0]}, {range1[1]}] = {range1[2]} / [{range2[0]}, {range2[1]}] = {range2[2]} -> ",
        end="",
    )
    if before is not None:
        print(f"[{before[0]}, {before[1]}] = {before[2]}, ", end="")
    else:
        print("NONE, ", end="")
    if overlap is not None:
        print(f"[{overlap[0]}, {overlap[1]}] = {overlap[2]}, ", end="")
    else:
        print("NONE, ", end="")
    if after is not None:
        print(f"[{after[0]}, {after[1]}] = {after[2]}")
    else:
        print("NONE")


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
