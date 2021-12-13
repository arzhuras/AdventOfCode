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
    g_data["col"] = []
    g_data["line"] = []
    g_data["split"] = []
    g_data["grid"] = []

    section = 0
    for lineContent in g_inputLines:
        if lineContent == "":
            section += 1
            continue

        if section == 0:
            col, line = lineContent.split(",")
            g_data["col"].append(int(col))
            g_data["line"].append(int(line))
        else:
            lineContent = lineContent.replace("fold along ", "")
            axe, coord = lineContent.split("=")
            g_data["split"].append((axe, int(coord)))

    maxCol = max(g_data["col"])
    maxLine = max(g_data["line"])
    print("width:", maxCol + 1, "heigth:", maxLine + 1)

    for i in range(maxLine + 1):
        g_data["grid"].append(["."] * (maxCol + 1))

    if (maxLine + 1) % 2 == 0:
        g_data["grid"].append(["."] * (maxCol + 1))

    for i in range(len(g_data["col"])):
        # print(g_data["col"][i], g_data["line"][i])
        g_data["grid"][g_data["line"][i]][g_data["col"][i]] = "#"

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def showGrid():
    for lineId, lineContent in enumerate(g_data["grid"]):
        print(f"{lineId:04} ", end="")
        for car in lineContent:
            print(car, end="")
        print()


def foldY(foldLine):
    tmpGrid = []

    grid = g_data["grid"]

    sourceLine = len(grid) - 1
    for line in range(foldLine):
        tmpGrid.append(grid[line])
        for col in range(len(grid[line])):
            if grid[sourceLine][col] == "#":
                tmpGrid[line][col] = "#"
        sourceLine -= 1

    g_data["grid"] = tmpGrid


def foldX(foldCol):
    tmpGrid = []

    grid = g_data["grid"]

    for line in range(len(grid)):
        tmpGrid.append(grid[line][0:foldCol])

    for line in range(len(grid)):
        sourceCol = len(grid[0]) - 1
        for col in range(foldCol):
            if grid[line][sourceCol] == "#":
                tmpGrid[line][col] = "#"
            sourceCol -= 1

    g_data["grid"] = tmpGrid


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    # showGrid()

    for axe in g_data["split"]:
        print(axe)
        if axe[0] == "y":
            foldY(axe[1])
            # showGrid()
        else:
            foldX(axe[1])
            # showGrid()

        break

    dotCount = 0
    for lineContent in g_data["grid"]:
        for car in lineContent:
            if car == "#":
                dotCount += 1

    return dotCount


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    # showGrid()

    for axe in g_data["split"]:
        print(axe)
        if axe[0] == "y":
            foldY(axe[1])
            # showGrid()
        else:
            foldX(axe[1])
            # showGrid()

    dotCount = 0
    for lineContent in g_data["grid"]:
        for car in lineContent:
            if car == "#":
                dotCount += 1

    showGrid()
    return dotCount


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

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
