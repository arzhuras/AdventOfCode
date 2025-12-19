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
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red, "^": Ansi.red, "|": Ansi.yellow}
# from matrix3d import *
# from graph import *


def initData():
    data.grid = []
    data.grid = loadMatrix2d(inputFile)[0]
    showGrid(data.grid, MATRIX2D_COLORSET)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def resolve_bothpart():
    grid = copy.deepcopy(data.grid)
    showGrid(grid, MATRIX2D_COLORSET, span=1)

    # recherche de la colonne de départ
    for x, elt in enumerate(grid[0]):
        if elt == "S":
            break
    print("Start x:", x)
    beamLst = [x]
    splitDic = {} # dictionnaire des splits réellement atteind

    for y in range(1, len(grid)):
        tmpBeamLst = []
        for x in beamLst:
            if grid[y][x] == ".":
                tmpBeamLst.append(x)
                grid[y][x] = "|"
            elif grid[y][x] == "^":
                nextNodes = [None, None]
                for idx, col in enumerate((x - 1, x + 1)):
                    tmpBeamLst.append(col)
                    grid[y][col] = "|"
                    for i in range(y + 1, len(grid)):
                        if grid[i][col] == "^":
                            nextNodes[idx] = (i, col)
                            break
                splitDic[(y, x)] = [nextNodes[0], nextNodes[1], 0] # next node left, next node right, somme des 2 noeuds
        beamLst = tmpBeamLst

    for value in reversed(list(splitDic.values())):
        for elt in value[0:2]:
            if elt is not None:
                value[2] += splitDic[elt][2]
            else:
                value[2] += 1

    showGrid(grid, MATRIX2D_COLORSET, span=1)

    return len(splitDic), splitDic[next(iter(splitDic))][2]


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
