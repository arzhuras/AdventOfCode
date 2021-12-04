import sys
import os
import time
import re
import copy
import math

from collections import namedtuple

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
print(f"=== {SCRIPT_NAME} ===")


def readInputFile(file=INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines


g_inputLines = []
g_data_l = []
g_grid_d = {}
g_flipCount_d = {}

# g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure():
    global g_data_l
    global g_grid_d
    global g_flipCount_d

    g_data_l = []
    g_grid_d = {}
    g_flipCount_d = {}

    # https://pythex.org/
    # patternRule = r"^(\d*): (\d*) (\d*) \| (\d*)-(\d*)
    for line in g_inputLines:
        g_data_l.append(list(line))


def nextTile(curLine, curIdx):
    nextIdx = curIdx
    ofsX = 0
    ofsY = 0

    if (g_data_l[curLine][nextIdx] == 'n'):
        ofsY = 1
        nextIdx += 1
    elif g_data_l[curLine][nextIdx] == 's':
        ofsY = -1
        nextIdx += 1

    if (g_data_l[curLine][nextIdx] == 'w'):
        if (ofsY == 0):
            ofsX = -2
        else:
            ofsX = -1
    elif (g_data_l[curLine][nextIdx] == 'e'):
        if (ofsY == 0):
            ofsX = 2
        else:
            ofsX = 1

    nextIdx += 1
    # print (f"    {g_data_l[curLine][curIdx:nextIdx]} ({ofsX}, {ofsY})")

    return ofsX, ofsY, nextIdx


def blackNeighbors(arg_x, arg_y):

    blackCount = 0
    for ofsX, ofsY in [(2, 0), (1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1)]:
        if (arg_x + ofsX in g_grid_d):
            if (arg_y + ofsY in g_grid_d[arg_x + ofsX]):
                if (g_grid_d[arg_x + ofsX][arg_y + ofsY] == False):
                    blackCount += 1
        #print(f"  ({arg_x},{arg_y}) -> ({arg_x + ofsX},{arg_y + ofsY}) {blackCount}")
    return blackCount


def showGrid():
    minX = min(g_grid_d.keys())
    maxX = max(g_grid_d.keys())

    minY = 0
    maxY = 0
    for idxX in g_grid_d.keys():
        if (min(g_grid_d[idxX].keys()) < minY):
            minY = min(g_grid_d[idxX].keys())
        if (max(g_grid_d[idxX].keys()) > maxY):
            maxY = max(g_grid_d[idxX].keys())

    #minX = -9
    #maxX = 9
    #minY = -5
    #maxY = 5

    tmpS = ""
    tmpS2 = ""
    for idxX in range(minX, maxX + 1):
        tmpS += f"{idxX:2}"
        tmpS2 += f"{idxX:2}"
    print(f"     {tmpS}   {tmpS2}")

    for idxY in range(minY, maxY + 1):
        tmpS = ""
        tmpS2 = ""
        for idxX in range(minX, maxX + 1):
            if (abs(idxX) % 2 == 0 and abs(idxY) % 2 == 1):
                tmpS += "  "
                tmpS2 += "  "
                continue

            if (abs(idxX) % 2 == 1 and abs(idxY) % 2 == 0):
                tmpS += "  "
                tmpS2 += "  "
                continue

            if (idxX not in g_grid_d):
                tmpS += " ."
                tmpS2 += "  "
                continue

            if (idxY not in g_grid_d[idxX]):
                tmpS += " ."
                tmpS2 += "  "
                continue

            if (g_grid_d[idxX][idxY] == True):
                tmpS += " ."
            else:
                tmpS += " #"

            if (idxX in g_flipCount_d and idxY in g_flipCount_d[idxX]):
                tmpS2 += f"{g_flipCount_d[idxX][idxY]:>2}"
            else:
                tmpS2 += "  "
            #print(f"({idxX}, {idxY}) = {g_grid_d[idxX][idxY]}")
        print(f"[{idxY:2}] {tmpS}   {tmpS2}")


def resolve_part2():
    global g_grid_d
    global g_flipCount_d
    DAY_ROUND = 100

    showGrid()
    print("")

    # print("resolve_part2():", g_data_d}

    for day in range(1, DAY_ROUND + 1):
        tmpGrid_d = copy.deepcopy(g_grid_d)
        tmpFlipCount_d = {}

        # find min and max
        minX = min(g_grid_d.keys()) - 2
        maxX = max(g_grid_d.keys()) + 2

        minY = 0
        maxY = 0
        for idxX in g_grid_d.keys():
            if (min(g_grid_d[idxX].keys()) < minY):
                minY = min(g_grid_d[idxX].keys())
            if (max(g_grid_d[idxX].keys()) > maxY):
                maxY = max(g_grid_d[idxX].keys())
        minY -= 1
        maxY += 1

        for idxY in range(minY, maxY + 1):
            for idxX in range(minX, maxX + 1):
                if (abs(idxX) % 2 == 0 and abs(idxY) % 2 == 1):
                    continue

                if (abs(idxX) % 2 == 1 and abs(idxY) % 2 == 0):
                    continue

                if (idxX in g_grid_d and idxY in g_grid_d[idxX]):
                    tile = g_grid_d[idxX][idxY]
                else:
                    tile = True
                #print(f"TEST ({idxX:2}, {idxY:2}) = {tile}")

                blackNeighbor = blackNeighbors(idxX, idxY)
                #print(f"  ({idxX:2}, {idxY:2}) = {tile} : {blackNeighbor}")

                if (tile == False and (blackNeighbor == 0 or blackNeighbor > 2)):
                    #print(f"FLIP TRUE ({idxX:2}, {idxY:2}) = {tile} : {blackNeighbor}")
                    if (idxX not in tmpGrid_d):
                        tmpGrid_d[idxX] = {}
                    tmpGrid_d[idxX][idxY] = True

                    if (idxX not in tmpFlipCount_d):
                        tmpFlipCount_d[idxX] = {}
                        if (idxY not in tmpFlipCount_d[idxX]):
                            tmpFlipCount_d[idxX][idxY] = '-'
                        else:
                            tmpFlipCount_d[idxX][idxY] = '-'
                    else:
                        tmpFlipCount_d[idxX][idxY] = '-'
                    # print(tmpGrid_d)
                elif (tile == True and blackNeighbor == 2):
                    #print(f"FLIP BLACK ({idxX:2}, {idxY:2}) = {tile} : {blackNeighbor}")
                    if (idxX not in tmpGrid_d):
                        tmpGrid_d[idxX] = {}
                    tmpGrid_d[idxX][idxY] = False

                    if (idxX not in tmpFlipCount_d):
                        tmpFlipCount_d[idxX] = {}
                        if (idxY not in tmpFlipCount_d[idxX]):
                            tmpFlipCount_d[idxX][idxY] = '+'
                        else:
                            tmpFlipCount_d[idxX][idxY] = '+'
                    else:
                        tmpFlipCount_d[idxX][idxY] = '+'

        # result
        # print(g_grid_d)
        g_grid_d = tmpGrid_d
        g_flipCount_d = tmpFlipCount_d
        # showGrid()
        blackCount = 0
        for gridX in g_grid_d.values():
            for gridXY in gridX.values():
                if (gridXY == False):
                    blackCount += 1

        print(f"DAY {day} = {blackCount}")

    return -1


def resolve_part1():
    # print("resolve_part1():", g_data_l)
    # g_grid_d = {}

    for lineIdx in range(len(g_data_l)):
        curX = 0
        curY = 0
        tileIdx = 0
        maxTileIdx = len(g_data_l[lineIdx])
        # print (f"{g_data_l[lineIdx]}")
        while (tileIdx < maxTileIdx):
            ofsX, ofsY, tileIdx = nextTile(lineIdx, tileIdx)
            # print (f"  ({ofsX}, {ofsY}) -> {tileIdx}")
            curX += ofsX
            curY += ofsY
            # print (f"  ({curX}, {curY})")

        if (curX not in g_grid_d):
            g_grid_d[curX] = {}
            g_flipCount_d[curX] = {}

        if (curY not in g_grid_d[curX]):  # force to black for first time
            g_grid_d[curX][curY] = False
            g_flipCount_d[curX][curY] = 1
        else:  # flip
            g_grid_d[curX][curY] = not g_grid_d[curX][curY]
            g_flipCount_d[curX][curY] += 1
        # print (f"  ({curX}, {curY}) = {g_grid_d[curX][curY]}")

        # showGrid()

    # print(g_grid_d)
    # print(g_flipCount_d)
    showGrid()
    blackCount = 0
    for gridX in g_grid_d.values():
        for gridY in gridX.values():
            if (gridY == False):
                blackCount += 1

    return blackCount


#g_inputLines = readInputFile("AoC_2020_24_sample.txt")
g_inputLines = readInputFile()

res = -1

###
# PART 1
###

# '''
print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''

###
# PART 2
###

# '''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

# initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''
