from tools import *

# from matrix2d import *
# from matrix3d import *

from functools import reduce
import itertools

import time

# from collections import deque
import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

import copy

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    history = None


data = Data()


def initData():
    data.line = []
    data.history = []

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        # data.line.append(line)

        # fields = line.split()
        data.history.append(list(map(int, line.split())))

    # print(data.history)


##################
### PROCEDURES ###
##################

def comput(hist: list) -> int:

    # print("###", hist)
    curNext = hist[-1]
    # lastHist = [curNext]
    while sum(hist) != 0:
        tmpHist = []
        for i in range(len(hist)-1):
            curVal = hist[i+1] - hist[i]
            tmpHist.append(curVal)
        # lastHist.append(curVal)
        curNext += curVal
        hist = tmpHist
        # print(curNext, hist, lastHist)
    # print(curNext)
    return (curNext)


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    sumNextOasis = 0
    for oasis in data.history:
        sumNextOasis += comput(oasis)

    return sumNextOasis


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    sumPrevOasis = 0
    for oasis in data.history:
        oasis.reverse()
        sumPrevOasis += comput(oasis)

    return sumPrevOasis


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

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
