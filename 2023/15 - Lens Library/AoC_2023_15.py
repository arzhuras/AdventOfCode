import time
import math
import copy

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# from functools import reduce
# import itertools

###  /modules libraries ###
from tools import *
# from matrix2d import *
# from matrix3d import *


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    fields = None

    # grid = None


data = Data()


def initData():
    data.fields = []
    # data.grid = []
    # data.grids = []

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        # intFields = list(map(int,line.split()))
        data.fields = line.split(",")

    # print("fields:", data.fields)

    # data.grid = loadMatrix2d(inputFile)[0]
    # data.grids = loadMatrix2d(inputFile)
    # showGrid(data.grid)

##################
### PROCEDURES ###
##################


def resolve_part1():

    # data.fields = ["HASH"]
    sumValue = 0
    for field in data.fields:
        value = 0

        for car in field:
            value += ord(car)
            value *= 17
            value = value % 256
        sumValue += value
        # print(f"{field:4} -> {value:3} : {sumValue}")

    return sumValue


def hashCalc(value):
    hash = 0
    for car in value:
        hash += ord(car)
        hash *= 17
        hash = hash % 256
    return hash


def resolve_part2():

    # data.fields = ["HASH"]
    sumValue = 0
    hashes = []
    for field in data.fields:
        hash = hashCalc(field)
        hashes.append(hash)
        sumValue += hash
        # print(f"{field:4} -> {hash:3} : {sumValue}")

    # print(hashes)
    boxes = [[] for _ in range(256)]
    for field in data.fields:
        idx = field.find("=")
        if idx > 0:
            label = field[:idx]
            focal = int(field[idx+1:])
            hash = hashCalc(label)
            # print("=", label, focal, hash)

            box = boxes[hash]
            lensPresent = False
            for lens in box:
                if lens[0] == label:
                    lens[1] = focal
                    lensPresent = True
                    break
            if lensPresent == False:
                box.append([label, focal])
        else:
            label = field[:idx]
            focal = -1
            hash = hashCalc(label)
            # print("-", label, hash)

            box = boxes[hash]
            for idx in range(len(box)):
                if box[idx][0] == label:
                    box.pop(idx)
                    break

    # print(boxes)
    sumValue = 0
    for boxIdx in range(len(boxes)):
        box = boxes[boxIdx]
        if len(box) == 0:
            continue
        # print("->", box)
        for idxLens in range(len(box)):
            sumValue += (boxIdx + 1) * (idxLens + 1) * box[idxLens][1]
            # print(boxIdx + 1, idxLens + 1, box[idxLens][1], "->", sumValue)

    return sumValue


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

# exit()

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
