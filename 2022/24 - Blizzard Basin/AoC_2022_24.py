from tools import *

from matrix2d import *
# from matrix3d import *

import time

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

import copy

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    grid = []
    blizUP = []
    blizDOWN = []
    blizLEFT = []
    blizRIGHT = []


data = Data()


def initData():
    data.line = []

    # il n'y a qu'une grille dans le fichier
    data.grid = loadMatrix2d(inputFile)[0]
    grid = data.grid
    showGrid(grid)

    # initialisation des blizzards
    data.blizUP = [[] for _ in range(len(grid[0]))]
    data.blizDOWN = [[] for _ in range(len(grid[0]))]
    data.blizLEFT = [[] for _ in range(len(grid))]
    data.blizLEFT = [[] for _ in range(len(grid))]

    for y in range(len(grid)):
        for x in range(len(grid[0])):

            # print(grid[y][x])
            if grid[y][x] == "^":
                print(f"{y},{x}: {grid[y][x]}")
                data.blizUP[x].append(y)
            elif grid[y][x] == "v":
                print(f"{y},{x}: {grid[y][x]}")
                data.blizDOWN[x].append(y)
            elif grid[y][x] == "<":
                print(f"{y},{x}: {grid[y][x]}")
                data.blizLEFT[y].append(x)
            elif grid[y][x] == ">":
                print(f"{y},{x}: {grid[y][x]}")
                data.blizLEFT[y].append(x)

    print("UP", data.blizUP)
    print("DOWN", data.blizDOWN)
    print("LEFT", data.blizLEFT)
    print("LEFT", data.blizLEFT)
    # print("initData:", data.line)


##################
### PROCEDURES ###
##################

def moveBliz():
    minX = 1
    maxX = len(data.blizLEFT) - 2
    minY = 1
    maxY = len(data.blizUP) - 2
    for y in range(len(data.grid)):
        if len(data.blizRIGHT[y]) == 0:
            continue
        for elt in range(len(data.blizRIGHT[y])):
            if data.blizRIGHT[y][elt] == maxX:
                data.blizRIGHT[y][elt] = minX
            else:
                data.blizRIGHT[y][elt] += 1

    for y in range(len(data.grid)):
        if len(data.blizLEFT[y]) == 0:
            continue
        for elt in range(len(data.blizLEFT[y])):
            if data.blizLEFT[y][elt] == 1:
                data.blizLEFT[y][elt] = maxX
            else:
                data.blizLEFT[y][elt] -= 1
    print(data.blizRIGHT)
    print(data.blizLEFT)


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    grid = data.grid
    showGrid(grid)
    for round in range(10):
        print(f"{Ansi.blue} ### ROUND {round:2} ###{Ansi.norm}")
        moveBliz()
        showGrid(grid)

    return None


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
