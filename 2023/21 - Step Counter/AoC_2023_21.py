# from matrix2d import *
import matrix2d
from tools import *
import time
import math
import copy

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

    grid = None
    start = None


data = Data()

###  /modules libraries ###
matrix2d.MATRIX2D_COLORSET = {"O": Ansi.red}
# from matrix3d import *


def initData():
    data.grid = []
    data.grid = matrix2d.loadMatrix2d(inputFile)[0]
    matrix2d.showGrid(data.grid)

    # data.grids = []
    # data.grids = loadMatrix2d(inputFile)

    for y in range(len(data.grid)):
        for x in range(len(data.grid[0])):
            if data.grid[y][x] == "S":
                data.start = (y, x)
                return


##################
### PROCEDURES ###
##################


def resolve_part1(maxSteps):
    grid = data.grid

    print(data.start)

    plots = [data.start]
    grid[data.start[0]][data.start[1]] = "."
    for steps in range(maxSteps):
        tmpPlots = []
        for plotY, plotX in plots:
            grid[plotY][plotX] = "."
        for plotY, plotX in plots:
            # print(plotY, plotX)
            for offsetY, offsetX, offsetDir in matrix2d.OFFSET.CROSS:
                y = plotY + offsetY
                x = plotX + offsetX
                if not isValidGridCoord(grid, y, x):
                    continue
                if grid[y][x] != "#" and grid[y][x] != "O":
                    grid[y][x] = "O"
                    tmpPlots.append((y, x))
                    # print(tmpPlots)
        plots = tmpPlots
        grid[data.start[0]][data.start[1]] = "S"
        print(steps + 1, "->", len(plots))
        # showGrid(grid)
    matrix2d.showGrid(grid)

    return len(plots)


def isValidGridCoord(grid, y, x, maxY=-1, maxX=-1):
    if (y < 0 or x < 0):
        return False

    if maxY == -1:
        maxY = len(grid)

    if maxX == -1:
        maxX = len(grid[0])

    if (y >= maxY or x >= maxX):
        return False

    return True


def resolve_part2(maxSteps):
    grid = data.grid

    for y in range(len(grid)):
        tmpGrid = copy.deepcopy(grid[y])
        for _ in range(4):
            grid[y] = grid[y] + tmpGrid

    maxY = len(grid)
    for _ in range(4):
        for y in range(maxY):
            grid.append(copy.deepcopy(grid[y]))
    data.start = (16, 16)
    # showGrid(grid)

    print(data.start)

    plots = [data.start]
    grid[data.start[0]][data.start[1]] = "."
    for steps in range(maxSteps):
        tmpPlots = []
        for plotY, plotX in plots:
            grid[plotY][plotX] = "."
        for plotY, plotX in plots:
            # print(plotY, plotX)
            for offsetY, offsetX, offsetDir in matrix2d.OFFSET.CROSS:
                y = plotY + offsetY
                x = plotX + offsetX
                if not isValidGridCoord(grid, y, x):
                    continue
                if grid[y][x] != "#" and grid[y][x] != "O":
                    grid[y][x] = "O"
                    tmpPlots.append((y, x))
                    # print(tmpPlots)
        plots = tmpPlots
        grid[data.start[0]][data.start[1]] = "S"
        print(Ansi.blue, steps + 1, "->", len(plots), Ansi.norm)
        matrix2d.showGrid(grid)

    return len(plots)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
maxSteps = 50

# MAX_ROUND = 1000
# inputFile = "input.txt"
# maxSteps = 64

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1(6)
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2(maxSteps)
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
