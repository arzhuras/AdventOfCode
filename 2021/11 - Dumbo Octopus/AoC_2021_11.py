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

    for line in g_inputLines:
        g_data["grid"].append([int(energy) for energy in line])

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def showGrid(step):
    grid = g_data["grid"]
    print("-> step", step)
    for line in range(len(grid)):
        for col in range(len(grid[line])):
            if grid[line][col] == 0:
                print(f"{ANSI_BLUE}{grid[line][col]:3}{ANSI_NORM}", end="")
            else:
                print(f"{grid[line][col]:3}", end="")
        print()


def computeStep():
    ADJ_OFFSET = [
        (-1, -1),
        (-1, 0),
        (-1, +1),
        (0, -1),
        (0, +1),
        (+1, -1),
        (+1, 0),
        (+1, +1),
    ]  # (line, col)

    grid = g_data["grid"]

    # incremente l'energie de tous les octopus
    for line in range(len(grid)):
        for col in range(len(grid[line])):
            grid[line][col] += 1

    # flash
    stepFlashCount = 0
    while True:
        curFlashCount = 0
        for line in range(len(grid)):
            for col in range(len(grid[line])):
                if grid[line][col] > 9:  # FLASH
                    curFlashCount += 1
                    grid[line][col] = 0

                    # propagate adjacent
                    for adj in ADJ_OFFSET:
                        lineAdj = line + adj[0]
                        colAdj = col + adj[1]
                        if lineAdj < 0 or lineAdj >= len(grid) or colAdj < 0 or colAdj >= len(grid[line]):  # skip
                            continue
                        if grid[lineAdj][colAdj] > 0:
                            grid[lineAdj][colAdj] += 1

        stepFlashCount += curFlashCount

        if curFlashCount == 0:
            break

    return stepFlashCount


def resolve_part1(nbStep):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    showGrid(0)
    print()

    totalFlashCount = 0
    for step in range(1, nbStep + 1):
        curFlashCount = computeStep()
        totalFlashCount += curFlashCount

        if (step) % 10 == 0:
            showGrid(step)
            print(f"totalFlashCount: {totalFlashCount} curFlashCount: {curFlashCount}")
            print()

    return totalFlashCount


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    step = 0
    while True:
        step += 1
        stepFlashCount = computeStep()

        if stepFlashCount == 100:
            showGrid(step)
            print()
            break

    return step


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1(100)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
