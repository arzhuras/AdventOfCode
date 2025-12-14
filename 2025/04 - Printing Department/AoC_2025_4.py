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

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red, "@": Ansi.green}
# from matrix3d import *
# from graph import *


def initData():
    data.lineFields = []

    data.grid = []
    data.grid = loadMatrix2d(inputFile)[0]
    # showGrid(data.grid)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def accessibleRolls(grid):
    rollCount = 0
    newGrid = copy.deepcopy(grid)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != "@":
                continue
            #print(f"({y},{x})={grid[y][x]}")
            neighbourRollCount = 0
            for neighbour in OFFSET.AROUND:
                nx = x + neighbour.x
                ny = y + neighbour.y
                if nx >= 0 and nx < len(grid[0]) and ny >= 0 and ny < len(grid):
                    if grid[ny][nx] == "@":
                        neighbourRollCount += 1
            if neighbourRollCount < 4:
                rollCount += 1
                newGrid[y][x] = "X"
    return rollCount, newGrid


def resolve_bothpart():
    grid = data.grid
    showGrid(grid, colorset=MATRIX2D_COLORSET, span=2)

    rollCount, rollCount2 = 0, 0
    tmpRollCount, newGrid = accessibleRolls(grid)
    showGrid(newGrid, colorset=MATRIX2D_COLORSET, span=2)
    rollCount = tmpRollCount
    while tmpRollCount > 0:
        tmpRollCount, newGrid = accessibleRolls(grid)
        showGrid(newGrid, colorset=MATRIX2D_COLORSET, span=2)
        rollCount2 += tmpRollCount
        grid = newGrid

    return rollCount, rollCount2


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
