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
    gridBorder = None
    startX = None
    startY = None


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red, "^": Ansi.green, "O": Ansi.yellow}
# from matrix3d import *


def initData():
    data.grid = copy.deepcopy(data.gridLst[0])
    extendGrid(data.grid, eltEmpty="/")
    data.gridBorder = 1

    # get start pos
    for y in range(len(data.grid)):
        for x in range(len(data.grid[y])):
            if data.grid[y][x] == "^":
                data.startX = x
                data.startY = y
                return


##################
### PROCEDURES ###
##################


def follow_path(grid, gridBorder, startY, startX):
    posCount = 1  # count start pos
    direction = OFFSET.N
    x = startX
    y = startY
    gridExitDirection = [
        [[] for i in range(len(grid) + 2 * gridBorder)]
        for j in range(len(grid[0]) + 2 * gridBorder)
    ]
    while (
        x >= gridBorder
        and x < len(grid[0]) - gridBorder
        and y >= gridBorder
        and y < len(grid) - gridBorder
    ):
        if grid[y][x] == ".":
            posCount += 1
            grid[y][x] = "X"

        # check infinite loop
        if direction in gridExitDirection[y][x]:  # infinite loop detected!
            # print(f"infinite loop detected in ({y},{x})")
            return -1
        gridExitDirection[y][x].append(direction)

        while (grid[y + direction.y][x + direction.x]) in (
            "#",
            "O",
        ):
            direction = OFFSET.ROTATE_RIGHT[direction]
        x = x + direction.x
        y = y + direction.y
    grid[y][x] = "@"

    return posCount  # number of pos (including start) or -1 if infinite loop


def resolve_bothpart():
    grid = copy.deepcopy(data.grid)
    # showGrid(grid1, MATRIX2D_COLORSET)

    posCount = follow_path(grid, data.gridBorder, data.startY, data.startX)
    # showGrid(grid, MATRIX2D_COLORSET)

    posLst = []
    for y in range(data.gridBorder, len(grid) - data.gridBorder):
        for x in range(data.gridBorder, len(grid[y]) - data.gridBorder):
            if grid[y][x] == "X":
                posLst.append((y, x))

    # test all blocking pos
    blockCount = 0
    for blockY, blockX in posLst:
        grid = copy.deepcopy(data.grid)
        grid[blockY][blockX] = "O"
        res = follow_path(grid, data.gridBorder, data.startY, data.startX)
        if res == -1:
            blockCount += 1

    return posCount, blockCount


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"
# inputFile = "Day06.txt"

# data.rawInput = readInputFile(inputFile)
data.gridLst = loadMatrix2d(inputFile)


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

# exit()

### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
