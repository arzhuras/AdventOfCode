import copy
import math
import time
from collections import defaultdict
from functools import cache

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

    for line in data.rawInput:
        data.fields = map(int,line.split())

    #print("fields:", data.fields)


##################
### PROCEDURES ###
##################

@cache
def splitStone(stoneVal:int):
    #print("splitStone", stoneVal)
    if stoneVal == 0:
        return [1]
    else:
        tmpStr = str(stoneVal)
        if len(tmpStr) % 2 == 0:
            return [int(tmpStr[: len(tmpStr) // 2]), int(tmpStr[len(tmpStr) // 2 :])]
        else:
            return [stoneVal * 2024]

@cache
def expandStone(stoneVal : int, blink: int): # en conservant les listes intermédiaires
    #print("  " * blink, "expandStone", stoneVal, blink)
    stoneLst = splitStone(stoneVal)
    if blink ==1:
        return stoneLst
    
    if len(stoneLst) == 1:
        return expandStone(stoneLst[0], blink - 1)
    else:
        return expandStone(stoneLst[0], blink - 1) + expandStone(stoneLst[1], blink - 1)


@cache
def expandStone2(stoneVal : int, blink: int): # sans conserver les listes intermédiaires
    #print("  " * blink, "expandStone", stoneVal, blink)
    stoneLst = splitStone(stoneVal)
    if blink ==1:
        #print("-> ", stoneVal, blink, stoneLst)
        return len(stoneLst)
    
    if len(stoneLst) == 1:
        return expandStone2(stoneLst[0], blink - 1)
    else:
        return expandStone2(stoneLst[0], blink - 1) + expandStone2(stoneLst[1], blink - 1)

def resolve_part1():
    BLINK = 25
    stoneCount = 0

    for stoneVal in data.fields:
        stoneCount += len(expandStone(stoneVal, BLINK))

    return stoneCount


def resolve_part2():
    BLINK = 75
    stoneCount = 0

    for stoneVal in data.fields:
        stoneCount += expandStone2(stoneVal, BLINK)

    return stoneCount


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
#inputFile = "sample3.txt"

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
