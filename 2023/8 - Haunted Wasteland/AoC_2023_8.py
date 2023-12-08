from tools import *

# from matrix2d import *
# from matrix3d import *

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
            # print("->", key, instruct[key])
    print("START KEYS", keys)
    print()

    # for key in instruct.keys():
    # if key[2] == "Z":
    # print("->", key, instruct[key])
    # print()

    # for keyIdx, key in [(0, keys[0])]:
    cycle = []
    for keyIdx, key in enumerate(keys):
        print(key, keyIdx)
        finished = False
        round = 0
        curKey = key
        while not finished:
            # if round > 10000:
            # print("infinite loop")
            # exit()
            for choice in data.path:
                # print(curKey, instruct[curKey], choice)
                choiceIdx = 0
                if choice == "R":
                    choiceIdx = 1

                curKey = instruct[curKey][choiceIdx]
                round += 1
                # print(round, curKey)

            if curKey[2] == "Z":
                print(round, key, instruct[key], data.path[0],
                      curKey, instruct[curKey], choice)
                print()
                cycle.append(round)
                finished = True
            """
            zCnt = 0
            for key in keys:
                if key[2] == "Z":
                    zCnt += 1
                # print(key, zCnt, len(keys))
            if zCnt > 0:
                print(round, keys, zCnt)
            if zCnt == len(keys):
                finished = True
            """
    print(cycle, ppcmMultiple(*cycle))

    return round


def decomp(n):
    L = dict()
    k = 2
    while n != 1:
        exp = 0
        while n % k == 0:
            n = n // k
            exp += 1
        if exp != 0:
            L[k] = exp
        k = k + 1

    return L


def ppcm(a, b):
    Da = decomp(a)
    Db = decomp(b)
    p = 1
    for facteur, exposant in Da.items():
        if facteur in Db:
            exp = max(exposant, Db[facteur])
        else:
            exp = exposant

        p *= facteur**exp

    for facteur, exposant in Db.items():
        if facteur not in Da:
            p *= facteur**exposant

    return p


def ppcmMultiple(*args):
    L = list(args)
    if len(L) == 2:
        return ppcm(L[0], L[1])
    else:
        n = len(L)
        i = 0
        A = []
        while i <= n-2:
            A.append(ppcm(L[i], L[i+1]))
            i += 2
        if n % 2 != 0:
            A.append(L[n-1])

        return ppcmMultiple(*A)

############
### MAIN ###
############


# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
inputFile = "sample3.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
# res = resolve_part1()
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

print(ppcmMultiple(12, 8, 42))
