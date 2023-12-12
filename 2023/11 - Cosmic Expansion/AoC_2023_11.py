import time
import math
import copy

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# from functools import reduce
# import itertools

###  /modules libraries ###
from tools import *
from matrix2d import *
# from matrix3d import *


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    fields = None

    grid = None


data = Data()


def initData():
    data.fields = []
    data.grid = []

    data.grid = loadMatrix2d(inputFile)[0]


##################
### PROCEDURES ###
##################


def resolve(expansionRate = 2):
    grid = data.grid

    galaxiesCoord = []
    rows = set()
    cols = set()

    # parcours l'univers pour trouver les galaxies
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '#':
                galaxiesCoord.append([y,x])
                rows.add(y)
                cols.add(x)
    rows = list(rows)
    cols = list(cols)
    #print("galaxiesCoord", galaxiesCoord)
    #print("rows", rows)
    #print("cols", cols)

    # cosmic expansion on both row and col!
    for groupId, group in (0, rows), (1, cols):
        for eltIdx in range(1, len(group)):
            delta = group[eltIdx] - group[eltIdx-1] - 1
            #print(group[eltIdx], group[eltIdx-1], delta)
            if delta > 0:
                for galaxy in galaxiesCoord:
                    if galaxy[groupId] >= group[eltIdx]:
                        galaxy[groupId] += delta * expansionRate - delta
                for i in range(eltIdx, len(group)):
                    group[i] += delta * expansionRate - delta
    #print()
    #print("galaxiesCoord", galaxiesCoord)
    #print("rows", rows)
    #print("cols", cols)

    # comput shortest path
    sumPath = 0
    print(galaxiesCoord)
    for srcId in range(len(galaxiesCoord)):
        for dstId in range(srcId+1, len(galaxiesCoord)):
            pathLen = abs(galaxiesCoord[srcId][0] - galaxiesCoord[dstId][0]) + abs(galaxiesCoord[srcId][1] - galaxiesCoord[dstId][1])
            sumPath += pathLen
            #print(srcId, galaxiesCoord[srcId], dstId, galaxiesCoord[dstId], pathLen, sumPath)

    return sumPath


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

EXPANSION_RATE = 2
EXPANSION_RATE = 10
#EXPANSION_RATE = 100
EXPANSION_RATE = 1000000

data.rawInput = readInputFile(inputFile)

initData()
showGrid(data.grid)

res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

res = resolve(EXPANSION_RATE)
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
