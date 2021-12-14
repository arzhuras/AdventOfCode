from collections import defaultdict
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
    g_data["germ"] = ""
    g_data["pair"] = {}
    g_data["elt"] = set()

    g_data["germ"] = g_inputLines[0]
    for line in range(2, len(g_inputLines)):
        a, _, c = g_inputLines[line].split()
        g_data["pair"][a] = c
        g_data["elt"].add(c)

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1(nbStep):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    germ = g_data["germ"]
    pair = g_data["pair"]
    print(f"Template {germ}")
    for step in range(nbStep):
        polymer = ""
        for i in range(len(germ) - 1):
            polymer += germ[i] + pair[germ[i] + germ[i + 1]]
            # print("pair:", germ[i] + germ[i + 1], pair[germ[i] + germ[i + 1]], polymer)
        polymer += germ[i + 1]
        germ = polymer
        # print(f"After step {step + 1}: {polymer}")
        print(f"After step {step + 1}: {len(polymer)}")

    countLst = []
    for elt in g_data["elt"]:
        countLst.append(polymer.count(elt))

    return max(countLst) - min(countLst)


def resolve_part2(nbStep):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    germ = g_data["germ"]
    pair = g_data["pair"]
    print(f"Template {germ}")

    germPairCount = DefaultDict(lambda: 0)
    for i in range(len(germ) - 1):
        germPairCount[germ[i] + germ[i + 1]] += 1

    for step in range(nbStep):
        polymerPairCount = DefaultDict(lambda: 0)
        for germPair in germPairCount:
            # print(germPair, germPair[0] + pair[germPair], pair[germPair] + germPair[1])
            polymerPairCount[germPair[0] + pair[germPair]] += germPairCount[germPair]
            polymerPairCount[pair[germPair] + germPair[1]] += germPairCount[germPair]
        germPairCount = polymerPairCount

        eltCount = defaultdict(lambda: 0)
        for polymerPair in polymerPairCount.keys():
            eltCount[polymerPair[0]] += polymerPairCount[polymerPair]
        eltCount[germ[-1]] += 1
        print(f"After step {step + 1}: {sum(eltCount.values())}")

    countDic = defaultdict(lambda: 0)
    for pair in polymerPairCount:
        countDic[pair[0]] += polymerPairCount[pair]
    countDic[germ[-1]] += 1  # add the last germ

    return max(countDic.values()) - min(countDic.values())


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1(10)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2(40)
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
