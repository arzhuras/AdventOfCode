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
    grid = None


data = Data()


def initData():
    data.line = []

    data.grid = []
    # il n'y a qu'une grille dans le fichier
    data.grid = loadMatrix2d(inputFile)[0]

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        # fields = line.split()

    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    grid = data.grid
    # grid[0][0] = "#"

    directions = [OFFSET.NORTH, OFFSET.SOUTH, OFFSET.WEST, OFFSET.EAST]
    for round in range(1, MAX_ROUND+1):
        print(f"{Ansi.blue}### ROUND {round:2} ###{Ansi.norm}")
        extendGrid(grid)
        # showGrid(grid)
        moveProposal = {}
        for y in range(1, len(grid) - 1):
            # print(f"{grid[y]}")
            for x in range(1, len(grid[0]) - 1):
                if grid[y][x] != ".":
                    hasNeighbor = False
                    for offset in OFFSET.AROUND:
                        if grid[y + offset[0]][x + offset[1]] != ".":
                            hasNeighbor = True
                            break
                    if hasNeighbor == False:
                        # print(f"{y},{x} -> NO MOVE - NO NEIGHBOR")
                        continue
                    for dir in directions:
                        # print("dir", dir)
                        hasNeighbor = False
                        for offset in dir:
                            if grid[y + offset[0]][x + offset[1]] != ".":
                                # print(f"  {y},{x} {offset} -> {grid[y + offset[0]][x + offset[1]]}")
                                hasNeighbor = True
                                break
                        if hasNeighbor == False:
                            # print(f"{y},{x} -> MOVE {dir[1][2]}")
                            target = (y + dir[1][0], x + dir[1][1])
                            if target not in moveProposal:
                                moveProposal[target] = [(y, x)]
                            else:
                                moveProposal[target].append((y, x))
                            break
                    if hasNeighbor == True:
                        # print(f"{y},{x} -> NO MOVE : NEIGHBOR ALL AROUND")
                        pass
        # print(moveProposal)
        for key, value in moveProposal.items():
            if len(value) > 1:
                # print(f"{key} {value} -> NO MOVE")
                continue
            # print(f"{value} move to {key}")
            grid[key[0]][key[1]] = '#'
            grid[value[0][0]][value[0][1]] = '.'
        showGrid(grid)
        directions.append(directions.pop(0))
        # print(directions)

    print()
    shrinkGrid(grid)
    showGrid(grid)

    # compte les vides
    emptyCount = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == ".":
                emptyCount += 1

    return emptyCount


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    grid = data.grid

    directions = [OFFSET.NORTH, OFFSET.SOUTH, OFFSET.WEST, OFFSET.EAST]
    round = 1
    while True:
        # print(f"{Ansi.blue}### ROUND {round:2} ###{Ansi.norm}")
        extendGrid(grid)
        # showGrid(grid)
        moveProposal = {}
        for y in range(1, len(grid) - 1):
            # print(f"{grid[y]}")
            for x in range(1, len(grid[0]) - 1):
                if grid[y][x] != ".":
                    hasNeighbor = False
                    for offset in OFFSET.AROUND:
                        if grid[y + offset[0]][x + offset[1]] != ".":
                            hasNeighbor = True
                            break
                    if hasNeighbor == False:
                        # print(f"{y},{x} -> NO MOVE - NO NEIGHBOR")
                        continue
                    for dir in directions:
                        # print("dir", dir)
                        hasNeighbor = False
                        for offset in dir:
                            if grid[y + offset[0]][x + offset[1]] != ".":
                                # print(f"  {y},{x} {offset} -> {grid[y + offset[0]][x + offset[1]]}")
                                hasNeighbor = True
                                break
                        if hasNeighbor == False:
                            # print(f"{y},{x} -> MOVE {dir[1][2]}")
                            target = (y + dir[1][0], x + dir[1][1])
                            if target not in moveProposal:
                                moveProposal[target] = [(y, x)]
                            else:
                                moveProposal[target].append((y, x))
                            break
                    if hasNeighbor == True:
                        # print(f"{y},{x} -> NO MOVE : NEIGHBOR ALL AROUND")
                        pass
        # print(moveProposal)
        moveCount = 0
        for key, value in moveProposal.items():
            if len(value) > 1:
                # print(f"{key} {value} -> NO MOVE")
                continue
            # print(f"{value} move to {key}")
            grid[key[0]][key[1]] = '#'
            grid[value[0][0]][value[0][1]] = '.'
            moveCount += 1
        # showGrid(grid)
        directions.append(directions.pop(0))
        # print(directions)

        if moveCount == 0:
            break
        round += 1

    print()
    print(f"{Ansi.blue}### NO MORE MOVE AT ROUND {round:2} ###{Ansi.norm}")
    shrinkGrid(grid)
    showGrid(grid)

    return round


############
### MAIN ###
############

MAX_ROUND = 10
inputFile = "sample.txt"

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

initData()
res = None

### PART 2 ###

startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
