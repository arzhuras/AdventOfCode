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
    gridLst = None
    grid = None
    patterns = None
    design = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():

    data.patterns = data.rawInput[0].replace(" ", "").split(",")
    data.design = []
    for line in data.rawInput[2:]:
        data.design.append(line)

    print("patterns:", data.patterns)
    print("design:", data.design)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def resolve_bothpart():

    possibleDesign = 0
    for design in data.design:
        print(f"{Ansi.blue}{design}{Ansi.norm}")
        curPos = 0
        while curPos < len(design):
            match = False
            for elt in data.patterns:
                # print(design[curPos : curPos + len(elt)], elt)
                if design[curPos : curPos + len(elt)] == elt:
                    match = True
                    print("  ", elt)
                    break
            if match == True:
                curPos += len(elt)
            else:
                print(f"{Ansi.red}  IMPOSSIBLE{Ansi.norm}")
                break
        if curPos >= len(design):
            possibleDesign += 1
            print(f"{Ansi.green}  MATCH{Ansi.norm}")

    return possibleDesign, None


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

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
initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
