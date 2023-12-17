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

# https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/
# @functools.lru_cache(maxsize=None)
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
        # curConditions = conditions.copy()
        # curConditions[idx] = car
        conditions[idx] = car
        res += checkConditions(idx + 1, conditions, groups)
    conditions[idx] = '?'

    return res


def resolve_part2_old():

    # ['?', '?', '?', '.', '#', '#', '#'] [1, 1, 3]

    conditions = ['.', '?', '?', '.', '.', '?',
                  '?', '.', '.', '.', '?', '#', '#', '.']
    groups = [1, 1, 3]

    # ['?', '#', '?', '#', '?', '#', '?', '#', '?', '#', '?', '#', '?', '#', '?'] [1, 3, 1, 6]

    conditions = ['?', '?', '?', '?', '.',
                  '#', '.', '.', '.', '#', '.', '.', '.']
    groups = [4, 1, 1]

    # conditions = ['?', '?', '?', '?', '.', '#', '#', '#',
    # '#', '#', '#', '.', '.', '#', '#', '#', '#', '#', '.']
    # groups = [1, 6, 5]

    conditions = ['?', '#', '#', '#', '?', '?', '?', '?', '?', '?', '?', '?']
    groups = [3, 2, 1]
    print(conditions, groups)
    res = checkConditions(0, conditions, groups)
    print(Ansi.blue, conditions, res, Ansi.norm)

    conditions2 = ['?'] + conditions
    print(conditions2, groups)
    res = checkConditions(0, conditions2, groups)
    print(Ansi.blue, conditions2, res, Ansi.norm)

    conditions2 = conditions + ['?']
    print(conditions2, groups)
    res = checkConditions(0, conditions2, groups)
    print(Ansi.blue, conditions2, res, Ansi.norm)
    # exit()

    resSum = 0
    for conditions, groups in data.springCondition[:10]:
        # print(conditions, groups)
        match conditions[-1]:
            case '.':
                print(".", conditions, groups)
                res1 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res1, Ansi.norm)

                conditions = ['?'] + conditions
                res2 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res2, Ansi.norm)

                res = res1 * (res2 ** 4)
                print(Ansi.yellow, conditions, res, Ansi.norm)

                resSum += res

            case '#':
                print("#", conditions, groups)
                res1 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res1, Ansi.norm)

                conditions = conditions + ['?']
                res2 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res2, Ansi.norm)

                conditions = ['?'] + conditions
                res3 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res3, Ansi.norm)

                conditions = conditions + ['?'] + conditions
                res3 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res3, Ansi.norm)

                res = res1 * (res2 ** 4)
                print(Ansi.green, conditions, res, Ansi.norm)

                resSum += res

            case other:
                print("?", conditions, groups)
                res1 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res1, Ansi.norm)

                conditions = ['?'] + conditions
                res2 = checkConditions(0, conditions, groups)
                print(Ansi.blue, conditions, res2, Ansi.norm)

                res = res1 * (res2 ** 4)
                print(Ansi.yellow, conditions, res, Ansi.norm)

                resSum += res

        print()
    return resSum


def checkConditions2(conditions: list, groups: list, idx=0, curGroup=-1, curGroupLen=0, level=0) -> int:
    tab = "  " * level
    # print(tab, "checkConditions IN", level, conditions,
    # groups, idx, curGroup, curGroupLen)
    res = 0
    while idx < len(conditions):
        match conditions[idx]:
            case "?":
                for car in "#", ".":
                    conditions[idx] = car
                    res += checkConditions2(conditions, groups, idx, curGroup,
                                            curGroupLen, level + 1)
                conditions[idx] = '?'
                # print(level, "res", res)
                return res
            case "#":
                if curGroupLen == 0:
                    curGroup += 1
                    if curGroup >= len(groups):
                        # print("curGroup", curGroup, len(groups))
                        return 0
                curGroupLen += 1
                if curGroupLen > groups[curGroup]:
                    # print("curGroupLen", curGroupLen, groups[curGroup])
                    return 0
                idx += 1
            case ".":
                if curGroupLen > 0:
                    if curGroupLen != groups[curGroup]:
                        # print("curGroupLen2", curGroupLen, groups[curGroup])
                        return 0
                    # dernier groupe, on vérifie qu'il n'y a pas de '#' après
                    if curGroup == len(groups) - 1:
                        idx += 1
                        while idx < len(conditions):
                            if conditions[idx] == "#":
                                # print("optim faux dernier groupe")
                                return 0
                            idx += 1
                        break
                    curGroupLen = 0
                idx += 1

    if curGroup == len(groups) - 1 and (curGroupLen == 0 or curGroupLen == groups[curGroup]):
        # print(tab, "checkConditions OUT", level, conditions,
        # groups, idx, curGroup, curGroupLen)
        return 1
    return 0


def resolve_part1():

    # toto = [1, 2, 3, 4, 5]
    # print(toto[:4-1], toto[:-1]) # [1, 2, 3] [1, 2, 3, 4]

    sumRes = 0
    # data.springCondition = [data.springCondition[0]]
    for conditions, groups in data.springCondition:
        # print(conditions, groups)
        res = checkConditions2(conditions, groups)
        sumRes += res
        print(Ansi.blue, conditions, res, sumRes, Ansi.norm)
    # print()
    return sumRes


def resolve_part2():
    sumRes = 0
    data.springCondition = [data.springCondition[11]]
    i = 1
    for conditions, groups in data.springCondition:
        print(conditions[-1], conditions, groups)
        if conditions[-1] == '.':
            res1 = checkConditions2(conditions, groups)
            print(Ansi.grey, i, conditions, groups, res1, sumRes, Ansi.norm)

            conditions = ['?'] + conditions
            res2 = checkConditions2(conditions, groups)
            print(Ansi.grey, i, conditions, groups, res2, sumRes, Ansi.norm)

            res = res1 * (res2 ** 4)
            print(Ansi.yellow, i, conditions, groups, res, sumRes, Ansi.norm)

            sumRes += res
        else:
            conditions += (["?"] + conditions) * 4
            groups += groups * 4
            # print(conditions, groups)
            res = checkConditions2(conditions, groups)
            sumRes += res
            print(Ansi.blue, i, conditions, groups, res, sumRes, Ansi.norm)
        i += 1
        print()
    return sumRes


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
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
