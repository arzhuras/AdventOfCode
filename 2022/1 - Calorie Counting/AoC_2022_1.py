from tools import *
import time

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

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

init_script()

g_data = {}


def initData():
    g_data["line"] = []

    for line in g_inputLines:
        g_data["line"].append(line)

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    curSum = 0
    maxSum = 0
    for line in g_inputLines:
        if line == "":
            if curSum > maxSum:
                maxSum = curSum
            curSum = 0
        else:
            curSum += int(line)

    return maxSum


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    curSum = 0
    sumLst = []
    for line in g_inputLines:
        if line == "":
            sumLst.append(curSum)
            curSum = 0
        else:
            curSum += int(line)
    sumLst.append(curSum)

    # sumLst.sort()

    return sum(sorted(sumLst)[-3:])


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
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

"""
elves = open("toto.txt").read().split("\n\n")
calories = [sum(map(int, elf.split())) for elf in elves]
print(max(calories), sum(sorted(calories)[-3:]))
"""
