from tools import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################


def readInputFile(argFile=INPUT_FILE_NAME):
    data.rawInput = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            data.rawInput.append(line)
    print(f"  {len(data.rawInput)} lignes")
    # print(inputLines)
    return data.rawInput


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = []
    line = []
    valves = {}


data = Data()


def initData():
    data.line = []

    for line in data.rawInput:
        line = line.replace(",", "")
        line = line.replace(";", "")
        line = line.replace("=", " ")
        data.line.append(line)

        fields = line.split()
        data.valves[fields[1]] = [int(fields[5]), fields[10:], False]

    # print("initData:", data.line)
    print("valves:", data.valves)


##################
### PROCEDURES ###
##################

MAX_TIME = 30


def checkValve(valve, elapsedtime, tab=""):
    # print(f"{tab}-> {valve} {elapsedtime} {data.valves[valve][0]} {data.valves[valve][1]} {data.valves[valve][2]}")

    curReleaseOn = 0
    curReleaseOff = 0

    # skip this valves and go for next
    if elapsedtime < MAX_TIME and data.valves[valve][2] == False:
        for next in data.valves[valve][1]:
            curReleaseOff = checkValve(next, elapsedtime + 1, tab + " ")

    # open this valves if possible and go for next
    if data.valves[valve][0] > 0 and data.valves[valve][2] == False:
        data.valves[valve][2] == True
        curReleaseOn = data.valves[valve][0] * (MAX_TIME - elapsedtime)
        elapsedtime += 1
        if elapsedtime < MAX_TIME:
            for next in data.valves[valve][1]:
                curReleaseOn = curReleaseOn + checkValve(next, elapsedtime + 1, tab + " ")

    if curReleaseOn > curReleaseOff:
        # print(f"{tab}  OPEN {curReleaseOn}")
        return curReleaseOn
    else:  # keep it closed!
        # print(f"{tab}  CLOSED {curReleaseOff}")
        data.valves[valve][2] == False
        return curReleaseOff


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    checkValve("AA", 1)

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    return res


############
### MAIN ###
############

readInputFile("sample.txt")
# readInputFile("sample2.txt")
# readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
