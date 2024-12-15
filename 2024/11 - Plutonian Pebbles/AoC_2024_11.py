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

    for line in data.rawInput:
        data.fields = line.split()

    print("fields:", data.fields)


##################
### PROCEDURES ###
##################


def update_stones(stoneLst, depth=0):
    tab = "  " * depth
    for stoneIdx, stone in enumerate(stoneLst):
        # print(f"{tab}{stone}")
        if type(stone) == str:
            if stone == "0":
                stoneLst[stoneIdx] = "1"
            elif len(stone) % 2 == 0:
                stoneLst[stoneIdx] = [
                    stone[: len(stone) // 2],
                    str(int(stone[len(stone) // 2 :])),
                ]
            else:
                stoneLst[stoneIdx] = str(int(stoneLst[stoneIdx]) * 2024)
        else:
            update_stones(stone, depth + 1)


def count_stones(stoneLst, depth=0):
    stoneCount = 0
    for stoneIdx, stone in enumerate(stoneLst):
        # print(f"{tab}{stone}")
        if type(stone) == str:
            stoneCount += 1
        else:
            stoneCount += count_stones(stone, depth + 1)
    return stoneCount


def resolve_part1():
    stoneLst = data.fields

    for round in range(25):
        print(round)
        for stoneIdx in range(len(stoneLst)):
            stone = stoneLst[stoneIdx]
            if stone == "0":
                stoneLst[stoneIdx] = "1"
            elif len(stone) % 2 == 0:
                stoneLst[stoneIdx] = stone[: len(stone) // 2]
                stoneLst.append(str(int(stone[len(stone) // 2 :])))
            else:
                stoneLst[stoneIdx] = str(int(stone) * 2024)
    # print(stoneLst)
    stoneCount = count_stones(stoneLst)
    return stoneCount


def resolve_part2a():
    stoneLst = data.fields

    for round in range(25):
        # print(f"{Ansi.blue}{round} {stoneLst}{Ansi.norm}")
        update_stones(stoneLst)
        # print(stoneLst)

    # print(stoneLst)
    stoneCount = count_stones(stoneLst)

    return stoneCount


def update_stones2(stoneBase, rounds, cache, depth=0):
    tab = "  " * depth

    stoneLst = stoneBase

    for round in range(rounds):
        roundOffset = rounds - round - 1  # nombre de round jusqu'a la cible
        for stoneIdx in range(stoneLst):
            stone = stoneLst[stoneIdx]
            if stone in cache:
                if len(cache[stone]) >= roundOffset:
                    stoneLst[stoneIdx] = cache[stone][roundOffset]
            else:
                if stone == "0":
                    stoneLst[stoneIdx] = "1"
                elif len(stone) % 2 == 0:
                    stoneLst[stoneIdx] = stone[: len(stone) // 2]
                    stoneLst.append(str(int(stone[len(stone) // 2 :])))
                else:
                    stoneLst[stoneIdx] = str(int(stoneLst[stoneIdx]) * 2024)

                # print(f"{tab}{stone}")
                if type(stone) == str:
                    if stone in cache:
                        stoneLst[stoneIdx] = cache[stone]
                        continue
                else:
                    update_stones2(stone, depth + 1)
    cache[stone] = []


def resolve_part2():
    stoneLst = data.fields
    cache = defaultdict(lambda: list())

    for stoneIdx, stone in enumerate(stoneLst):
        stoneLst[stoneIdx] = update_stones2(stone, 6, cache)

    return sum(stoneLst)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
inputFile = "sample3.txt"

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
# res1, res2 = resolve_bothpart()
endTime = time.time()

print()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")
exit()

### PART 2 ###
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()

print()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
