import sys
import os
import time
from typing import DefaultDict

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
    g_data["nodes"] = DefaultDict(lambda: [])
    g_data["big"] = DefaultDict(lambda: [])
    g_data["path"] = []

    for line in g_inputLines:
        origin, dest = line.split("-")
        g_data["nodes"][origin].append(dest)
        g_data["nodes"][dest].append(origin)
        g_data["big"][origin] = True if origin.isupper() else False
        g_data["big"][dest] = True if dest.isupper() else False
        # print(origin, origin.isupper(), g_data["big"][origin], dest, dest.isupper(), g_data["big"][dest])

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def scanPath(curNode, curPath=[], allowTwice=False, depth=0):
    tab = "  " * depth
    # print(f"{tab}### {curNode} {curPath} {twice}")

    big = g_data["big"]

    curPath.append(curNode)
    for destNodeId, destNode in enumerate(g_data["nodes"][curNode]):
        if destNode == "end":
            curPath.append("end")
            # print(f"{ANSI_BLUE}{tab}  {curNode} -> {destNode}: PATH COMPLETED {curPath}{ANSI_NORM}")
            g_data["path"].append(curPath.copy())
            curPath.pop()

        elif big[destNode]:
            # print(f"{ANSI_GREEN}{tab}  {curNode} -> {destNode}: SCAN BIG{ANSI_NORM}")
            scanPath(destNode, curPath, allowTwice, depth + 1)

        elif not destNode in curPath:
            # print(f"{ANSI_GREEN}{tab}  {curNode} -> {destNode}: SCAN SMALL FIRST TIME{ANSI_NORM}")
            scanPath(destNode, curPath, allowTwice, depth + 1)

        elif allowTwice and destNode != "start":
            # print(f"{ANSI_RED}{tab}  {curNode} -> {destNode}: SCAN SMALL SECOND TIME{ANSI_NORM}")
            scanPath(destNode, curPath, False, depth + 1)

        else:
            # print(f"{tab}  {curNode} -> {destNode}: SKIP")
            pass

    curPath.pop()


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    scanPath("start")

    return len(g_data["path"])


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    scanPath("start", allowTwice=True)

    return len(g_data["path"])


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile("sample3.txt")
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
