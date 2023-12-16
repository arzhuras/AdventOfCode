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

    # grid = None


data = Data()


def initData():
    data.fields = []
    data.grid = []
    # data.grids = []

    data.grid = loadMatrix2d(inputFile)[0]
    # data.grids = loadMatrix2d(inputFile)
    # showGrid(data.grid)

##################
### PROCEDURES ###
##################


def followPath(grid: list, visited: dict, cell: tuple, direction: tuple, level=0) -> int:
    tab = "  " * level
    # print(tab, level, "followPath", cell, direction, visited)
    if level == 1000:
        print("INFINITE")
        exit()

    maxY = len(grid)
    maxX = len(grid[0])
    y = cell[0]
    x = cell[1]
    while y >= 0 and y < maxY and x >= 0 and x < maxX and ((y, x) not in visited or direction[2] not in visited[(y, x)]):
        # print(tab, "  @", y, x, grid[y][x])
        if (y, x) not in visited:
            visited[(y, x)] = [direction[2]]
        else:
            visited[(y, x)].append(direction[2])
        match grid[y][x]:
            case  "-":
                # print(tab, "  -", y, x, direction)
                if direction == OFFSET.N or direction == OFFSET.S:
                    followPath(
                        grid, visited, (y+OFFSET.W[0], x+OFFSET.W[1]), OFFSET.W, level + 1)
                    followPath(
                        grid, visited, (y+OFFSET.E[0], x+OFFSET.E[1]), OFFSET.E, level + 1)
                    break
            case  "|":
                # print(tab, "  |", y, x, direction)
                if direction == OFFSET.W or direction == OFFSET.E:
                    followPath(
                        grid, visited, (y+OFFSET.N[0], x+OFFSET.N[1]), OFFSET.N, level + 1)
                    followPath(
                        grid, visited, (y+OFFSET.S[0], x+OFFSET.S[1]), OFFSET.S, level + 1)
                    break
            case  "/":
                # print(tab, "  /", y, x, direction)
                match direction:
                    case OFFSET.E:
                        direction = OFFSET.N
                    case OFFSET.S:
                        direction = OFFSET.W
                    case OFFSET.N:
                        direction = OFFSET.E
                    case OFFSET.W:
                        direction = OFFSET.S
            case  "\\":
                # print(tab, "  \\", y, x, direction)
                match direction:
                    case OFFSET.E:
                        direction = OFFSET.S
                    case OFFSET.S:
                        direction = OFFSET.E
                    case OFFSET.N:
                        direction = OFFSET.W
                    case OFFSET.W:
                        direction = OFFSET.N
        y += direction[0]
        x += direction[1]

    return len(visited)


def resolve_part1():

    grid = data.grid

    visitedCnt = followPath(grid, {}, (0, 0), OFFSET.E)
    # showGrid(grid)
    # print()

    return visitedCnt


def resolve_part2():
    grid = data.grid

    visitedCnt = []

    for y, direction in [(0, OFFSET.S), (len(grid) - 1, OFFSET.N)]:
        for x in range(len(grid[0])):
            visitedCnt.append(followPath(
                grid, {}, (y, x), direction))
            # print(Ansi.blue, direction[2], y, x, visitedCnt[-1], Ansi.norm)

    for x, direction in [(0, OFFSET.E), (len(grid[y]) - 1, OFFSET.W)]:
        for y in range(len(grid)):
            visitedCnt.append(followPath(
                grid, {}, (y, x), direction))
            # print(Ansi.blue, direction[2], y, x, visitedCnt[-1], Ansi.norm)

    # print(visitedCnt)
    return max(visitedCnt)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1()
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
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
