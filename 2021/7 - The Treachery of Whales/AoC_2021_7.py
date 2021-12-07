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
    g_data["pos"] = [int(pos) for pos in g_inputLines[0].split(",")]
    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def compute(fuelMode):
    minPos = min(g_data["pos"])
    maxPos = max(g_data["pos"])
    print("minPos:", minPos, "maxPos", maxPos)

    targetPosSumLst = [0] * (maxPos + 1)
    for targetPos in range(minPos, maxPos + 1):
        targetPosSum = 0
        for pos in g_data["pos"]:
            n = abs(pos - targetPos)
            if fuelMode == 1:
                targetPosSum += n
            else:  # fuelMode 2
                targetPosSum += int(n * (n + 1) / 2)
        targetPosSumLst[targetPos] = targetPosSum

    # print(targetPosSumLst)
    bestSum = targetPosSumLst[minPos]
    bestSumPos = minPos
    for i in range(minPos + 1, maxPos + 1):
        if targetPosSumLst[i] < bestSum:
            bestSum = targetPosSumLst[i]
            bestSumPos = i

    print("bestSumPos:", bestSumPos, "bestSum:", bestSum)
    return bestSum


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return compute(1)


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return compute(2)


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
