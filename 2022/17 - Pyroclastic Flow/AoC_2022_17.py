from tools import *
from matrix2d import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None
    stack = None
    tetris = None
    tetrisFlipV = None
    tall = None


data = Data()


def initData():
    data.line = []

    for line in data.rawInput:
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        # fields = line.split()

    data.tetris = loadMatrix2d("tetris.txt")
    data.tetrisFlipV = flipVLst(data.tetris)

    data.stack = [["+"] + ["-"] * 7 + ["+"]]
    data.tall = 0

    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    curTetris = 0
    curGazJetIdx = 0
    gazJetLst = data.line[0]
    # print(f"gazJet: {len(data.line[0])} '{data.line[0]}'")
    for rockCount in range(1, MAX_ROCK_COUNT + 1):
        # print(f"## {rockCount} -> {curTetris} tall: {data.tall} ##")

        # complete to 3+4 empty line
        for _ in range(7 - (len(data.stack) - 1 - data.tall)):
            data.stack.append(["|"] + ["."] * 7 + ["|"] + [str(len(data.stack))])

        # showStack(data.stack)

        # new tetris rock
        curRock = data.tetrisFlipV[curTetris]
        curRockCol = 3

        curStackLine = data.tall + 4
        # print(f"  curStackLine: {curStackLine} before falling")
        while True:

            # manage gaz jet
            if gazJetLst[curGazJetIdx] == ">":
                tmpCol = curRockCol + 1
            else:
                tmpCol = curRockCol - 1

            # check if there is room for sliding
            overlap = isOverlap(data.stack, curStackLine, tmpCol, curRock, ".")
            if not overlap == True:
                curRockCol = tmpCol
            curGazJetIdx = (curGazJetIdx + 1) % len(gazJetLst)
            # print(f"  GAZ: curStackLine: {curStackLine} curRockcol: {curRockCol} after gaz {gazJetLst[curGazJetIdx]} {not overlap}")

            # check if there is room for falling
            overlap = isOverlap(data.stack, curStackLine - 1, curRockCol, curRock, ".")
            # print(f"  FALL: curStackLine: {curStackLine} {curRock[0]} {not overlap}")
            if overlap == True:
                break
            curStackLine -= 1

        # print(f"  curStackLine: {curStackLine} after falling")
        # put tetris at rest
        for i in range(len(curRock)):
            tmpLst = data.stack[curStackLine]

            for j in range(len(curRock[i])):
                if tmpLst[curRockCol + j] == ".":
                    tmpLst[curRockCol + j] = curRock[i][j]
            data.stack[curStackLine] = tmpLst
            curStackLine += 1

        # data.tall += 3
        if curStackLine - 1 > data.tall:
            data.tall = curStackLine - 1
        # print(f"## {rockCount} -> {curTetris} tall: {data.tall} curGazJetIdx:{curGazJetIdx} ##")
        curTetris = (curTetris + 1) % 5

    # showStack(data.stack)

    return data.tall


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    curTetris = 0
    curGazJetIdx = 0
    gazJetLst = data.line[0]
    print(f"gazJet: {len(data.line[0])} '{data.line[0]}'")
    for rockCount in range(1, MAX_ROCK_COUNT + 1):
        # print(f"## {rockCount} -> {curTetris} tall: {data.tall} ##")

        if curTetris == 0:
            print("BINGO CYCLE TETRIS", rockCount, curGazJetIdx)
        if curGazJetIdx == 0:
            print("BINGO CYCLE JET", rockCount)
        if curGazJetIdx == 0 and curTetris == 0:
            print("BINGO CYCLE COMBO", rockCount)

        # complete to 3+4 empty line
        for _ in range(7 - (len(data.stack) - 1 - data.tall)):
            data.stack.append(["|"] + ["."] * 7 + ["|"] + [str(len(data.stack))] + [0])

        # showStack(data.stack)

        # new tetris rock
        curRock = data.tetrisFlipV[curTetris]
        curRockCol = 3

        curStackLine = data.tall + 4
        # print(f"  curStackLine: {curStackLine} before falling")
        while True:

            # manage gaz jet
            if gazJetLst[curGazJetIdx] == ">":
                tmpCol = curRockCol + 1
            else:
                tmpCol = curRockCol - 1

            # check if there is room for sliding
            overlap = isOverlap(data.stack, curStackLine, tmpCol, curRock, ".")
            if not overlap == True:
                curRockCol = tmpCol
            curGazJetIdx = (curGazJetIdx + 1) % len(gazJetLst)
            # print(f"  GAZ: curStackLine: {curStackLine} curRockcol: {curRockCol} after gaz {gazJetLst[curGazJetIdx]} {not overlap}")

            # check if there is room for falling
            overlap = isOverlap(data.stack, curStackLine - 1, curRockCol, curRock, ".")
            # print(f"  FALL: curStackLine: {curStackLine} {curRock[0]} {not overlap}")
            if overlap == True:
                break
            curStackLine -= 1

        # print(f"  curStackLine: {curStackLine} after falling")
        # put tetris at rest
        for i in range(len(curRock)):
            tmpLst = data.stack[curStackLine]

            for j in range(len(curRock[i])):
                if tmpLst[curRockCol + j] == ".":
                    tmpLst[curRockCol + j] = curRock[i][j]
                # if curRock[i][j] != ".":
                # tmpLst[10] += 1
            # test if line is full
            # print(curStackLine, tmpLst)
            # if tmpLst[10] == 7:
            # print("BINGO", curStackLine)

            data.stack[curStackLine] = tmpLst
            curStackLine += 1
        # print()

        # data.tall += 3
        if curStackLine - 1 > data.tall:
            data.tall = curStackLine - 1
        # print(f"## {rockCount} -> {curTetris} tall: {data.tall} curGazJetIdx:{curGazJetIdx} ##")
        curTetris = (curTetris + 1) % 5

    # showStack(data.stack)

    return data.tall


############
### MAIN ###
############

inputFilename = "sample2.txt"

MAX_ROCK_COUNT = 2022
inputFilename = "sample.txt"

# MAX_ROCK_COUNT = 5
# MAX_ROCK_COUNT = 2022
inputFilename = "input.txt"

data.rawInput = readInputFile(inputFilename)

initData()

res = None

### PART 1 ###
startTime = time.time()
# res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
