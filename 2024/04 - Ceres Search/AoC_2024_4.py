from tools import *
import time
import math
import copy
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
    grid = None


data = Data()

###  /modules libraries ###
from matrix2d import *
MATRIX2D_COLORSET = {"X": Ansi.red}
# from matrix3d import *


def initData():
    return



##################
### PROCEDURES ###
##################


def resolve_part1():
    grid = copy.deepcopy(data.grid[0])
    grid_height = len(grid)
    grid_width = len(grid[0])
    #print(grid_height, grid_width)
    extendGrid(grid)
    border_size = 1
    #showGrid(grid)

    xmasCount = 0
    for y in range(border_size, grid_height + border_size):
        for x in range(border_size, grid_width + border_size):
            for offset in OFFSET.AROUND:
                if grid[y][x] != "X":
                    continue
                #print(grid[y][x])
                if grid[y+offset[0]][x+offset[1]] == "M" and grid[y+offset[0]*2][x+offset[1]*2] == "A" and grid[y+offset[0]*3][x+offset[1]*3] == "S":
                    xmasCount += 1
                    #print(f"GOTCHA {xmasCount:04}: y:{y} x:{y} OFFSET {offset}")

    return xmasCount


def resolve_part2():
    grid = copy.deepcopy(data.grid[0])
    grid_height = len(grid)
    grid_width = len(grid[0])
    #print(grid_height, grid_width)
    extendGrid(grid)
    border_size = 1
    #showGrid(grid)

    xmasCount = 0
    for y in range(border_size, grid_height + border_size):
        for x in range(border_size, grid_width + border_size):
            if grid[y][x] != "A":
                continue
            for offsetA,offsetB in (OFFSET.NW, OFFSET.SW),(OFFSET.NW, OFFSET.NE),(OFFSET.NE, OFFSET.SE),(OFFSET.SE, OFFSET.SW),:
                #print(grid[y][x])
                if grid[y+offsetA[0]][x+offsetA[1]] == "M" and grid[y+offsetB[0]][x+offsetB[1]] == "M" and grid[y+offsetA[0]*-1][x+offsetA[1]*-1] == "S" and grid[y+offsetB[0]*-1][x+offsetB[1]*-1] == "S":
                    xmasCount += 1
                    #print(f"GOTCHA {xmasCount:04}: y:{y} x:{y} OFFSET {offsetA} {offsetB}")

    return xmasCount


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

#data.rawInput = readInputFile(inputFile)
data.grid = loadMatrix2d(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.6f}s): {Ansi.blue}{res}{Ansi.norm}")

#exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.6f}s): {Ansi.blue}{res}{Ansi.norm}")
