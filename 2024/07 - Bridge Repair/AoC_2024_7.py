import copy
import math

# from collections import deque
import operator
import time
from collections import defaultdict

from tools import *

# import re

# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# opFunc = {"+": operator.add, "*": operator.mul}
# from functools import reduce
# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    equations = None
    line = None
    gridLst = None
    grid = None


data = Data()


def initData():
    data.equations = {}

    for line in data.rawInput:
        testValue, numbers = line.split(":")
        data.equations[int(testValue)] = list(map(int, numbers.split()))

    # print("equations:", data.equations)


##################
### PROCEDURES ###
##################


def calc(testValue, numbers, opLst=[]):
    # Combinatoire des opérandes
    if len(opLst) < len(numbers) - 1:
        for operande in "+", "*", "|":
            mode = calc(testValue, numbers, opLst + [operande])
            if mode > 0:
                return mode
        return 0

    # Calcul de l'équation
    # print(opLst)
    mode = 1
    curTestValue = numbers[0]
    for opIdx in range(len(opLst)):
        if opLst[opIdx] == "+":
            curTestValue = curTestValue + numbers[opIdx + 1]
        elif opLst[opIdx] == "*":
            curTestValue = curTestValue * numbers[opIdx + 1]
        elif opLst[opIdx] == "|":
            mode = 2
            curTestValue = int(str(curTestValue) + str(numbers[opIdx + 1]))

        if curTestValue > testValue:
            # print("HIGHER", curTestValue, testValue, numbers, opLst)
            return 0

    if curTestValue == testValue:
        if mode == 1:
            pass
            # print(f"{Ansi.green}-> {testValue} {numbers} {opLst}{Ansi.norm}")
        else:
            pass
            # print(f"{Ansi.yellow}-> {testValue} {numbers} {opLst}{Ansi.norm}")
        return mode

    return 0


def resolve_bothpart():
    sum1 = sum2 = 0
    for testValue, numbers in data.equations.items():
        mode = calc(testValue, numbers)
        if mode > 0:
            if mode == 1:
                sum1 += testValue
            else:
                sum2 += testValue
                # print(
                # f"{Ansi.yellow}-> {testValue} {numbers} mode: {resMode} {resOpLst}{Ansi.norm}"
                # )
        else:
            pass
            # print(f"{Ansi.red}-> {testValue} {numbers}{Ansi.norm}")

    return sum1, sum1 + sum2


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

initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
