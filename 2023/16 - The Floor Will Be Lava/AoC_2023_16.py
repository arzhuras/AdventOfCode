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
    showGrid(data.grid)

##################
### PROCEDURES ###
##################


def followPath(grid, visited, cell, direction, level=0):
    tab = "  " * level
    # print(tab, level, "followPath", cell, direction)
    if level == 1000:
        print("INFINITE")
        exit()
    maxY = len(grid)
    maxX = len(grid[0])
    y = cell[0]
    x = cell[1]
    while y >= 0 and y < maxY and x >= 0 and x < maxX and (y, x, direction[2]) not in visited:
        # print(tab, "  @", y, x, grid[y][x], visited)
        match grid[y][x]:
            case  ".":
                # print(tab, "  .", y, x, direction)
                grid[y][x] = "#"
                visited.append((y, x, direction[2]))
                y += direction[0]
                x += direction[1]
            case  "#":
                # print(tab, "  #", y, x, direction)
                visited.append((y, x, direction[2]))
                y += direction[0]
                x += direction[1]
            case  "-":
                # print(tab, "  -", y, x, direction)
                visited.append((y, x, direction[2]))
                if direction == OFFSET.E or direction == OFFSET.W:
                    y += direction[0]
                    x += direction[1]
                else:
                    followPath(
                        grid, visited, (y+OFFSET.W[0], x+OFFSET.W[1]), OFFSET.W, level + 1)
                    followPath(
                        grid, visited, (y+OFFSET.E[0], x+OFFSET.E[1]), OFFSET.E, level + 1)
                    break
            case  "|":
                # print(tab, "  |", y, x, direction)
                visited.append((y, x, direction[2]))
                if direction == OFFSET.N or direction == OFFSET.S:
                    y += direction[0]
                    x += direction[1]
                else:
                    followPath(
                        grid, visited, (y+OFFSET.N[0], x+OFFSET.N[1]), OFFSET.N, level + 1)
                    followPath(
                        grid, visited, (y+OFFSET.S[0], x+OFFSET.S[1]), OFFSET.S, level + 1)
                    break
            case  "/":
                # print(tab, "  /", y, x, direction)
                visited.append((y, x, direction[2]))
                match direction:
                    case OFFSET.E:
                        direction = OFFSET.N
                    case OFFSET.S:
                        direction = OFFSET.W
                    case OFFSET.N:
                        direction = OFFSET.E
                    case OFFSET.W:
                        direction = OFFSET.S
                y += direction[0]
                x += direction[1]
            case  "\\":
                # print(tab, "  \\", y, x, direction)
                visited.append((y, x, direction[2]))
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


def resolve_part1():

    grid = data.grid
    visited = []

    followPath(grid, visited, (0, 0), OFFSET.E)
    showGrid(grid)
    print()

    # print(visited)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = "."
    for cell in visited:
        grid[cell[0]][cell[1]] = "#"
    visitedCnt = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                visitedCnt += 1
    showGrid(grid)

    return visitedCnt


def countVisited(grid, visited, cell, direction):
    followPath(grid, visited, (cell[0], cell[1]), direction)
    # showGrid(grid)

    # print(visited)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = "."
    for cell in visited:
        grid[cell[0]][cell[1]] = "#"
    visitedCnt = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                visitedCnt += 1
    # showGrid(grid)
    return visitedCnt


def resolve_part2():
    grid = data.grid
    showGrid(grid)

    visitedCnt = []

    for y, direction in [(0, OFFSET.S), (len(grid) - 1, OFFSET.N)]:
        for x in range(len(grid[0])):
            workGrid = copy.deepcopy(grid)
            visited = []
            visitedCnt.append(countVisited(
                workGrid, visited, (y, x), direction))
            print(Ansi.blue, direction[2], y, x, visitedCnt[-1], Ansi.norm)
            # showGrid(workGrid)
            # print()

    for x, direction in [(0, OFFSET.E), (len(grid[y]) - 1, OFFSET.W)]:
        for y in range(len(grid)):
            workGrid = copy.deepcopy(grid)
            visited = []
            visitedCnt.append(countVisited(
                workGrid, visited, (y, x), direction))
            print(Ansi.blue, direction[2], y, x, visitedCnt[-1], Ansi.norm)
            # showGrid(workGrid)
            # print()

    print(visitedCnt)
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
