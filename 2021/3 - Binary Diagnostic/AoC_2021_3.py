import sys
import os

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
# INPUT_URL = "https://adventofcode.com/2021/day/" + str(1) + "/input"


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


g_inputLines = []


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    gamma = 0
    epsilon = 0

    nbOne = [0] * len(g_inputLines[0])
    nbZero = [0] * len(g_inputLines[0])
    # print(nbOne, nbZero, len(g_inputLines[0]))

    for line in g_inputLines:
        for i in range(len(line)):
            if line[i] == "1":
                nbOne[i] += 1
            else:
                nbZero[i] += 1
    print(nbOne, nbZero, len(g_inputLines[0]))

    gammaStr = ""
    epsilonStr = ""
    for i in range(len(line)):
        if nbOne[i] > nbZero[i]:
            gammaStr = gammaStr + "1"
            epsilonStr = epsilonStr + "0"
            # print(f"gamma: {i} {gamma}")
        else:
            epsilonStr = epsilonStr + "1"
            gammaStr = gammaStr + "0"
            # print(f"epsilon: {i} {epsilon}")

    print(gammaStr, epsilonStr)
    gamma = int(gammaStr, 2)
    epsilon = int(epsilonStr, 2)

    return gamma * epsilon


def compute(argLst, crit1, crit2):
    curLst = argLst.copy()
    curLstTmp = []

    for i in range(len(argLst[0])):
        if len(curLst) == 1:
            break

        # compute number of 1 and 0 par colonne
        nbOne = 0
        nbZero = 0
        for line in curLst:
            if line[i] == "1":
                nbOne += 1
            else:
                nbZero += 1

        # filter lines
        for str in curLst:
            if nbOne >= nbZero and str[i] == crit1:
                curLstTmp.append(str)
            if nbOne < nbZero and str[i] == crit2:
                curLstTmp.append(str)

        curLst = curLstTmp.copy()
        curLstTmp = []
        # print(i, curLst)

    return curLst[0]


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    oxygen = int(compute(g_inputLines, "1", "0"), 2)
    print("oxygen:", oxygen)
    co2 = int(compute(g_inputLines, "0", "1"), 2)
    print("co2   :", co2)

    return oxygen * co2


# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

res = resolve_part1()
print()
print(f"-> part 1 : {ANSI_BLUE}{res}{ANSI_NORM}")

res = resolve_part2()
print()
print(f"-> part 2 : {ANSI_BLUE}{res}{ANSI_NORM}")
