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


def resolve_part1():
    diskmap = data.rawInput[0]
    splitmap = []

    # explode
    idNumber = 0
    # print(diskmap)
    for blockIdx, block in enumerate(diskmap):
        # print(blockIdx, block)
        if blockIdx % 2 == 0:  # pair
            splitmap.append(["file", int(block), str(idNumber), int(block)])
            idNumber += 1
        else:
            splitmap.append(["free", int(block)])
    # print(splitmap)

    # compact star 1
    fileBlockIdx = len(splitmap) - len(splitmap) % 2
    fileBlock = splitmap[fileBlockIdx]
    for freeBlockIdx in range(1, len(splitmap), 2):
        freeBlock = splitmap[freeBlockIdx]
        # print("freeBlock", freeBlockIdx, freeBlock)
        while freeBlock[1] > 0 and fileBlockIdx >= 0:
            chunkLen = min(freeBlock[1], fileBlock[1])
            # print(f"  fileBlock {fileBlockIdx} {fileBlock} chunk {chunkLen}")
            freeBlock.append(fileBlock[2])
            freeBlock.append(chunkLen)
            freeBlock[1] -= chunkLen
            fileBlock[1] -= chunkLen
            fileBlock[3] = fileBlock[1]
            # print("  ", freeBlock)
            # print("  ", fileBlock)

            if fileBlock[1] == 0:
                fileBlockIdx -= 2
                fileBlock = splitmap[fileBlockIdx]
        if fileBlockIdx - freeBlockIdx == 1:
            break

    # checksum
    checksum = 0
    fileId = 0
    for elt in splitmap:
        # print(elt)
        for blockId in range(2, len(elt), 2):
            if elt[blockId + 1] == 0:
                break
            for num in range(elt[blockId + 1]):
                tmpsum = fileId * int(elt[blockId])
                checksum += tmpsum
                # print("  ", elt[blockId], elt[blockId + 1], fileId, tmpsum, checksum)
                fileId += 1

    return checksum


def resolve_part2():

    diskmap = data.rawInput[0]
    splitmap = []

    # explode
    idNumber = 0
    # print(diskmap)
    # record splitmap -> file|free, blockSize, block
    for blockIdx, blockLen in enumerate(diskmap):
        # print(blockIdx, block)
        if blockIdx % 2 == 0:  # pair
            splitmap.append(["file", int(blockLen), str(idNumber), int(blockLen)])
            idNumber += 1
        else:
            splitmap.append(["free", int(blockLen)])
    # print(splitmap)

    # compact star 2

    # fileBlockSorted = sorted(s, key = lambda x: (x[1], x[2]))

    for eltIdx, elt in enumerate(splitmap):
        print(eltIdx, elt)

    for fileBlockIdx in range(len(splitmap) - len(splitmap) % 2, 0, -2):
        fileBlock = splitmap[fileBlockIdx]
        print("-> fileBlock", fileBlockIdx, fileBlock)

        # freeBlock = splitmap[freeBlockIdx]
        freeBlockIdx = 1
        freeBlock = splitmap[freeBlockIdx]
        while freeBlock[1] < fileBlock[1]:
            freeBlockIdx += 2
            if freeBlockIdx > len(splitmap) - 1:
                break
            freeBlock = splitmap[freeBlockIdx]
        if freeBlockIdx > len(splitmap) - 1:
            print("   SKIP")
            continue
        print("   freeBlock", freeBlockIdx, freeBlock)

        freeBlock[1] -= fileBlock[1]
        freeBlock.append(fileBlock[2])
        freeBlock.append(fileBlock[3])
        # fileBlock[2] = "."
        fileBlock[1] = 0
        # fileBlock[3] = 0

        # print("  ", freeBlock)
        # print("  ", fileBlock)

        # if fileBlockIdx - freeBlockIdx == 1:
        # break

    for eltIdx, elt in enumerate(splitmap):
        print(eltIdx, elt)
    print()

    # checksum
    checksum = 0
    fileId = 0
    for eltId, elt in enumerate(splitmap):
        print(eltId, elt)
        if eltId % 2 == 0:  # file record
            if elt[1] == 0:
                fileId += elt[3]
                print(fileId)
                continue

            for blockId in range(2, len(elt), 2):
                for _ in range(elt[blockId + 1]):
                    if elt[blockId + 1] > 0:
                        tmpsum = fileId * int(elt[blockId])
                        checksum += tmpsum
                        print(
                            "  ",
                            elt[blockId],
                            elt[blockId + 1],
                            fileId,
                            tmpsum,
                            checksum,
                        )
                    fileId += 1
                    print(fileId)

        if len(elt) == 2:
            fileId += elt[1]
            print(fileId)
            continue

        for blockId in range(2, len(elt), 2):
            for _ in range(elt[blockId + 1]):
                if elt[blockId] != "." and elt[blockId + 1] > 0:
                    tmpsum = fileId * int(elt[blockId])
                    checksum += tmpsum
                    print(
                        "  ", elt[blockId], elt[blockId + 1], fileId, tmpsum, checksum
                    )
                fileId += 1
                print(fileId)

    return checksum


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
# res1, res2 = resolve_bothpart()
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
