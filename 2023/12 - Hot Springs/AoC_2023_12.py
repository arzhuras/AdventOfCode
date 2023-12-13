import time
import math
import copy

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# from functools import reduce
import functools
# import itertools

###  /modules libraries ###
from tools import *
# from matrix2d import *
# from matrix3d import *


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    fields = None

    springCondition = None


data = Data()


def initData():
    data.fields = []
    data.springCondition = []

    for line in data.rawInput:
        fields = line.split()
        data.springCondition.append((
            list(fields[0]),
            list(map(int, fields[1].split(",")))))

    # print("data.springCondition:", data.springCondition)


##################
### PROCEDURES ###
##################

@functools.lru_cache(maxsize=None)
def countGroup(conditions):
    idx = 0
    groups = []
    while idx < len(conditions):
        groupLen = 0
        while idx < len(conditions) and conditions[idx] == "#":
            groupLen += 1
            idx += 1
        if groupLen > 0:
            groups.append(groupLen)
        idx += 1
    # print(Ansi.yellow, conditions, groups, Ansi.norm)
    return groups


def checkConditions(idx: int, conditions: list, groups: list) -> int:
    # print(" " * idx, idx, conditions, groups)

    while idx < len(conditions) and conditions[idx] != "?":
        idx += 1

    if idx == len(conditions):
        resGroups = countGroup(conditions)
        if resGroups == groups:
            # print(Ansi.green, "MATCH", Ansi.norm)
            return 1
        return 0

    res = 0
    for car in ".", "#":
        curConditions = conditions.copy()
        curConditions[idx] = car
        res += checkConditions(idx + 1, curConditions, groups)

    return res


def resolve_part1():

    res = 0
    for conditions, groups in data.springCondition:
        res += checkConditions(0, conditions, groups)
    # print(Ansi.blue, conditions, res, Ansi.norm)
    # print()
    return res


def resolve_part2():

    res = 0
    for conditions, groups in data.springCondition:
        # print(conditions, groups)
        conditions += (["?"] + conditions) * 4
        groups += groups * 4
        print(conditions, groups)
        # res += checkConditions(0, conditions, groups)
        # print(Ansi.blue, conditions, res, Ansi.norm)
        print()
    return res


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
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
# res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
