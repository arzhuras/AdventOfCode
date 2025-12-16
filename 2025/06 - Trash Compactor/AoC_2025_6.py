import copy
import math
import time
from collections import defaultdict

from tools import *

# import re

# from collections import deque

# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

from functools import reduce

# from functools import cache

# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None
    lineFields = None
    operands = None
    operator = None
    operands2 = None
    operator2 = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *
# from graph import *


def initData():
    data.operator = []
    data.operands = []

    for line in data.rawInput:
        if line[0] == "+" or line[0] == "*":
            data.operator = line.split()
        else:
            data.operands.append(list(map(int, line.split())))

    #print("operands:", data.operands)
    #print("operator:", data.operator)

    data.operator2 = []
    data.operands2 = []

    # ajout espaces fin de ligne si besoin
    # data.rawInput[-1] += (len(data.rawInput[0]) - len(data.rawInput[-1])) * " "

    i = len(data.rawInput[0]) - 1
    operands = data.rawInput[:-1]
    operator = data.rawInput[-1]
    tmpOperands = []
    tmpStr = ""
    while i >= 0:
        tmpStr = ""
        for elt in operands:
            if elt[i] != " ":
                tmpStr += elt[i]
        if tmpStr != "":
            tmpOperands.append(int(tmpStr))
        if operator[i] != " ":
            data.operands2.append(tmpOperands)
            tmpOperands = []
        i -= 1

    data.operator2 = line.split()[::-1]
    #print("operands2:", data.operands2)
    #print("operator2:", data.operator2)


##################
### PROCEDURES ###
##################


def resolve_bothpart():

    res = calc(data.operator, data.operands)
    #print("->", res)

    res2 = []
    for idx, op in enumerate(data.operator2):
        if op == "+":
            res2.append(sum(data.operands2[idx]))
        else:
            res2.append(math.prod(data.operands2[idx]))
        #print(f"[{idx:03}] {op} -> {data.operands2[idx]} {res2[-1]}")
    #print("->", res2)

    return sum(res), sum(res2)


def calc(operator, operands):
    res = []
    for idx, op in enumerate(operator):
        if op == "+":
            tmpRes = 0
            for elt in operands:
                tmpRes += elt[idx]
        else:
            tmpRes = 1
            for elt in operands:
                tmpRes *= elt[idx]
        #print(f"[{idx:03}] {op} -> {tmpRes}")
        res.append(tmpRes)
    return res


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.gridLst = loadMatrix2d(inputFile)


### PART 1 ###
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)
initData()
startTime = time.time()
# res1 = resolve_part1()
res1, res2 = resolve_bothpart()
endTime = time.time()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)
# initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
