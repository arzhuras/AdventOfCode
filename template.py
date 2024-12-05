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
    fields = None
    line = None
    grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():
    data.fields = []

    # data.line = "".join(data.rawInput)

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        # intFields = list(map(int,line.split()))
        data.fields.append([line.split()])

    print("fields:", data.fields)

    # data.grid = []
    # data.grid = loadMatrix2d(inputFile)[0]
    # showGrid(data.grid)

    # data.grids = []
    # data.grids = loadMatrix2d(inputFile)
    # showGridLst(data.grid)

    # REGEXP https://pynative.com/python-regex-findall-finditer/
    # line = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    # res = re.finditer(r"mul\((?P<a>\d+),(?P<b>\d+)\)|(do\(\))|(don\'t\(\))",data.line)
    # for match in res:
    # print(match)
    # print(match.group())
    # print(match.group(1))
    # print(match.group(2))
    # print(match.group("a"))
    # print(match.group("b"))


##################
### PROCEDURES ###
##################


def resolve_part1():
    # grid = data.grid

    return None


def resolve_part2():

    return None


def resolve_bothpart():

    return None, None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.grid = loadMatrix2d(inputFile)


### PART 1 ###
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
res1 = resolve_part1()
# res1,res2 = resolve_bothpart()
endTime = time.time()

print()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
