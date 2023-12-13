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

def checkColDiff(grid, col1, col2):
    diffCnt = 0
    for row in range(len(grid)):
        if grid[row][col1] != grid[row][col2]:
            diffCnt += 1
    return diffCnt


def checkRowDiff(grid, row1, row2):
    diffCnt = 0
    for col in range(len(grid[0])):
        if grid[row1][col] != grid[row2][col]:
            diffCnt += 1
    return diffCnt


def checkColSpanDiff(grid, col1, col2):  # col 2 > col 1, col1 et col2 déjà égales
    if (col2 - col1 + 1) % 2 == 1:  # si impair, on skip
        return 2

    span = int((col2 - col1 + 1) / 2)
    # toutes les colonnes dans le span doivent être identiques ou avec 1 différence
    diffs = 0
    for colSpan in range(1, span):
        diffs += checkColDiff(grid, col1 + colSpan, col2 - colSpan)
        if diffs > 1:
            return 3
    return diffs


def checkRowSpanDiff(grid, row1, row2):  # row 2 > row 1, row 1 et row 2 déjà égales
    if (row2 - row1 + 1) % 2 == 1:  # si impair, on skip
        return 2

    span = int((row2 - row1 + 1) / 2)
    # toutes les colonnes dans le span doivent être identiques ou avec 1 différence
    diffs = 0
    for rowSpan in range(1, span):
        diffs += checkRowDiff(grid, row1 + rowSpan, row2 - rowSpan)
        if diffs > 1:
            return 3
    return diffs


def resolve():

    normalPatternNotes = 0
    smudgePatternNotes = 0
    # hypothèse: 1 seul axe de symétrie normal et 1 seul smudge par grid
    for gridIdx, grid in enumerate(data.grids):
        print("->", gridIdx)
        # showGrid(grid)
        # check col reflection
        col = 0  # left sided reflection
        for colReflected in range(col+1, len(grid[0]), 2):
            diffs = checkColDiff(grid, col, colReflected)
            if diffs <= 1:
                diffs += checkColSpanDiff(grid, col, colReflected)
                span = int((colReflected - col + 1) / 2)
                match diffs:
                    case 0:
                        normalPatternNotes += col + span
                        print("LEFT", col, colReflected,
                              span, normalPatternNotes)
                    case 1:
                        smudgePatternNotes += col + span
                        print("LEFT SMUDGE", col,
                              colReflected, span, smudgePatternNotes)

        col = len(grid[0])-1  # right sided reflection
        for colReflected in range(col-1, -1, -2):
            diffs = checkColDiff(grid, colReflected, col)
            if diffs <= 1:
                diffs += checkColSpanDiff(grid, colReflected, col)
                span = int((col - colReflected + 1) / 2)
                match diffs:
                    case 0:
                        normalPatternNotes += colReflected + span
                        print("RIGHT", colReflected, col,
                              span, normalPatternNotes)
                    case 1:
                        smudgePatternNotes += colReflected + span
                        print("RIGHT SMUDGE", colReflected,
                              col, span, smudgePatternNotes)

        row = 0  # up sided reflection
        for rowReflected in range(row+1, len(grid), 2):
            diffs = checkRowDiff(grid, row, rowReflected)
            if diffs <= 1:
                diffs += checkRowSpanDiff(grid, row, rowReflected)
                span = int((rowReflected - row + 1) / 2)
                match diffs:
                    case 0:
                        normalPatternNotes += 100 * (row + span)
                        print("UP", row, rowReflected,
                              span, normalPatternNotes)
                    case 1:
                        smudgePatternNotes += 100 * (row + span)
                        print("UP SMUDGE", row, rowReflected,
                              span, smudgePatternNotes)

        row = len(grid)-1  # down sided reflection
        for rowReflected in range(row-1, -1, -2):
            diffs = checkRowDiff(grid, rowReflected, row)
            if diffs <= 1:
                diffs += checkRowSpanDiff(grid, rowReflected, row)
                span = int((row - rowReflected + 1) / 2)
                match diffs:
                    case 0:
                        normalPatternNotes += 100 * (rowReflected + span)
                        print("DOWN", rowReflected, row,
                              span, normalPatternNotes)
                    case 1:
                        smudgePatternNotes += 100 * (rowReflected + span)
                        print("DOWN SMUDGE", rowReflected,
                              row, span, smudgePatternNotes)

        # print()

    return normalPatternNotes, smudgePatternNotes


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
res = resolve()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res[0]}{Ansi.norm}")


### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
# res = resolve()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res[1]}{Ansi.norm}")
