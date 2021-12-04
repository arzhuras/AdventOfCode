import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
# INPUT_URL = "https://adventofcode.com/2021/day/" + str(1) + "/input"


g_inputLines = []
g_data = {}


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


def initData():
    g_data["raw"] = [int(field) for field in g_inputLines[0].split(",")]

    curLine = 2
    g_data["grid"] = []
    while curLine < len(g_inputLines):
        grid = []
        for j in range(5):
            grid.append([int(field) for field in g_inputLines[curLine + j].split()])
        g_data["grid"].append(grid)
        curLine += 6

    # print(g_data)


def isWin(grid, raw):
    for line in range(5):
        for col in range(5):
            if grid[line][col] == raw:
                grid[line][col] = -1
                # print(raw, gridId, grid)
            # print(sum(grid[line]), grid[line])
            if sum(grid[line]) == -5 or sum([grid[i][col] for i in range(5)]) == -5:
                grid[0][0] = -2  # mark as already won
                return True
    return False


def scanGrid():
    winGridLst = []
    for raw in g_data["raw"]:
        for gridId in range(len(g_data["grid"])):
            grid = g_data["grid"][gridId]
            if grid[0][0] == -2:  # skip grid already won
                continue

            res = isWin(grid, raw)
            if res == True:
                winGridLst.append([gridId, raw, sumUnmarked(grid)])
                print("GOTCHA -", "gridId:", gridId, "winGridLst[-1]:", winGridLst[-1])
    return winGridLst


def sumUnmarked(grid):
    score = 0
    for line in grid:
        for elt in line:
            if elt > -1:
                score += elt
    return score


def resolve_part1(winGrid):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    print("first win grid:", winGrid[0])
    print(g_data["grid"][winGrid[0]])
    print("raw:", winGrid[1], "unmarked sum:", winGrid[2])

    return winGrid[1] * winGrid[2]


def resolve_part2(winGrid):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    print("last win grid:", winGrid[0])
    print(g_data["grid"][winGrid[0]])
    print("raw:", winGrid[1], "unmarked sum:", winGrid[2])

    return winGrid[1] * winGrid[2]


# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

initData()

startTime = time.time()
winGridLst = scanGrid()  # winGrid: id, raw, unmarked sum
print()
print(f"-> scan grid ({time.time() - startTime:.3f}s)")

startTime = time.time()
res = resolve_part1(winGridLst[0])
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
# 64124 too high

startTime = time.time()
res = resolve_part2(winGridLst[-1])
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
