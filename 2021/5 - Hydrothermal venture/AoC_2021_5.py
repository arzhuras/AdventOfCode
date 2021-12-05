import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")


INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
# INPUT_URL = "https://adventofcode.com/2021/day/" + str(1) + "/input"


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
    g_data["coord"] = []

    maxX = 0
    maxY = 0
    for line in g_inputLines:
        a, _, b = line.split()
        x1, y1 = [int(i) for i in a.split(",")]
        x2, y2 = [int(i) for i in b.split(",")]

        # g_data["coord"].append([(tuple([int(i) for i in a.split(",")])), tuple([int(i) for i in b.split(",")])])
        g_data["coord"].append([x1, y1, x2, y2])

        if x1 > maxX:
            maxX = x1
        if x2 > maxX:
            maxX = x2
        if y1 > maxY:
            maxY = y1
        if y1 > maxY:
            maxY = y2

    g_data["width"] = (maxX + 1, maxY + 1)
    # print(g_data)


##################
### PROCEDURES ###
##################


def checkOverlap(argCheckDiag):

    maxX = g_data["width"][0]
    maxY = g_data["width"][1]
    # init grid
    grid = []
    for line in range(maxY):
        grid.append([0] * (maxX))

    for coord in g_data["coord"]:
        x1, y1, x2, y2 = coord

        if argCheckDiag == False and x1 != x2 and y1 != y2:  # diagonal check
            continue

        offsetX = 1 if x1 < x2 else -1
        offsetY = 1 if y1 < y2 else -1

        # print("coord:", x1, y1, x2, y2, offsetX, offsetY)
        while True:
            grid[y1][x1] += 1

            if x1 == x2 and y1 == y2:
                break

            if x1 != x2:
                x1 += offsetX
            if y1 != y2:
                y1 += offsetY

    overlapCount = 0
    for line in range(maxY):
        # print(line, grid[line])
        for col in range(maxX):
            if grid[line][col] >= 2:
                overlapCount += 1

    return overlapCount


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return checkOverlap(False)


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return checkOverlap(True)


############
### MAIN ###
############


# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

initData()


startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
