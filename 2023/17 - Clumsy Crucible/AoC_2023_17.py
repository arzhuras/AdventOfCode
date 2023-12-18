import time
import math
import copy

from collections import deque
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

    # grid = None


data = Data()


def initData():
    data.fields = []

    data.grid = []
    data.grid = loadMatrix2d(inputFile)[0]

    showGrid(data.grid)

##################
### PROCEDURES ###
##################


def getVoisins(grid, cell, dirIn, dirInCnt):
    print("  getVoisins", cell, dirIn, dirInCnt)
    voisins = []
    maxY = len(grid)
    maxX = len(grid[0])
    for offset in OFFSET.NOTURNINGBACK[dirIn]:
        y = cell[0] + offset[0]
        x = cell[1] + offset[1]
        if y >= 0 and y < maxY and x >= 0 and x < maxX:
            if OFFSET.OPPOSITE[offset] == dirIn:
                if dirInCnt == 3:  # on force un virage car trop longtemps dans la même direction
                    # print("SKIP OPPOSITE")
                    continue
                # print("OPPOSITE")
                voisins.append(((y, x), OFFSET.OPPOSITE[offset], dirInCnt + 1))
            else:
                voisins.append(((y, x), OFFSET.OPPOSITE[offset], 1))
    print("    ->", voisins)
    return voisins


def dijkstraAlgoWithPath(grid: list, destCell: tuple, destCellInDir: tuple) -> list:
    """
    Dijkstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale + le chemin depuis la source
    """
    queue = deque([(destCell, destCellInDir, 0)])
    print("queue", queue, len(queue))
    distance = {(destCell, destCellInDir[2]): (int(grid[destCell[0]][destCell[1]]), [
        (destCell, destCellInDir, 0)])}
    print("distance", distance)
    while queue:
        tCell, tInDir, tInDirCnt = queue.popleft()
        print(Ansi.blue, "@ t", tCell, tInDir, tInDirCnt, Ansi.norm)
        for voisinCell, voisinInDir, voisinInDirCnt in getVoisins(grid, tCell, tInDir, tInDirCnt):
            nouvelle_distance = distance[(tCell, tInDir[2])][0] + \
                int(grid[voisinCell[0]][voisinCell[1]])
            print("  check ", voisinCell, voisinInDir[2], distance[(tCell, tInDir[2])][0], int(
                grid[voisinCell[0]][voisinCell[1]]), nouvelle_distance)
            if (voisinCell, voisinInDir[2]) not in distance or nouvelle_distance < distance[(voisinCell, voisinInDir[2])][0]:
                distance[(voisinCell, voisinInDir[2])] = nouvelle_distance, distance[(tCell, tInDir[2])][1] + \
                    [(voisinCell, voisinInDir, voisinInDirCnt)]
                print("    UPDATE", distance[(voisinCell, voisinInDir[2])])
                queue.append(
                    (voisinCell, voisinInDir, voisinInDirCnt))

    # remove the node itself from the list
    # del distance[destCell]

    return distance


def dijkstraAlgoWithPathB(grid: list, destCell: tuple, destCellInDir: tuple) -> list:
    """
    Dijkstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale + le chemin depuis la source
    """
    queue = deque([(destCell, destCellInDir, 0)])
    print("queue", queue, len(queue))
    distance = {destCell: (int(grid[destCell[0]][destCell[1]]), [
        (destCell, destCellInDir, 0)])}
    print("distance", distance)
    while queue:
        tCell, tInDir, tInDirCnt = queue.popleft()
        if tCell in ((0, 2), (0, 3), (0, 4), (0, 5), (0, 6)):
            print(Ansi.red, tCell)
        print(Ansi.blue, "@ t", tCell, tInDir, tInDirCnt, Ansi.norm)
        for voisinCell, voisinInDir, voisinInDirCnt in getVoisins(grid, tCell, tInDir, tInDirCnt):
            nouvelle_distance = distance[tCell][0] + \
                int(grid[voisinCell[0]][voisinCell[1]])
            print("  check ", voisinCell, voisinInDir[2], distance[tCell][0], int(
                grid[voisinCell[0]][voisinCell[1]]), nouvelle_distance)
            if voisinCell not in distance or nouvelle_distance < distance[voisinCell][0]:
                distance[voisinCell] = nouvelle_distance, distance[tCell][1] + \
                    [(voisinCell, voisinInDir, voisinInDirCnt)]
                print("    UPDATE", distance[voisinCell])
                queue.append(
                    (voisinCell, voisinInDir, voisinInDirCnt))

    # remove the node itself from the list
    # del distance[destCell]

    return distance


def resolve_part1():
    grid = data.grid

    distance = dijkstraAlgoWithPathB(
        grid, (len(grid) - 1, len(grid[0]) - 1), OFFSET.E)
    origin = (0, 0)
    for key, value in distance.items():
        if key[0] == 0 and key[1] == 0:
            print(key, value)
    # """
    print("distance", origin[0], origin[1], "=",
          distance[(origin[0], origin[1])][0])
    for elt in distance[(origin[0], origin[1])][1]:
        match elt[1][2]:
            case "E":
                car = ">"
            case "W":
                car = "<"
            case "N":
                car = "^"
            case "S":
                car = "V"
        grid[elt[0][0]][elt[0][1]] = car
        print(elt[0], elt[1][2], distance[elt[0]][0])

    showGrid(grid)
    # """
    return None


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
# inputFile = "sample2.txt"
inputFile = "sample3.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

"""
print(getVoisins(data.grid, (0, 0), OFFSET.N, 0))
print(getVoisins(data.grid, (1, 1), OFFSET.N, 1))
print(getVoisins(data.grid, (1, 2), OFFSET.W, 3))

exit()
"""

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
