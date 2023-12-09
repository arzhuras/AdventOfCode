import time
import math
import copy

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

###  \modules libraries ###
from tools import *
# from matrix2d import *
# from matrix3d import *

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    path = ""
    instruct = None


data = Data()


def initData():
    data.line = []
    data.instruct = {}

    data.path = data.rawInput[0].strip()
    for line in data.rawInput[2:]:
        line = line.replace("(", "")
        line = line.replace(",", "")
        line = line.replace(")", "")
        line = line.replace("=", " ")

        key, left, right = line.split()
        data.instruct[key] = (left, right)

    # print("data.path", data.path)
    # print("data.instruct", data.instruct)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    instruct = data.instruct
    key = "AAA"
    round = 0
    finished = False
    while not finished:
        for choice in data.path:
            # print(key, choice)
            choiceIdx = 0
            if choice == "R":
                choiceIdx = 1

            key = instruct[key][choiceIdx]
            round += 1
            # print(round, keys)

        if key == "ZZZ":
            finished = True

    return round


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    instruct = data.instruct
    keys = []
    for key in instruct.keys():
        if key[2] == "A":
            keys.append(key)
    print("START KEYS", keys)
    print()

    cycle = []
    for key in keys:
        finished = False
        round = 0
        curKey = key
        while not finished:
            for choice in data.path:
                choiceIdx = 0
                if choice == "R":
                    choiceIdx = 1

                curKey = instruct[curKey][choiceIdx]
                round += 1

            if curKey[2] == "Z":
                print(round, len(data.path), round/len(data.path), "start: ", key, instruct[key], data.path[0],
                      "exit: ", curKey, instruct[curKey], choice)
                cycle.append(round)
                finished = True

    return math.lcm(*cycle)

############
### MAIN ###
############


# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
#inputFile = "sample3.txt"

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

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
