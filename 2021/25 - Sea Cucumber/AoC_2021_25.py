import sys
import os
import time
import copy

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

ANSI_NORM = "\033[0m"
ANSI_GREY = "\033[30;1m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_YELLOW = "\033[33;1m"
ANSI_BLUE = "\033[34;1m"
ANSI_PURPLE = "\033[35;1m"
ANSI_CYAN = "\033[36;1m"

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
    g_data["seabed"] = []
    seabed = g_data["seabed"]

    for line in g_inputLines:
        seabed.append([elt for elt in line])

    print("initData:", g_data)


##################
### PROCEDURES ###
##################


def showSeabed(seabed):
    for line in range(len(seabed)):
        for col in range(len(seabed[0])):
            print(seabed[line][col], end="")
        print()
    print()


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    step = 0
    seabed = g_data["seabed"]

    width = len(seabed[0])
    heigth = len(seabed)

    print("STEP:", step)
    showSeabed(seabed)
    moveCnt = 1
    while moveCnt > 0:
        step += 1
        moveCnt = 0

        tmpSeabed = copy.deepcopy(seabed)
        for line in range(heigth):
            for col in range(width):
                if seabed[line][col] == ">" and seabed[line][(col + 1) % width] == ".":
                    # print(">", line, col, seabed[line][col], seabed[line][(col + 1) % width])
                    tmpSeabed[line][col] = "."
                    tmpSeabed[line][(col + 1) % width] = ">"
                    moveCnt += 1

        seabed = tmpSeabed
        tmpSeabed = copy.deepcopy(seabed)
        for line in range(heigth):
            for col in range(width):
                if seabed[line][col] == "v" and seabed[(line + 1) % heigth][col] == ".":
                    # print("v", line, col, seabed[line][col], seabed[(line + 1) % heigth][col])
                    tmpSeabed[line][col] = "."
                    tmpSeabed[(line + 1) % heigth][col] = "v"
                    moveCnt += 1

        seabed = tmpSeabed

    print("STEP:", step)
    showSeabed(seabed)

    return step


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return 0


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

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
