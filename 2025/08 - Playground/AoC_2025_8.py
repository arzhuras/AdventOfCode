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
    boxes = None
    gridLst = None
    grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *
# from graph import *


def initData():
    data.boxes = []

    for line in data.rawInput:
        data.boxes.append(list(map(int, line.split(","))))

    # print("lineFields:", data.boxes)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


def resolve_bothpart():
    boxes = data.boxes

    # calcul des distances optimisation sous la diagnonale
    boxDistLst = []
    for boxeIdx, boxe in enumerate(boxes):
        tmpDist = []
        for nextBoxeIdx in range(len(boxes)):
            if nextBoxeIdx < boxeIdx:  # optim sous la diagonale
                tmpDist = 0
                for coor in range(3):
                    tmpDist += (boxe[coor] - boxes[nextBoxeIdx][coor]) ** 2
                # tmpDist = math.sqrt(tmpDist) # pas besoin de la racine carrée pour comparer les distances
                boxDistLst.append(
                    (tmpDist, tuple(boxes[boxeIdx]), tuple(boxes[nextBoxeIdx]))
                )
    boxDistLst.sort(key=lambda elt: elt[0])  # trier par distance croissante

    """
    for idx, elt in enumerate(boxDistLst[:20]):
        print(idx, elt)
    print(len(boxDistLst))
    """

    circuitsDict = []
    boxCircuit = {}

    res1, res2 = 0, 0

    for idx, elt in enumerate(boxDistLst):  # boxDistLst 0=dist, 1=box1, 2=box2
        # print()
        # print(idx, elt[1], elt[2], elt[0])
        if elt[1] not in boxCircuit and elt[2] not in boxCircuit:
            circuitsDict.append([elt[1], elt[2]])
            boxCircuit[elt[1]] = len(circuitsDict) - 1
            boxCircuit[elt[2]] = len(circuitsDict) - 1
            # print(Ansi.green, "new", Ansi.norm, circuitsDict[-1])
        elif elt[1] in boxCircuit and elt[2] in boxCircuit:
            if boxCircuit[elt[1]] == boxCircuit[elt[2]]:
                # print(Ansi.blue, "both already in same circuits", Ansi.norm)
                pass
            else:
                circ1Idx = boxCircuit[elt[1]]
                circ2Idx = boxCircuit[elt[2]]
                # print(Ansi.red, "merge", Ansi.norm, circ1Idx, "and", circ2Idx)
                circuitsDict[circ1Idx] = circuitsDict[circ1Idx] + circuitsDict[circ2Idx]
                for box in circuitsDict[circ2Idx]:
                    boxCircuit[box] = circ1Idx
                circuitsDict[circ2Idx] = []
        elif elt[1] not in boxCircuit:
            circuitsDict[boxCircuit[elt[2]]].append(elt[1])
            boxCircuit[elt[1]] = boxCircuit[elt[2]]
            # print(Ansi.yellow, "add", Ansi.norm, elt[1], boxCircuit[elt[2]], elt[2])
        elif elt[2] not in boxCircuit:
            circuitsDict[boxCircuit[elt[1]]].append(elt[2])
            boxCircuit[elt[2]] = boxCircuit[elt[1]]
            # print(Ansi.yellow, "add ", Ansi.norm, elt[2], boxCircuit[elt[1]], elt[1])

        # check 3 larger circuit at MAX_ROUND-1
        if idx == MAX_ROUND - 1:
            # print()
            circLen = []
            for circuitIdx, circuit in enumerate(circuitsDict):
                circLen.append(len(circuit))
                # print(circuitIdx, len(circuit), circuit)
            circLen.sort(reverse=True)
            res1 = math.prod(circLen[:3])
            print(Ansi.cyan, "res1=", res1, "circLen:", circLen[:3], Ansi.norm)

        """
        print("boxCircuit:", len(boxes), len(boxCircuit), boxCircuit)
        for circuitIdx, circuit in enumerate(circuitsDict):
            print(circuitIdx, len(circuit), circuit)
        """
        # check unique crocuit with ALL boxes
        circuitCount = 0
        for circuit in circuitsDict:
            if len(circuit) > 0:
                circuitCount += 1
        # print("circuitCount:", circuitCount, len(boxCircuit))
        if circuitCount == 1 and len(boxCircuit) == len(
            boxes
        ):  # 1 circuit avec 100% des boxes
            res2 = elt[1][0] * elt[2][0]
            print(Ansi.cyan, "res2=", res2, idx, elt[1], elt[2], Ansi.norm)
            break

    return res1, res2


def resolve_part2():

    return None


############
### MAIN ###
############

inputFile, MAX_ROUND = "sample.txt", 10
inputFile, MAX_ROUND = "input.txt", 1000

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
