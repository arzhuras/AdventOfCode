import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

g_inputLines = []


def readInputFile(argFile=INPUT_FILE_NAME):
    inputLines = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    print(f"  {len(inputLines)} lignes")
    # print(inputLines)
    return inputLines


#############################
### INITIALISATION & DATA ###
#############################

g_data = {}


def initData():
    g_data["grid"] = []
    g_data["heat"] = []
    g_data["last"] = {}

    for line in g_inputLines:
        g_data["grid"].append([int(digit) for digit in line])
        g_data["heat"].append([0] * len(line))

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def getLowPoints():
    grid = g_data["grid"]
    heat = g_data["heat"]
    lowPointsLst = []

    maxLine = len(grid)
    for line in range(len(grid)):
        maxCol = len(grid[line])
        for col in range(len(grid[line])):
            curVal = grid[line][col]
            lowest = True
            if line > 0 and curVal >= grid[line - 1][col]:
                lowest = False
            elif line < maxLine - 1 and curVal >= grid[line + 1][col]:
                lowest = False
            elif col < maxCol - 1 and curVal >= grid[line][col + 1]:
                lowest = False
            elif col > 0 and curVal >= grid[line][col - 1]:
                lowest = False

            if lowest == True:
                lowPointsLst.append([(col, line), curVal])
                heat[line][col] = 1

    return lowPointsLst


def showHeat():
    grid = g_data["grid"]
    heat = g_data["heat"]
    for line in range(len(grid)):
        print(f"{line:2} ", end="")
        for col in range(len(grid[line])):
            if heat[line][col] == 0:
                print(f"{grid[line][col]}", end="")
            elif heat[line][col] == 1:
                print(f"{ANSI_GREEN}{grid[line][col]}{ANSI_NORM}", end="")
            elif heat[line][col] == 2:
                print(f"{ANSI_BLUE}{grid[line][col]}{ANSI_NORM}", end="")
        print()


def scanBasin(col, line, mode="U", depth=0):
    grid = g_data["grid"]
    heat = g_data["heat"]
    last = g_data["last"]

    tab = "  " * depth
    # last = {}

    # print(f"{tab} - scanBasin [{line},{col}] {mode}")

    offset = -1 if mode == "U" else 1

    colStart = col
    while colStart > 0 and grid[line][colStart - 1] != 9:
        colStart -= 1

    col = colStart
    basinSize = 0
    while col < len(grid[line]) and grid[line][col] != 9:
        # print(f"{tab}  grid[{line}][{col}] = {grid[line][col]}")
        # check up or down
        # print(mode, line, len(grid))

        if ((mode == "U" and line > 0) or (mode == "D" and line < len(grid) - 1)) and grid[line + offset][col] != 9:
            if (
                line + offset in last and last[line + offset][0] < col and col < last[line + offset][1]
            ):  # cas des mont au milieu de la zone
                print("#### skip mount in middle: line:", line, "col:", col)
                col += 1
            else:
                resEndCol, _, resBasinSize = scanBasin(col, line + offset, mode, depth + 1)
                while col < resEndCol and grid[line][col] != 9:
                    col += 1
                basinSize += resBasinSize
        else:
            col += 1
    for i in range(colStart, col):
        if heat[line][i] == 0:
            heat[line][i] = 2

    lineSize = col - colStart
    last[line] = (colStart, col)
    # print(last)
    basinSize += lineSize
    # print(
    # f"{tab}  line: {line} {mode} colStart: {colStart}, col: {col}, lineSize: {lineSize},  basinSize: {basinSize}"
    # )

    return col, lineSize, basinSize


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    lowestSum = 0
    for point in getLowPoints():
        lowestSum += point[1] + 1

    showHeat()
    return lowestSum


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    basinSizeLst = []
    lowPonitsLst = getLowPoints()
    for i in range(len(lowPonitsLst)):
        col = lowPonitsLst[i][0][0]
        line = lowPonitsLst[i][0][1]
        # print(f"{ANSI_BLUE}### Scan low point [{line},{col}] ###{ANSI_NORM}")

        basinSize = 0
        # cherche si le basin continue au dessus
        _, _, resBasinSize = scanBasin(col, line, "U")
        basinSize += resBasinSize

        # cherche si le basin continue en dessous
        _, resLineSize, resBasinSize = scanBasin(col, line, "D")
        basinSize += resBasinSize - resLineSize  # enlève la ligne currente compté en double
        basinSizeLst.append(basinSize)
        print(f"Point [{line}][{col}] -> basinSize: {basinSize}")

    produit = 1
    for i in sorted(basinSizeLst, reverse=True)[0:3]:
        print(i)
        produit *= i

    showHeat()
    return produit


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

### PART 2 ###
startTime = time.time()
res = resolve_part2()
# 81770004 too high
# 1055166 too high
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
