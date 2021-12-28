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
    g_data["algo"] = [int(elt) for elt in g_inputLines[0].replace(".", "0").replace("#", "1")]
    g_data["image"] = []

    pad = 80
    width = len(g_inputLines[2])

    for _ in range(pad):
        g_data["image"].append([0] * (pad + width + pad))

    for line in range(2, len(g_inputLines)):
        g_data["image"].append(
            [0] * pad + [int(elt) for elt in g_inputLines[line].replace(".", "0").replace("#", "1")] + [0] * pad
        )

    for _ in range(pad):
        g_data["image"].append([0] * (pad + width + pad))

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def showAndSum(image):
    sum = 0
    for line in range(len(image)):
        for col in range(len(image[line])):
            sum += image[line][col]
            print("." if image[line][col] == 0 else "#", end="")
        print()
    return sum


def simulate(maxStep):
    algo = g_data["algo"]
    image = g_data["image"]
    image2 = copy.deepcopy(image)

    height = len(image)
    width = len(image[0])
    print("-> Step 0")
    showAndSum(image)
    print()
    for step in range(maxStep):
        for line in range(height):
            for col in range(width):
                # force margin for infinite border simulation...
                if line == 0 or line == height - 1 or col == 0 or col == width - 1:
                    if algo[0] == 1:
                        image2[line][col] = algo[(step % 2) * 511]
                    continue

                curLine = image[line - 1]
                idx = (curLine[col - 1] << 8) + (curLine[col] << 7) + (curLine[col + 1] << 6)
                curLine = image[line]
                idx += (curLine[col - 1] << 5) + (curLine[col] << 4) + (curLine[col + 1] << 3)
                curLine = image[line + 1]
                idx += (curLine[col - 1] << 2) + (curLine[col] << 1) + (curLine[col + 1] << 0)
                # idx = image[line - 1][col - 1] * 256 + image[line - 1][col] * 128 + image[line - 1][col + 1] * 64
                # idx += image[line][col - 1] * 32 + image[line][col] * 16 + image[line][col + 1] * 8
                # idx += image[line + 1][col - 1] * 4 + image[line + 1][col] * 2 + image[line + 1][col + 1] * 1
                image2[line][col] = algo[idx]
        image = copy.deepcopy(image2)
        # print("-> Step", step + 1)
        # sum = showAndSum(image)
        # print()

    print("-> Step", step + 1)
    sum = showAndSum(image)
    print()

    return sum


def resolve_part1(maxStep):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return simulate(maxStep)


def resolve_part2(maxStep):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return simulate(maxStep)


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

# print(3 << 3)
# exit()
initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1(2)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2(50)
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
