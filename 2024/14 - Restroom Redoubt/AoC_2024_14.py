import copy
import math
import time
from collections import defaultdict
from functools import reduce
from operator import mul

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


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():
    data.fields = []
    for line in data.rawInput:
        line = line.replace("p", "").replace("v", "").replace("=", "").replace(",", " ")
        data.fields.append(list(map(int, line.split())))
    # data.fields = [[2, 4, 2, -3]]
    # print("fields:", data.fields)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def showRobots(width, height, robots, condition=0):
    grid = [["." for i in range(width)] for j in range(height)]

    for robot in robots:
        if grid[robot[1]][robot[0]] == ".":
            grid[robot[1]][robot[0]] = "1"
        else:
            grid[robot[1]][robot[0]] = str(int(grid[robot[1]][robot[0]]) + 1)
    if condition == 0:
        showGrid(grid, MATRIX2D_COLORSET)
    else:
        for y in range(height):
            if grid[y].count(".") <= condition:
                print("y", y)
                showGrid(grid, MATRIX2D_COLORSET)
                break


def resolve_bothpart():
    roomWidth = 11
    roomHeight = 7
    roomWidth = 101
    roomHeight = 103
    for round in range(10000):
        for robot in data.fields:
            # print(round + 1, robot, end="")
            for coord, vel, size in (0, 2, roomWidth), (1, 3, roomHeight):
                robot[coord] = (robot[coord] + robot[vel]) % (size + 0)
            # print(" -> ", robot)
        print(round + 1)
        showRobots(roomWidth, roomHeight, data.fields, 80)

    quadNW = 0
    quadNE = 0
    quadSW = 0
    quadSE = 0
    midHor = roomWidth // 2
    midVer = roomHeight // 2
    # print(roomWidth, midHor, roomHeight, midVer)
    for robot in data.fields:
        if robot[0] < midHor:  # W
            if robot[1] < midVer:  # N
                quadNW += 1
            elif robot[1] > midVer:  # S
                quadSW += 1
        elif robot[0] > midHor:  # E
            if robot[1] < midVer:  # N
                quadNE += 1
            elif robot[1] > midVer:  # S
                quadSE += 1

    # print(quadNW, quadNE, quadSW, quadSE)

    showRobots(roomWidth, roomHeight, data.fields)
    return reduce(mul, [quadNW, quadNE, quadSW, quadSE]), None


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
# data.grid = loadMatrix2d(inputFile)


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


### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
