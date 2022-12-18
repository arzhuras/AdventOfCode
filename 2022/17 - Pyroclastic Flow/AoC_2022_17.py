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
    tallLst = None


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
    data.tetrisFlipV = flipHLst(data.tetris)

    data.stack = [["+"] + ["-"] * 7 + ["+"]]
    data.tall = 0
    data.tallLst = []

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
    # print(f"gazJet: {len(data.line[0])} '{data.line[0]}'")
    print(f"gazJet: {len(data.line[0])}")
    offsetStack = 0
    for rockCount in range(1, MAX_ROCK_COUNT + 1):
        # print(f"## {rockCount} -> {curTetris} tall: {data.tall} ##")
        # complete to 3+4 empty line
        for _ in range(7 - (len(data.stack) + offsetStack - 1 - data.tall)):
            data.stack.append(["|"] + ["."] * 7 + ["|"] + [str(len(data.stack) + offsetStack)])

        # showStack(data.stack)

        # new tetris rock
        curRock = data.tetrisFlipV[curTetris]
        curRockCol = 3

        curStackLine = data.tall - offsetStack + 4
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
        for idxB in range(len(curRock)):
            tmpLst = data.stack[curStackLine]

            for idxA in range(len(curRock[idxB])):
                if tmpLst[curRockCol + idxA] == ".":
                    tmpLst[curRockCol + idxA] = curRock[idxB][idxA]
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
        oldTall = data.tall
        if curStackLine + offsetStack - 1 > data.tall:
            data.tall = curStackLine + offsetStack - 1
        # print(f"## {rockCount} -> {curTetris} tall: {data.tall} curGazJetIdx:{curGazJetIdx} ##")
        data.tallLst.append((rockCount, data.tall, data.tall - oldTall))
        curTetris = (curTetris + 1) % 5

    # print("------------------------3", data.tall)
    # showStack(data.stack)

    """
    data.tallLst = []
    for i in range(4):
        data.tallLst.append((i + 1 + 4, 0, i))
    data.tallLst = [(1, 0, 9), (2, 0, 8), (3, 0, 7), (4, 0, 6)] + data.tallLst + data.tallLst
    """
    # for elt in reversed(data.tallLst):
    # print(elt)

    deltaOffsetLst = []
    deltaCycleLst = []
    for offset in range(50000):
        # print(offset)
        for idxB in range(1, ((len(data.tallLst) - offset) // 2) + 1):
            # print("  ", idxB + 1, "len", idxB)
            for idxA in range(idxB):
                # print("  ", idxA + 1, idxB + idxA + 1, data.tallLst[idxA], data.tallLst[idxB + idxA], end="")
                if data.tallLst[idxA + offset][2] == data.tallLst[idxB + idxA + offset][2]:
                    # print(" True")
                    pass
                else:
                    # print(" False")
                    break
            if data.tallLst[idxA + offset][2] == data.tallLst[idxB + idxA + offset][2]:
                # if data.tallLst[idxA + offset][2] == data.tallLst[idxB + idxA + offset + idxB][2]:
                if idxB > 20:
                    print(
                        "  bingo",
                        offset,
                        data.tallLst[offset],
                        idxB + offset,
                        data.tallLst[idxB + offset],
                        "len",
                        idxB,
                    )
                    for elt in data.tallLst[:offset]:
                        deltaOffsetLst.append(elt[2])
                    for elt in data.tallLst[offset : offset + idxB]:
                        deltaCycleLst.append(elt[2])
                    break
        if len(deltaCycleLst) > 0:
            break

    print("offset", offset, "idxB", idxB)
    # print(len(deltaCycleLst), deltaCycleLst)
    # print(len(deltaOffsetLst), deltaOffsetLst)

    TARGET_ROCK = 2022
    print("##", TARGET_ROCK, "##")
    print("div eucli", TARGET_ROCK // idxB)
    print("modulo", TARGET_ROCK % idxB)
    # print(sum(deltaOffsetLst))
    # print(sum(deltaCycleLst))
    res = (
        sum(deltaOffsetLst)
        + (sum(deltaCycleLst) * (TARGET_ROCK // idxB))
        + sum(deltaCycleLst[: (TARGET_ROCK % idxB) - offset])
    )
    print(f"Résultat pour {TARGET_ROCK}: {res}")

    TARGET_ROCK = 1000000000000
    print("##", TARGET_ROCK, "##")
    print("  div eucli", TARGET_ROCK // idxB)
    print("  modulo", TARGET_ROCK % idxB)
    # print(sum(deltaOffsetLst))
    # print(sum(deltaCycleLst))
    res = (
        sum(deltaOffsetLst)
        + (sum(deltaCycleLst) * (TARGET_ROCK // idxB))
        + sum(deltaCycleLst[: (TARGET_ROCK % idxB) - offset])
    )
    print(f"Résultat pour {TARGET_ROCK}: {res}")

    return res


############
### MAIN ###
############

inputFilename = "sample2.txt"

MAX_ROCK_COUNT = 20
inputFilename = "sample.txt"

# MAX_ROCK_COUNT = 5
MAX_ROCK_COUNT = 20220
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
