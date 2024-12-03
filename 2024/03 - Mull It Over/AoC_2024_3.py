from tools import *
import time
import math
import copy
import re

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

    # grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan}
# from matrix3d import *


def initData():
    data.fields = []
    data.line = "".join(data.rawInput)


##################
### PROCEDURES ###
##################


def resolve_part1():
    return sum(map(lambda elt: elt[0] * elt[1], [(int(match.group("a")), int(match.group("b"))) for match in re.finditer(r"mul\((?P<a>\d+),(?P<b>\d+)\)",data.line)]))

def resolve_part2():
    flagMulEnabled = True
    mulList = []
    res = re.finditer(r"mul\((?P<a>\d+),(?P<b>\d+)\)|(do\(\))|(don\'t\(\))",data.line)
    for match in res:
        if match.group() == "do()":
            flagMulEnabled = True
        elif match.group() == "don't()":
            flagMulEnabled = False
        else:
            if flagMulEnabled == True:
                mulList.append(int(match.group("a")) * int(match.group("b")))

    return sum(mulList)


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
    f"-> part 1 ({time.time() - startTime:.6f}s): {Ansi.blue}{res}{Ansi.norm}")

#exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.6f}s): {Ansi.blue}{res}{Ansi.norm}")
