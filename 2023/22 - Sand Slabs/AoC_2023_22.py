from matrix3d import *
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
    bricks = None
    maxCoord = None
    bricksIsSupporting = None
    bricksSupportedBy = None

    grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan}


def initData():
    data.bricks = []
    data.maxCoord = [0, 0, 0]

    for line in data.rawInput:
        line = line.replace(",", " ")
        line = line.replace("~", " ")
        intFields = list(map(int, line.split()))
        intFields.reverse()  # on remet dans l'ordre z, y, x
        for coordIdx, coord in enumerate(intFields):
            if coord > data.maxCoord[coordIdx % 3]:
                data.maxCoord[coordIdx % 3] = coord

        data.bricks.append(
            [intFields[3:], intFields[0:3]])

    data.bricksIsSupporting = [[] for _ in range(len(data.bricks))]
    data.bricksSupportedBy = [[] for _ in range(len(data.bricks))]

    # print("bricks:", data.bricks)
    # print("maxCoord:", data.maxCoord)

    # data.grid = []
    # data.grid = loadMatrix2d(inputFile)[0]
    # showGrid(data.grid)

    # data.grids = []
    # data.grids = loadMatrix2d(inputFile)
    # showGridLst(data.grid)


##################
### PROCEDURES ###
##################

def putBrick(grid3d, brickCoord, car="."):
    z1, y1, x1 = brickCoord[0]
    z2, y2, x2 = brickCoord[1]
    if z1 != z2:  # axe des z
        for z in range(z1, z2+1):
            grid3d[z][y1][x1] = car
    elif y1 != y2:  # axe des y
        for y in range(y1, y2+1):
            grid3d[z1][y][x1] = car
    else:  # axe des x
        for x in range(x1, x2+1):
            grid3d[z1][y1][x] = car
    # print(grid3d)


# return min z et la liste des brick sur laquelle repose la brick d'origine
def getMinZ(grid3d, brickCoord):
    z1, y1, x1 = brickCoord[0]
    z2, y2, x2 = brickCoord[1]

    minZ = z1
    supportBrick = []
    while minZ > 0:
        # parcours
        minZ = minZ - 1
        if z1 != z2:  # axe des z
            if grid3d[minZ][y1][x1] != ".":
                supportBrick.append(grid3d[minZ][y1][x1])
        elif y1 != y2:  # axe des y
            for y in range(y1, y2+1):
                if grid3d[minZ][y][x1] != ".":
                    supportBrick.append(grid3d[minZ][y][x1])
        else:  # axe des x
            for x in range(x1, x2+1):
                if grid3d[minZ][y1][x] != ".":
                    supportBrick.append(grid3d[minZ][y1][x])
        if len(supportBrick) > 0:  # on a atterri
            minZ = minZ + 1
            break
    # print(minZ, supportBrick)
    return (minZ, supportBrick)


def resolve_part1():
    grid3d = data.grid
    bricks = data.bricks
    bricksIsSupporting = data.bricksIsSupporting
    bricksSupportedBy = data.bricksSupportedBy
    maxZ, maxY, maxX = data.maxCoord

    """ Test la grille 3D
    grid3d = [[[(z, y, x) for x in range(maxX + 1)]
               for y in range(maxY + 1)] for z in range(maxZ + 1)]
    showMatrix3dV(grid3d[0:2])
    """

    # init grid
    grid3d = [[["." for x in range(maxX + 1)]
               for y in range(maxY + 1)] for z in range(maxZ + 1)]
    for brickIdx, brickCoord in enumerate(bricks):
        putBrick(grid3d, brickCoord, brickIdx)
    showMatrix3dV(grid3d[0:5], 5)

    # fall brick
    for brickIdx, brickCoord in enumerate(bricks):
        minZ1, brickSupportedBy = getMinZ(grid3d, brickCoord)
        # print(brickIdx, minZ1, brickSupportedBy)

        # update grid
        putBrick(grid3d, brickCoord, ".")
        minZ2 = minZ1 + (brickCoord[1][0] - brickCoord[0][0])
        brickCoord[0][0] = minZ1
        brickCoord[1][0] = minZ2
        putBrick(grid3d, brickCoord, brickIdx)

        # update supportedBrick list
        bricksSupportedBy[brickIdx] = brickSupportedBy
        for supportedBrickIdx in brickSupportedBy:
            bricksIsSupporting[supportedBrickIdx].append(brickIdx)

    # check disintegrable bricks
    showMatrix3dV(grid3d, 5)
    print()
    disintegrableBrickCnt = 0
    for brickIdx in range(len(bricks)):
        bricksIsSupporting[brickIdx] = set(bricksIsSupporting[brickIdx])
        bricksSupportedBy[brickIdx] = set(bricksSupportedBy[brickIdx])
        disintegrable = True
        for brickIsSupportingIdx in bricksIsSupporting[brickIdx]:
            # print(brickSupportingIdx, bricksSupporting[brickSupportingIdx])
            if len(bricksSupportedBy[brickIsSupportingIdx]) < 2:
                disintegrable = False
                break
        print(brickIdx, f"{disintegrable:5}", "supporting",
              f"{str(bricksIsSupporting[brickIdx]):20}", "supportedBy", bricksSupportedBy[brickIdx])
        if disintegrable == True:
            disintegrableBrickCnt += 1

    return disintegrableBrickCnt


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

exit()

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
