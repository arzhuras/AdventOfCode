from tools import *
import time
import math
import copy

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
    
    # grid = None
    left = None
    right = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan}
# from matrix3d import *


def initData():
    data.fields = []
    data.left = []
    data.right = []

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        intFields = list(map(int,line.split()))
        data.left.append(intFields[0])
        data.right.append(intFields[1])
        data.fields.append([line.split()])

    #print("fields:", data.fields)
    #print("left:", data.left)
    #print("rigth:", data.right)

    # data.grid = []
    # data.grid = loadMatrix2d(inputFile)[0]
    # showGrid(data.grid)

    # data.grids = []
    # data.grids = loadMatrix2d(inputFile)
    # showGridLst(data.grid)


##################
### PROCEDURES ###
##################


def resolve_part1b():
    distance = []
    left = data.left
    right = data.right
    while len(left) > 0:
        smaller_left_idx = 0
        smaller_left_elt = left[0]
        for idx, elt in enumerate(left):
            if elt < smaller_left_elt:
                smaller_left_idx = idx
                smaller_left_elt = elt
        
        smaller_right_idx = 0
        smaller_right_elt = right[0]
        for idx, elt in enumerate(right):
            if elt < smaller_right_elt:
                smaller_right_idx = idx
                smaller_right_elt = elt

        distance.append(abs(smaller_right_elt - smaller_left_elt))
        left.pop(smaller_left_idx)
        right.pop(smaller_right_idx)
    #print(distance)
    return sum(distance)

def resolve_part1():
    distance = []
    left = sorted(data.left)
    right = sorted(data.right)
    for i in range(len(left)):
        distance.append(abs(right[i] - left[i]))
    #print(distance)
    return sum(distance)


def resolve_part2():
    similarity = []
    left = data.left
    right = data.right

    for left_val in left:
        right_count = 0
        for right_val in right:
            if right_val == left_val:
                right_count += 1
        similarity.append(left_val * right_count)

    #print(similarity)
    return sum(similarity)


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
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
