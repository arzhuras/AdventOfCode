from tools import *

# from matrix2d import *
# from matrix3d import *

import math
import time

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

import copy

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    time = None
    dist = None


data = Data()


def initData():
    data.line = []

    data.time = list(map(int, data.rawInput[0].split(":")[1].split()))
    data.dist = list(map(int, data.rawInput[1].split(":")[1].split()))


def initData2():
    data.line = []

    data.time = list(
        map(int, data.rawInput[0].replace(" ", "").split(":")[1].split()))
    data.dist = list(
        map(int, data.rawInput[1].replace(" ", "").split(":")[1].split()))


##################
### PROCEDURES ###
##################

def checkRaceRun(time, dist):
    # print(time, dist)
    betterDistCount = 0
    for charge in range(time+1):
        myDist = (time - charge) * charge
        if myDist > dist:
            betterDistCount += 1

    # print("betterDistCount", betterDistCount)
    return betterDistCount


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    raceRecord = []
    for time, dist in zip(data.time, data.dist):
        checkRaceRun(time, dist)
        raceRecord.append(checkRaceRun(time, dist))
    print("raceRecord", raceRecord)

    return math.prod(raceRecord)


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    time = data.time[0]
    dist = data.dist[0]

    return checkRaceRun(time, dist)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData2()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
