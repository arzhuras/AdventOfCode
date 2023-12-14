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
    data.grid = []

    data.grid = loadMatrix2d(inputFile)[0]


##################
### PROCEDURES ###
##################

def cycle(grid, moves=[OFFSET.N]):
    maxY = len(grid)
    maxX = len(grid[0])
    for move in moves:
        yLoop = (0, maxY, 1)
        if move[0] == 1:
            yLoop = (maxY-1, -1, -1)

        xLoop = (0, maxX, 1)
        if move[1] == 1:
            xLoop = (maxX-1, -1, -1)

        for y in range(*yLoop):
            for x in range(*xLoop):
                if grid[y][x] == "O":
                    newY = y
                    newX = x
                    tmpY = newY + move[0]
                    tmpX = newX + move[1]
                    while tmpY >= 0 and tmpY < maxY and tmpX >= 0 and tmpX < maxX and grid[tmpY][tmpX] == ".":
                        newY = tmpY
                        newX = tmpX
                        tmpY += move[0]
                        tmpX += move[1]
                    if newY != y or newX != x:
                        grid[newY][newX] = "O"
                        grid[y][x] = "."
        # print(move)
        # showGrid(grid)
        # print()


def calcLoad(grid):
    load = 0
    factor = len(grid)
    for row in grid:
        load += factor * row.count("O")
        factor -= 1
    return load


def resolve_part1():
    grid = data.grid

    cycle(grid, [OFFSET.N])

    showGrid(grid)

    return calcLoad(grid)


def resolve_part2():

    grid = data.grid

    for i in range(cycleStart + len(cycleLoad) - 1):
        cycle(grid, [OFFSET.N, OFFSET.W, OFFSET.S, OFFSET.E])
        load = calcLoad(grid)
        if i == cycleStart - 1:
            print("CYCLE START")
        print("CYCLE", i+1, load, cycleLoad[(i+1-cycleStart) % len(cycleLoad)])

    i = 1000000000 - 1
    return cycleLoad[(i+1-cycleStart) % len(cycleLoad)]


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
cycleStart = 4
cycleLoad = [69, 65, 64, 65, 63, 68, 69]  # sample


# MAX_ROUND = 1000
inputFile = "input.txt"
cycleStart = 179
cycleLoad = [91039, 91031, 91003, 90974, 90950, 90923, 90918, 90931,
             90946, 90982, 91016, 91038, 91057, 91050]  # input start at cycle 179

data.rawInput = readInputFile(inputFile)

initData()
res = None
showGrid(data.grid)
print()

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
