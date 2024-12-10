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
    antenna = defaultdict


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():
    grid = data.grid[0]
    data.antenna = defaultdict(lambda: list())
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == ".":
                continue
            data.antenna[grid[y][x]].append((y, x))

    # print(data.antenna)


##################
### PROCEDURES ###
##################


def resolve_part1():

    grid = copy.deepcopy(data.grid[0])
    # showGrid(grid, MATRIX2D_COLORSET)

    antennaCount1 = 0
    for antennaType, antennaCoord in data.antenna.items():
        for i in range(len(antennaCoord) - 1):
            for j in range(i + 1, len(antennaCoord)):
                distY = antennaCoord[i][0] - antennaCoord[j][0]
                distX = antennaCoord[i][1] - antennaCoord[j][1]
                antinodeCoord1 = (
                    antennaCoord[i][0] + distY,
                    antennaCoord[i][1] + distX,
                )
                antinodeCoord2 = (
                    antennaCoord[j][0] - distY,
                    antennaCoord[j][1] - distX,
                )
                for coord in antinodeCoord1, antinodeCoord2:
                    if (
                        coord[0] >= 0
                        and coord[0] < len(grid)
                        and coord[1] >= 0
                        and coord[1] < len(grid[0])
                        and grid[coord[0]][coord[1]] != "#"
                    ):
                        antennaCount1 += 1
                        grid[coord[0]][coord[1]] = "#"

    # showGrid(grid, MATRIX2D_COLORSET)
    return antennaCount1


def resolve_part2():
    grid = copy.copy(data.grid[0])
    # showGrid(grid, MATRIX2D_COLORSET)

    antennaCount2 = 0
    for antennaType, antennaCoord in data.antenna.items():
        for i in range(len(antennaCoord) - 1):
            for j in range(i + 1, len(antennaCoord)):
                dist = (
                    antennaCoord[i][0] - antennaCoord[j][0],
                    antennaCoord[i][1] - antennaCoord[j][1],
                )
                for curAntennaCoord, direction in (antennaCoord[i], 1), (
                    antennaCoord[j],
                    -1,
                ):
                    factor = 1
                    antinodeCoord = (
                        curAntennaCoord[0] + dist[0] * direction * factor,
                        curAntennaCoord[1] + dist[1] * direction * factor,
                    )
                    while (
                        antinodeCoord[0] >= 0
                        and antinodeCoord[0] < len(grid)
                        and antinodeCoord[1] >= 0
                        and antinodeCoord[1] < len(grid[0])
                    ):
                        if grid[antinodeCoord[0]][antinodeCoord[1]] != "#":
                            antennaCount2 += 1
                            grid[antinodeCoord[0]][antinodeCoord[1]] = "#"
                        factor += 1
                        antinodeCoord = (
                            curAntennaCoord[0] + dist[0] * direction * factor,
                            curAntennaCoord[1] + dist[1] * direction * factor,
                        )
                    for coord in antennaCoord[i], antennaCoord[j]:
                        if grid[coord[0]][coord[1]] != "#":
                            antennaCount2 += 1
                            grid[coord[0]][coord[1]] = "#"

    # showGrid(grid, MATRIX2D_COLORSET)
    return antennaCount2


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
# inputFile = "sample2.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

# data.rawInput = readInputFile(inputFile)
data.grid = loadMatrix2d(inputFile)


### PART 1 ###
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
res1 = resolve_part1()
# res1, res2 = resolve_bothpart()
endTime = time.time()

print()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
