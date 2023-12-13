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
    grids = None


data = Data()


def initData():
    data.fields = []
    data.grids = []

    data.grids = loadMatrix2d(inputFile)
    # showGridLst(data.grids)


##################
### PROCEDURES ###
##################

def checkColEquality(grid, col1, col2):
    for row in range(len(grid)):
        if grid[row][col1] != grid[row][col2]:
            return False
    return True


def checkRowEquality(grid, row1, row2):
    for col in range(len(grid[0])):
        if grid[row1][col] != grid[row2][col]:
            return False
    return True


def checkColSpan(grid, col1, col2):  # col 2 > col 1, col1 et col2 déjà égales
    if (col2 - col1 + 1) % 2 == 1:  # si impair, on skip
        print(Ansi.yellow, "SKIPPED", col1, col2, Ansi.norm)
        return False

    span = int((col2 - col1 + 1) / 2)
    # toutes les colonnes dans le span doivent être identiques
    for colSpan in range(1, span):
        if not checkColEquality(grid, col1 + colSpan, col2 - colSpan):
            return False
    return True


def checkRowSpan(grid, row1, row2):  # row 2 > row 1, row 1 et row 2 déjà égales
    if (row2 - row1 + 1) % 2 == 1:  # si impair, on skip
        print(Ansi.yellow, "SKIPPED", row1, row2, Ansi.norm)
        return False

    span = int((row2 - row1 + 1) / 2)
    # toutes les colonnes dans le span doivent être identiques
    for colSpan in range(1, span):
        if not checkRowEquality(grid, row1 + colSpan, row2 - colSpan):
            print("checkRowSpan", row1, row2, False)
            return False
    return True


def resolve_part1():

    patternNotes = 0
    # hypothèse: un seul axe de symetrie par grid
    for gridIdx, grid in enumerate(data.grids):
        print("->", gridIdx)
        # showGrid(grid)
        # check col reflection
        col = 0  # left sided reflection
        for colReflected in range(col+1, len(grid[0]), 2):
            if checkColEquality(grid, col, colReflected) == True:
                if checkColSpan(grid, col, colReflected) == True:
                    span = int((colReflected - col + 1) / 2)
                    patternNotes += col + span
                    print("LEFT", col, colReflected, span, patternNotes)

        col = len(grid[0])-1  # right sided reflection
        for colReflected in range(col-1, -1, -2):
            if checkColEquality(grid, colReflected, col) == True:
                if checkColSpan(grid, colReflected, col, ) == True:
                    span = int((col - colReflected + 1) / 2)
                    patternNotes += colReflected + span
                    print("RIGHT", colReflected, col, span, patternNotes)

        row = 0  # up sided reflection
        for rowReflected in range(row+1, len(grid), 2):
            if checkRowEquality(grid, row, rowReflected) == True:
                if checkRowSpan(grid, row, rowReflected) == True:
                    span = int((rowReflected - row + 1) / 2)
                    patternNotes += 100 * (row + span)
                    print("UP", row, rowReflected, span, patternNotes)

        row = len(grid)-1  # down sided reflection
        for rowReflected in range(row-1, -1, -2):
            if checkRowEquality(grid, rowReflected, row) == True:
                if checkRowSpan(grid, rowReflected, row) == True:
                    span = int((row - rowReflected + 1) / 2)
                    patternNotes += 100 * (rowReflected + span)
                    print("DOWN", rowReflected, row, span, patternNotes)

        print()

    return patternNotes


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

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
