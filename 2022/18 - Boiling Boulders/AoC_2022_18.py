from tools import *
import time
from collections import deque
import operator

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    cubes = None
    adjacent = None
    external = None

    air = None
    airAdjacent = None

    grid3d = None  # 3d list : "." = air inside, "#" = lava, " " = air exterior


data = Data()


SCAN_SIZE = 22
ADJACENT_OFFSET = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
# ADJACENT_OFFSET2 = [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (-1, 1, 0), (0, 1, 0), (1, 1, 0)]


def initData():
    data.line = []

    data.cubes = []
    data.air = []
    data.adjacent = {}
    data.airAdjacent = {}
    data.grid3d = {}
    for line in data.rawInput:
        # line = line.replace(",", "")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        coord = tuple(map(int, line.split(",")))
        data.cubes.append(coord)  # (x,y,z)
        data.adjacent[coord] = []
    data.cubes.sort(key=operator.itemgetter(2, 1, 0))
    # fields = line.split()

    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    totalSurf = 0
    for elt in data.cubes:
        # print("->", elt, "= ", end="")
        nbSurf = 6
        for offset in ADJACENT_OFFSET:
            adj = elt[0] + offset[0], elt[1] + offset[1], elt[2] + offset[2]
            if adj in data.adjacent:
                data.adjacent[elt].append(adj)
                nbSurf -= 1
        # print(nbSurf, data.adjacent[elt])
        totalSurf += nbSurf
        # print("  ", nbSurf, totalSurf)
        # print("  ", data.adjacent[elt])

    return totalSurf


def show3dmatrix(matrix):
    for z in range(len(matrix)):
        print(f"[{z}]")
        for y in range(len(matrix[z])):
            for x in range(len(matrix[z][y])):
                print(matrix[z][y][x], end="")
            print()
        print()


def searchExterior():
    # find external/internal position
    data.grid3d[0][0][0] = " "
    scan = True
    while scan == True:
        updated = 0
        for z in range(SCAN_SIZE):
            for y in range(SCAN_SIZE):
                for x in range(SCAN_SIZE):
                    if data.grid3d[z][y][x] == ".":
                        for ofsX, ofsY, ofsZ in ADJACENT_OFFSET:
                            newX = x + ofsX
                            if newX < 0 or newX >= SCAN_SIZE:
                                continue

                            newY = y + ofsY
                            if newY < 0 or newY >= SCAN_SIZE:
                                continue

                            newZ = z + ofsZ
                            if newZ < 0 or newZ >= SCAN_SIZE:
                                continue

                            if data.grid3d[newZ][newY][newX] == " ":
                                data.grid3d[z][y][x] = " "
                                updated += 1
        if updated == 0:
            scan = False


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    data.grid3d = [[["." for x in range(SCAN_SIZE)] for y in range(SCAN_SIZE)] for z in range(SCAN_SIZE)]

    for elt in data.cubes:
        data.grid3d[elt[2]][elt[1]][elt[0]] = "#"

    searchExterior()

    # show3dmatrix(data.grid3d)

    totalSurf = 0
    for elt in data.cubes:
        # print("->", elt, "= ", end="")
        nbSurf = 6
        for ofsX, ofsY, ofsZ in ADJACENT_OFFSET:
            newX = elt[0] + ofsX
            if newX < 0 or newX >= SCAN_SIZE:
                continue

            newY = elt[1] + ofsY
            if newY < 0 or newY >= SCAN_SIZE:
                continue

            newZ = elt[2] + ofsZ
            if newZ < 0 or newZ >= SCAN_SIZE:
                continue

            adj = data.grid3d[newZ][newY][newX]
            if adj == "." or adj == "#":
                nbSurf -= 1
        totalSurf += nbSurf

    return totalSurf


############
### MAIN ###
############

inputFile = "sample2.txt"

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)


initData()


### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# 4178 high