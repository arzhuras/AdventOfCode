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
    g_data["line"] = []

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1(numberOfDay):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return 0


def resolve_part2(numberOfDay):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return 0


############
### MAIN ###
############

g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1(80)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

### PART 2 ###
startTime = time.time()
res = resolve_part2(256)
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
