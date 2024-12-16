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


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red, "-1": Ansi.grey}
# from matrix3d import *


def initData():
    data.rules = defaultdict(lambda: set())
    # data.line = "".join(data.rawInput)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


class Region:
    zoneIdx = 0
    gardenType = ""
    gardenPlotLst = []
    area = 0
    perimeter = 0
    side = 0
    """
    def __init__(self):
        self.zoneIdx = 0
        self.gardenPlotLst = []
        self.area = 0
        self.perimeter = 0

    def __repr__(self):
        return f"{self.zoneIdx}, {self.gardenPlotLst}, {self.area}, {self.perimeter}"

    def __str__(self):
        return f"{self.zoneIdx}, {self.gardenPlotLst}, {self.area}, {self.perimeter}"
    """


def resolve_bothpart():
    grid = data.gridLst[0]
    extendGrid(grid)
    gridBorder = 1

    zone = [[-1 for x in range(len(grid[0]))] for y in range(len(grid))]
    # showGrid(zone)

    # showGrid(grid)

    # map the zone
    zoneIdx = 0
    regionLst = []
    for y in range(gridBorder, len(grid) - gridBorder):
        for x in range(gridBorder, len(grid[y]) - gridBorder):
            if zone[y][x] == -1:  # new zone
                gardenType = grid[y][x]
                region = Region()
                regionLst.append(region)
                zone[y][x] = zoneIdx
                scootLst = [(y, x)]
                while len(scootLst) > 0:
                    scootY, scootX = scootLst.pop()
                    region.zoneIdx = zoneIdx
                    region.gardenType = gardenType
                    region.gardenPlotLst.append((scootY, scootX))
                    region.area += 1
                    for offset in OFFSET.CROSS:
                        if grid[scootY + offset.y][scootX + offset.x] == gardenType:
                            if zone[scootY + offset.y][scootX + offset.x] == -1:
                                zone[scootY + offset.y][scootX + offset.x] = zoneIdx
                                scootLst.append((scootY + offset.y, scootX + offset.x))
                        else:
                            region.perimeter += 1
                zoneIdx += 1
    # showGrid(zone, MATRIX2D_COLORSET, 4)

    # calculate price1: perimeter
    price1 = 0
    for region in regionLst:
        price1 += region.area * region.perimeter
        if False:
            print(
                region.zoneIdx,
                region.gardenType,
                region.area,
                region.perimeter,
                region.area * region.perimeter,
                price1,
            )

    # calculate price2: side
    price2 = 0
    for zoneIdx, region in enumerate(regionLst):
        # Horizontal sides
        for y in range(gridBorder, len(zone) - gridBorder):
            for offset in OFFSET.N, OFFSET.S:
                flag = False
                for x in range(gridBorder, len(zone[y]) - gridBorder):
                    if (
                        flag == False
                        and zone[y][x] == zoneIdx
                        and zone[y + offset.y][x] != zoneIdx
                    ):
                        flag = True
                        region.side += 1
                    elif flag == True and (
                        zone[y][x] != zoneIdx or zone[y + offset.y][x] == zoneIdx
                    ):
                        flag = False

        # Vertical sides
        for x in range(gridBorder, len(zone[y]) - gridBorder):
            for offset in OFFSET.W, OFFSET.E:
                flag = False
                for y in range(gridBorder, len(zone) - gridBorder):
                    if (
                        flag == False
                        and zone[y][x] == zoneIdx
                        and zone[y][x + offset.x] != zoneIdx
                    ):
                        flag = True
                        region.side += 1
                    elif flag == True and (
                        zone[y][x] != zoneIdx or zone[y][x + offset.x] == zoneIdx
                    ):
                        flag = False

        price2 += region.area * region.side
        if False:
            print(
                "->",
                region.zoneIdx,
                region.gardenType,
                region.area,
                region.side,
                region.area * region.side,
                price2,
            )

    return price1, price2


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
inputFile = "sample3.txt"
inputFile = "sample4.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

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


### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
