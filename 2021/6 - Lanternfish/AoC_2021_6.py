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
    g_data["cycle"] = [0] * 9

    cycle = g_data["cycle"]

    for timer in g_inputLines[0].split(","):
        cycle[int(timer)] += 1

    print("init:", g_data)


##################
### PROCEDURES ###
##################


def simulate(numberOfDay):
    cycle = g_data["cycle"]

    print(f"Initial day   : {cycle}")
    for day in range(1, numberOfDay + 1):
        spawn = cycle[0]
        for i in range(8):
            cycle[i] = cycle[i + 1]
        cycle[6] += spawn
        cycle[8] = spawn
        # print(f"After {day:2} days : {cycle}")

    return sum(cycle)


def resolve_part1(numberOfDay):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return simulate(numberOfDay)


def resolve_part2(numberOfDay):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return simulate(numberOfDay)


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

initData()

startTime = time.time()
res = resolve_part1(80)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData()

startTime = time.time()
res = resolve_part2(256)
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
