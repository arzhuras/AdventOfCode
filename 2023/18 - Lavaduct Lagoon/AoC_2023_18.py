from matrix2d import *
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
    fields = None

    # grid = None


data = Data()

###  /modules libraries ###
# from matrix3d import *


def initData():
    data.fields = []
    data.fields2 = []

    moveMap = ["R", "D", "L", "U"]

    for line in data.rawInput:
        line = line.replace("(", "")
        line = line.replace(")", "")
        line = line.replace("#", "")
        move, span, color = line.split()
        span = int(span)
        data.fields.append((move, span))

        #part 2
        move2 = moveMap[int(color[-1])]
        span2 = int(color[:-1], base=16)
        data.fields2.append((move2, span2))
        
    print("fields:", data.fields)
    print("fields2:", data.fields2)

##################
### PROCEDURES ###
##################


def resolve_part1():
    width = 0
    maxWidth = 0
    minWidth = 0
    height = 0
    minHeight = 0
    maxHeight = 0

    for move, span in data.fields:
        match move:
            case "D":
                height += span
                if height > maxHeight:
                    maxHeight = height
            case "U":
                height -= span
                if height < minHeight:
                    minHeight = height
            case "R":
                width += span
                if width > maxWidth:
                    maxWidth = width
            case "L":
                width -= span
                if width < minWidth:
                    minWidth = width
    width = maxWidth - minWidth + 1
    height = maxHeight - minHeight + 1
    print("width", width, minWidth, maxWidth)
    print("height", height, minHeight, maxHeight)

    grid = [["."] * width for _ in range(height)]

    y = abs(minHeight)
    x = abs(minWidth)
    sumLava = 0
    for move, span in data.fields:
        sumLava += span
        match move:
            case "D":
                for y in range(y + 1, y + span + 1):
                    grid[y][x] = "#"
            case "U":
                for y in range(y - 1, y - span - 1, -1):
                    grid[y][x] = "#"
            case "R":
                for x in range(x + 1, x + span + 1):
                    grid[y][x] = "#"
            case "L":
                for x in range(x - 1, x - span - 1, -1):
                    grid[y][x] = "#"
    print()
    extendGrid(grid)
    #showGrid(grid)

    # recherche des cases intérieurs/extérieurs
    bag = [(0, 0)]
    maxY = len(grid)
    maxX = len(grid[0])
    while len(bag) > 0:
        curCell = bag.pop()
        grid[curCell[0]][curCell[1]] = ","
        for offset in OFFSET.CROSS:
            newY = curCell[0] + offset[0]
            newX = curCell[1] + offset[1]
            if newY < 0 or newY >= maxY:
                continue
            if newX < 0 or newX >= maxX:
                continue
            if grid[newY][newX] == ".":
                bag.append((curCell[0] + offset[0], curCell[1] + offset[1]))

    # Compte les cases restantes -> zone interne
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == ".":
                grid[y][x] = "#"
                sumLava += 1

    #print()
    #showGrid(grid)

    return sumLava


def resolve_part2():

    fields = data.fields
    # On reporte la première et dernière ligne pour se faciliter la vie après
    fields.insert(0, fields[-1])
    fields.append(fields[1])

    x = 0
    maxWidth = 0
    minWidth = 0
    y = 0
    minHeight = 0
    maxHeight = 0

    cols = [] # (ytop, ybot, x), on ne stocke pas le premier et le dernier élément d'une colonne
    sumLava = 0
    for fieldIdx in range(1, len(fields)-1):
        move, span = fields[fieldIdx]
        print(move, span, "    y", y, "x", x)
        match move:
            case "D":
                cols.append((y+1, y + span-1, x))
                print(cols[-1])
                y += span
                if y > maxHeight:
                    maxHeight = y
            case "U":
                cols.append((y - span + 1, y -1, x))
                print(cols[-1])
                y -= span
                if y < minHeight:
                    minHeight = y
            case "R":
                # on regarde si le bloc est un sommet/creux ou non. Si sommet, on l'ignore
                if (fields[fieldIdx-1][0] == "U" and fields[fieldIdx+1][0] == "D") or (fields[fieldIdx-1][0] == "D" and fields[fieldIdx+1][0] == "U"):
                    print("SKIP")
                else:
                    cols.append((y, y, x))
                    print(cols[-1])
                x += span
                if x > maxWidth:
                    maxWidth = x
            case "L":
                # on regarde si le bloc est un sommet/creux ou non. Si sommet, on l'ignore
                if (fields[fieldIdx-1][0] == "U" and fields[fieldIdx+1][0] == "D") or (fields[fieldIdx-1][0] == "D" and fields[fieldIdx+1][0] == "U"):
                    print("SKIP")
                else:
                    cols.append((y, y, x - span))
                    print(cols[-1])
                x -= span
                if x < minWidth:
                    minWidth = x
        sumLava += span
    x = maxWidth - minWidth + 1
    y = maxHeight - minHeight + 1
    print("width", x, minWidth, maxWidth)
    print("height", y, minHeight, maxHeight)
    print(cols)

    return sumLava


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
#inputFile = "input.txt"

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

#exit()

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
