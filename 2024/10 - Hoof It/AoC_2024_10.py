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
# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    fields = None
    line = None
    gridLst = None
    grid = None


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"0": Ansi.red, "9": Ansi.blue}
# from matrix3d import *


def initData():
    return


##################
### PROCEDURES ###
##################

NEXT = {
    "0": "1",
    "1": "2",
    "2": "3",
    "3": "4",
    "4": "5",
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
}


def findTrail(grid, y, x, depth=0):
    tab = " " * depth
    if depth > 9:
        exit()

    # print(f"{tab}{depth} ({y},{x})")
    if grid[y][x] == "9":
        # print("GOTCHA", y, x)
        return [(y, x)]

    next = NEXT[grid[y][x]]
    # summitLst = set()
    summitLst = []
    for offset in OFFSET.CROSS:
        nextY = y + offset.y
        nextX = x + offset.x
        if nextY < 0 or nextY > len(grid) - 1 or nextX < 0 or nextX > len(grid[0]) - 1:
            continue
        # print(offset)
        if grid[nextY][nextX] == next:
            res = findTrail(grid, nextY, nextX, depth + 1)
            # print(tab, depth, "res:", res, offset.label)
            if len(res) > 0:
                summitLst = summitLst + res
            # print(tab, depth, "summitLst:", summitLst)
    return summitLst


def resolve_bothpart():
    grid = data.grid[0]
    # showGrid(grid, MATRIX2D_COLORSET)

    trailLst = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "0":
                res = findTrail(grid, y, x)
                if len(res) > 0:
                    trailLst.append([(y, x), res])

    sum1 = 0
    for elt in trailLst:
        sum1 += len(set(elt[1]))
        # print(elt[0], len(set(elt[1])), elt[1])

    sum2 = 0
    for elt in trailLst:
        sum2 += len(elt[1])
        # print(elt[0], len(elt[1]), elt[1])

    return sum1, sum2


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
# inputFile = "sample2.txt"
# inputFile = "sample3.txt"
# inputFile = "sample4.txt"
inputFile = "sample5.txt"  # target sample
# inputFile = "sample6.txt"
# inputFile = "sample7.txt"
# inputFile = "sample8.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

# data.rawInput = readInputFile(inputFile)
data.grid = loadMatrix2d(inputFile)


### PART 1 ###
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
# res1 = resolve_part1()
res1, res2 = resolve_bothpart()
endTime = time.time()

print()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
