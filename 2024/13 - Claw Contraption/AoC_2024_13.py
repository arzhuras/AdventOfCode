import copy
import math
import time
from collections import defaultdict

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
    fields = None
    line = None
    gridLst = None
    grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():
    data.fields = []

    for lineIdx in range(0, len(data.rawInput), 4):
        fields = (
            data.rawInput[lineIdx]
            .replace("Button A: X+", "")
            .replace(" Y+", "")
            .replace(",", " ")
        )
        butA = list(map(int, fields.split()))
        fields = (
            data.rawInput[lineIdx + 1]
            .replace("Button B: X+", "")
            .replace(" Y+", "")
            .replace(",", " ")
        )
        butB = list(map(int, fields.split()))
        fields = (
            data.rawInput[lineIdx + 2]
            .replace("Prize: X=", "")
            .replace(" Y=", "")
            .replace(",", " ")
        )
        prize = list(map(int, fields.split()))
        data.fields.append(butA + butB + prize)

    # print("fields:", data.fields)


##################
### PROCEDURES ###
##################


def foundMinCost(machine):
    minCost = 0
    for countA in range(100):
        countB = 0
        reminderX = machine[4] - (countA * machine[0])
        reminderY = machine[5] - (countA * machine[1])
        if reminderX % machine[2] != 0:
            continue
        if reminderY % machine[3] != 0:
            continue
        countB = reminderX // machine[2]
        if countB != reminderY // machine[3]:
            continue
        curCost = countA * 3 + countB * 1
        # print("  Found ", machine, countA, countB, curCost)
        if minCost == 0:
            minCost = curCost
        if curCost < minCost:
            print(Ansi.red, "GOTCHA", Ansi.norm)
            minCost = curCost
    return minCost, countA, countB


def resolve_part1():
    costLst1 = []
    for machineIdx, machine in enumerate(data.fields[:]):
        # print(machineIdx, machine)
        res1 = foundMinCost(machine)
        costLst1.append(res1[0])

    # print(costLst1)
    return sum(costLst1)


def foundMinCost2(machine):
    cost = 0
    aX, aY, bX, bY, posX, posY = machine

    posX += 10_000_000_000_000
    posY += 10_000_000_000_000
    countA = int(round((posX - ((bX * posY) / bY)) / (aX - ((bX * aY) / bY)), 2))
    countB = int(round((posY - (aY * countA)) / bY, 2))
    if countA * aX + countB * bX == posX and countA * aY + countB * bY == posY:
        cost = int(countA * 3 + countB)

    return cost, countA, countB


def resolve_part2():
    costLst2 = []
    for machineIdx, machine in enumerate(data.fields[:]):
        # print(machineIdx, machine)
        res1 = foundMinCost2(machine)
        costLst2.append(res1[0])

    # print(costLst1)
    return sum(costLst2)


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
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
res1 = resolve_part1()
# res1, res2 = resolve_bothpart()
endTime = time.time()

print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()

print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
