import copy
import math
import time

from tools import *

# import re

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# from functools import reduce
# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    rules = None
    updates = None


data = Data()


def initData():
    data.fields = []
    data.rules = {}
    data.updates = []

    for curLine, line in enumerate(data.rawInput):
        if line == "":
            break
        key, value = map(int, line.split("|"))
        if key not in data.rules:
            data.rules[key] = set()
        data.rules[key].add(value)

    # print(data.rules)

    for curLine, line in enumerate(data.rawInput[curLine + 1 :]):
        data.updates.append(list(map(int, line.split(","))))

    # print(data.updates)


##################
### PROCEDURES ###
##################


def is_valid(curUpdate):  # return the page and conflicting page or -1
    rules = data.rules
    for pageIdx, page in enumerate(curUpdate):
        if page in rules:
            intersect = rules[page] & set(curUpdate[:pageIdx])
            if intersect:
                return page, list(intersect)[0]
    return -1, -1


def resolve_bothpart():
    middle_1 = []
    middle_2 = []
    for updtIdx, curUpdate in enumerate(data.updates):
        page, conflictingPage = is_valid(curUpdate)
        if page == -1:
            middle_1.append(curUpdate[int(len(curUpdate) / 2)])
            # print(updtIdx, curUpdate, "  VALID DIRECT:", middle_1)
            continue
        while page != -1:
            # print(updtIdx, curUpdate, "  INVALID", page, pageConflict, rules[page])
            curUpdate[curUpdate.index(page)] = conflictingPage
            curUpdate[curUpdate.index(conflictingPage)] = page
            page, conflictingPage = is_valid(curUpdate)
        middle_2.append(curUpdate[int(len(curUpdate) / 2)])
        # print(updtIdx, curUpdate, "  VALID:", middle_2)

    return sum(middle_1), sum(middle_2)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.grid = loadMatrix2d(inputFile)

### PART 1 ###
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
# res1 = resolve_part1()
res1, res2 = resolve_bothpart()
endTime = time.time()

print()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

# initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
