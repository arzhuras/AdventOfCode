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
    data.fields = []
    data.grid = []

    data.grid = loadMatrix2d(inputFile)[0]

    # print("data.grid:", data.grid)
    # showGrid(data.grid)


##################
### PROCEDURES ###
##################

# offset tuple are (y,x)
CONNECTION = {"|": (OFFSET.N, OFFSET.S),
              "-": (OFFSET.E, OFFSET.W),
              "L": (OFFSET.N, OFFSET.E),
              "J": (OFFSET.N, OFFSET.W),
              "7": (OFFSET.S, OFFSET.W),
              "F": (OFFSET.S, OFFSET.E),
              }

# tableau de la connexion sortante en fonction de la connexion entrante
NEXT_CONNECTION = {}
for key, value in CONNECTION.items():
    NEXT_CONNECTION[(key, value[0])] = value[1]
    NEXT_CONNECTION[(key, value[1])] = value[0]
print("CONNECTION", CONNECTION)
print()
print("NEXT_CONNECTION", NEXT_CONNECTION)
print()


def getStartInfo():
    grid = data.grid
    start = None
    # search start
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (grid[y][x] == 'S'):
                start = (y, x)
                break
        if start != None:
            break

    # search neighbor connection for S
    neighborsOffset = []
    for offset in OFFSET.CROSS:
        neighbor = grid[start[0] + offset[0]][start[1] + offset[1]]
        if (neighbor, OFFSET.OPPOSITE[offset]) in NEXT_CONNECTION:
            neighborsOffset.append(offset)

    # 2 sorties possible, on prend la première qui tombe!
    offset = neighborsOffset[0]

    # identifie le type de 'S'
    for conKey, conValue in CONNECTION.items():
        if neighborsOffset[0] in conValue and neighborsOffset[1] in conValue:
            startType = conKey

    # print((start[0], start[1]), startType, neighborsOffset)

    return (start[0], start[1]), startType, neighborsOffset


def browseLoop(startCoord, offset):
    grid = data.grid

    prevOffset = OFFSET.OPPOSITE[offset]
    y = startCoord[0] + offset[0]
    x = startCoord[1] + offset[1]
    loopElt = [(startCoord[0], startCoord[1])]
    while grid[y][x] != "S":
        # print(grid[y][x], "prev", prevOffset)
        nextOffset = NEXT_CONNECTION[(grid[y][x], prevOffset)]
        loopElt.append((y, x))
        y += nextOffset[0]
        x += nextOffset[1]
        prevOffset = OFFSET.OPPOSITE[nextOffset]
        # print("  ->", grid[y][x], "next", nextOffset)

    return loopElt


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    startCoord, startType, startNeighborOffset = getStartInfo()

    # 2 sorties possibles pour le start, on prend la première au hasard!
    loopElt = browseLoop(startCoord, startNeighborOffset[0])

    return int(len(loopElt)/2)


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    grid = data.grid

    startCoord, startType, startNeighborOffset = getStartInfo()

    # 2 sorties possibles pour le start, on prend la première au hasard!
    loopElt = browseLoop(startCoord, startNeighborOffset[0])

    # mise à zéro des case n'appartenant pas à la loop pour simplifier le traitement
    grid[startCoord[0]][startCoord[1]] = startType
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (y, x) not in loopElt:
                grid[y][x] = "."
    print("RAZ")

    # On rajoute une couronne vide autour pour faire communiquer toute les zones externes
    extendGrid(grid)
    print("EXTEND")
    # showGrid(grid)

    # astuce: on rajoute des lignes et des colonnes intercalaires pour remettre en connexion les zones "squeezes"
    grid2 = []
    for y in range(len(grid)):
        grid2.append(["." for _ in range(len(grid[y])*2)])
        grid2.append(["." for _ in range(len(grid[y])*2)])
        for x in range(len(grid[y])):
            if grid[y][x] != " ":
                grid2[2*y][2*x] = grid[y][x]
                if grid[y][x] in ("-", "F", "L"):
                    grid2[2*y][2*x+1] = "-"
                if grid[y][x] in ("|", "F", "7"):
                    grid2[2*y+1][2*x] = "|"
    print("COL/LIGNE INTERCALAIRES")
    # showGrid(grid2)

    # recherche des cases intérieurs/extérieurs
    bag = [(0, 0)]
    maxY = len(grid2)
    maxX = len(grid2[0])
    while len(bag) > 0:
        curCell = bag.pop()
        grid2[curCell[0]][curCell[1]] = "O"
        for offset in OFFSET.CROSS:
            newY = curCell[0] + offset[0]
            newX = curCell[1] + offset[1]
            if newY < 0 or newY >= maxY:
                continue
            if newX < 0 or newX >= maxX:
                continue
            if grid2[newY][newX] == ".":
                bag.append((curCell[0] + offset[0], curCell[1] + offset[1]))
    print("FINAL WITH OUTSIDE")
    showGrid(grid2)

    # Compte les cases restantes -> zone interne
    insideCount = 0
    for y in range(0, maxY, 2):
        for x in range(0, maxX, 2):
            if grid2[y][x] == ".":
                insideCount += 1

    return int(insideCount)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
inputFile = "sample4.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
