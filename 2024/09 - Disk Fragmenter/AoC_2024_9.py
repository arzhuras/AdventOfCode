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
    return


##################
### PROCEDURES ###
##################


def doSplitMap(diskmap):
    splitmap = []

    idNumber = 0
    for blockIdx, blockLen in enumerate(diskmap):
        # print(blockIdx, blockLen)

        if blockIdx % 2 == 0:  # pair
            splitmap.append(["file", int(blockLen), 0, idNumber, int(blockLen)])
            idNumber += 1
            if int(blockLen) == 0:
                print(blockIdx, "FILE ZERO BLOCK", splitmap[-1])
        else:
            splitmap.append(["free", int(blockLen), int(blockLen)])

    # print("SPLITMAP")
    # for eltIdx, elt in enumerate(splitmap):
    #     print(eltIdx, elt)

    return splitmap


def doChecksum(splitmap):
    checksum = 0
    blockPos = 0
    for eltId, elt in enumerate(splitmap):
        # print(eltId, blockPos, elt)
        if elt[1] == elt[2]:  # empty block
            blockPos += elt[1]
            # print("   SKIP BLOCK", eltId, elt[1], blockPos)
            continue

        for blockId in range(3, len(elt), 2):
            for i in range(elt[blockId + 1]):
                if elt[blockId + 1] > 0:
                    tmpsum = blockPos * elt[blockId]
                    checksum += tmpsum
                    blockPos += 1
        if elt[2] > 0:
            blockPos += elt[2]
            # print("   SKIP", elt[2], blockPos)
    return checksum


def resolve_part1():
    ### split map ###
    # 0:"file", 1:fileSize, 2:fileEmptySpace, 3:idNumber1, 4:idCount1
    # 0:"free", 1:freeSize, 2:freeEmptySpace, [3:idNumber1, 4:idCount1 ... idNumberN, idCountN]
    splitmap = doSplitMap(data.rawInput[0])

    # compact star 1
    fileBlockIdx = len(splitmap) - len(splitmap) % 2
    fileBlock = splitmap[fileBlockIdx]
    for freeBlockIdx in range(1, len(splitmap), 2):
        freeBlock = splitmap[freeBlockIdx]
        while freeBlock[2] > 0 and fileBlockIdx >= 0:
            chunkLen = min(freeBlock[2], fileBlock[1] - fileBlock[2])
            # print(f"  fileBlock {fileBlockIdx} {fileBlock} chunk {chunkLen}")
            freeBlock.append(fileBlock[3])
            freeBlock.append(chunkLen)
            freeBlock[2] -= chunkLen
            fileBlock[2] += chunkLen
            fileBlock[4] -= chunkLen

            if fileBlock[4] == 0:  # block vide
                fileBlockIdx -= 2
                fileBlock = splitmap[fileBlockIdx]

            if freeBlockIdx > fileBlockIdx:
                # print("BREAK 1 >", freeBlockIdx, fileBlockIdx)
                break

        if freeBlockIdx > fileBlockIdx:
            # print("BREAK 2 >", freeBlockIdx, fileBlockIdx)
            break

    # for eltIdx, elt in enumerate(splitmap):
    #     print(eltIdx, elt)

    return doChecksum(splitmap)


def resolve_part2():
    ### split map ###
    # 0:"file", 1:fileSize, 2:fileEmptySpace, 3:idNumber1, 4:idCount1
    # 0:"free", 1:freeSize, 2:freeEmptySpace, [3:idNumber1, 4:idCount1 ... idNumberN, idCountN]
    splitmap = doSplitMap(data.rawInput[0])
    print()
    ### compact star 2 ###
    for fileBlockIdx in range(len(splitmap) - len(splitmap) % 2, 0, -2):
        fileBlock = splitmap[fileBlockIdx]
        # print("-> fileBlock", fileBlockIdx, fileBlock)

        freeBlockIdx = 1
        freeBlock = splitmap[freeBlockIdx]
        while freeBlockIdx < fileBlockIdx and freeBlock[2] < fileBlock[1]:
            freeBlockIdx += 2
            if freeBlockIdx > len(splitmap) - 1:
                break
            freeBlock = splitmap[freeBlockIdx]

        if freeBlockIdx < fileBlockIdx:
            freeBlock[2] -= fileBlock[1]
            freeBlock.append(fileBlock[3])
            freeBlock.append(fileBlock[4])

            fileBlock[2] = fileBlock[1]
            fileBlock[4] = 0

    # for eltIdx, elt in enumerate(splitmap):
    #     print(eltIdx, elt)
    # print()

    return doChecksum(splitmap)


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
print(sys.argv[0])
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)
initData()
startTime = time.time()
res1 = resolve_part1()
# res1, res2 = resolve_bothpart()
endTime = time.time()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")

# exit()

### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)
initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
