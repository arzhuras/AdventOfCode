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

    moves = None
    startPosX = None
    startPosY = None


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red, "@": Ansi.yellow}
# from matrix3d import *


def initData():
    data.grid = loadGrid(data.rawInput)
    # showGrid(data.grid, MATRIX2D_COLORSET, 1)

    data.startPosX = 0
    data.startPosY = 0
    for y in range(len(data.grid)):
        for x in range(len(data.grid[0])):
            if data.grid[y][x] == "@":
                data.startPosY = y
                data.startPosX = x
                break
        if data.startPosY != 0:
            break

    data.moves = []
    for line in data.rawInput[len(data.grid) + 1 :]:
        data.moves += [car for car in line]

    # print("moves:", data.moves)


##################
### PROCEDURES ###
##################


def doMove(posY, posX, offset, grid):
    if grid[posY + offset.y][posX + offset.x] == "O":
        endX = posX + 2 * offset.x
        endY = posY + 2 * offset.y
        while grid[endY][endX] == "O":
            endX += offset.x
            endY += offset.y
        if grid[endY][endX] == ".":
            grid[posY][posX] = "."
            grid[posY + offset.y][posX + offset.x] = "@"
            grid[endY][endX] = "O"
            return posY + offset.y, posX + offset.x
        else:
            return posY, posX

    if grid[posY + offset.y][posX + offset.x] == ".":
        grid[posY][posX] = "."
        grid[posY + offset.y][posX + offset.x] = "@"
        return posY + offset.y, posX + offset.x

    return posY, posX


def resolve_part1():
    grid = data.grid
    posX = data.startPosX
    posY = data.startPosY
    # showGrid(grid, MATRIX2D_COLORSET, 3)

    for move in data.moves:
        # print("move:", move)
        offset = OFFSET.MOVE[move]
        posY, posX = doMove(posY, posX, offset, grid)
        # showGrid(grid, MATRIX2D_COLORSET, 1)

    sum1 = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                sum1 += (y * 100) + x

    return sum1


def doMove2(posY, posX, offset, grid):
    endX = posX + offset.x
    endY = posY + offset.y
    # print("domove2()", posY, posX, offset, "endY:", endY, "endX:", endX, grid[endY][endX])
    if grid[endY][endX] == "#":
        return posY, posX

    if grid[endY][endX] == ".":
        grid[posY][posX] = "."
        grid[endY][endX] = "@"
        return endY, endX

    if offset.y == 0:  # horizontal
        while grid[endY][endX] == "[" or grid[endY][endX] == "]":
            endX += 2 * offset.x
            # print("endY:", endY, "endX:", endX, grid[endY][endX])
        if grid[endY][endX] == ".":
            while grid[endY][endX] != "@":
                grid[endY][endX] = grid[endY][endX - offset.x]
                endX -= offset.x
            grid[endY][endX] = "."
            return posY + offset.y, posX + offset.x

    else:  # vertical
        if grid[endY][endX] == "[":
            stack = [[endX, endX + 1]]
        else:  # ]
            stack = [[endX - 1, endX]]
        stackIdx = 0
        while True:
            stack.append([])
            for x in stack[stackIdx]:
                if grid[endY + (stackIdx * offset.y) + offset.y][x] == "#":
                    return posY, posX

                if grid[endY + (stackIdx * offset.y) + offset.y][x] == "[":
                    stack[stackIdx + 1] += [x, x + 1]
                elif grid[endY + (stackIdx * offset.y) + offset.y][x] == "]":
                    stack[stackIdx + 1] += [x - 1, x]
            if len(stack[stackIdx + 1]) == 0:
                break
            stackIdx += 1

        for y in range(stackIdx, -1, -1):
            # print(y, "stack", stack[y])
            for x in stack[y]:
                if grid[endY + (y * offset.y) + offset.y][x] == ".":
                    grid[endY + (y * offset.y) + offset.y][x] = grid[
                        endY + (y * offset.y)
                    ][x]
                    grid[endY + (y * offset.y)][x] = "."
        grid[endY][endX] = "@"
        grid[posY][posX] = "."
        return endY, endX

    return posY, posX


def resolve_part2():
    grid = data.grid
    posX = data.startPosX
    posY = data.startPosY

    # extend grid wide
    grid2 = []
    for y in range(len(grid)):
        tmpLst = []
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                tmpLst += ["#", "#"]
            elif grid[y][x] == "O":
                tmpLst += ["[", "]"]
            elif grid[y][x] == ".":
                tmpLst += [".", "."]
            elif grid[y][x] == "@":
                posX = len(tmpLst)
                tmpLst += ["@", "."]
        grid2.append(tmpLst)

    # showGrid(grid2, MATRIX2D_COLORSET, 3)

    for moveIdx, move in enumerate(data.moves):
        # print(moveIdx, "move:", move)
        offset = OFFSET.MOVE[move]
        posY, posX = doMove2(posY, posX, offset, grid2)
        # showGrid(grid2, MATRIX2D_COLORSET, 3)

    sum2 = 0
    for y in range(len(grid2)):
        for x in range(len(grid2[0])):
            if grid2[y][x] == "[":
                sum2 += (y * 100) + x

    return sum2


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
# inputFile = "sample2.txt"
# inputFile = "sample3.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)


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
initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
