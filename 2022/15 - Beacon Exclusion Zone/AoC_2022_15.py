from tools import *
import time
from collections import deque
import operator

#########################
### COMMON PROCEDURES ###
#########################

INPUT_FILE_NAME = "input.txt"


def readInputFile(argFile=INPUT_FILE_NAME):
    data.rawInput = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            data.rawInput.append(line)
    print(f"  {len(data.rawInput)} lignes")
    # print(inputLines)
    return data.rawInput


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = []
    line = []
    sensors = []
    scanLine = {}


data = Data()


def initData():
    data.line = []
    data.sensors = []
    data.scanLine = {}

    for line in data.rawInput:
        line = line.replace(":", "")
        line = line.replace(",", "")
        fields = line.split("=")
        sX = int(fields[1].split()[0])
        sY = int(fields[2].split()[0])
        bX = int(fields[3].split()[0])
        bY = int(fields[4].split()[0])
        manhattan = abs(sX - bX) + abs(sY - bY)
        data.sensors.append(((sX, sY), (bX, bY), manhattan))

        data.line.append(line)

    # print("initData:", data.line)
    print("sensors:", data.sensors)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    for elt in data.sensors:
        print("##", elt, "##")
        sX, sY = elt[0]
        manhattan = elt[2]

        for offset in range(manhattan + 1):
            if sY + offset not in data.scanLine:
                data.scanLine[sY + offset] = []
            radius = manhattan - offset
            data.scanLine[sY + offset].append((sX - radius, sX + radius, elt[0], manhattan))
            # print(sY + offset, data.scanLine[sY + offset])
            if offset > 0:
                if sY - offset not in data.scanLine:
                    data.scanLine[sY - offset] = []
                data.scanLine[sY - offset].append((sX - radius, sX + radius, elt[0], manhattan))
                # print(sY - offset, data.scanLine[sY - offset])

    # print(7, data.scanLine[7])
    # print(10, data.scanLine[10])
    tmpLst = sorted(data.scanLine[ROW], key=operator.itemgetter(0, 1))
    print(tmpLst)
    rangeSize = 0
    rangeStart, rangeEnd = tmpLst[0][0], tmpLst[0][1]
    for i in range(1, len(tmpLst)):
        print(tmpLst[i][0], tmpLst[i][1])

        if tmpLst[i][0] > rangeEnd:  # nouvelle range
            rangeSize += rangeEnd - rangeStart
            rangeStart, rangeEnd = tmpLst[i][0], tmpLst[i][1]
            print(Ansi.red, "new", Ansi.norm, rangeStart, rangeEnd, rangeSize, tmpLst[i])
        else:  # overlap
            if tmpLst[i][1] > rangeEnd:
                rangeEnd = tmpLst[i][1]
                print("overlap", rangeStart, rangeEnd, rangeSize)
            else:
                print("skip", rangeStart, rangeEnd, rangeSize)
                pass
    rangeSize += rangeEnd - rangeStart

    return rangeSize


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    for j in range(LIMIT + 1):
        tmpLst = sorted(data.scanLine[j], key=operator.itemgetter(0, 1))
        # print(j, tmpLst)
        rangeStart, rangeEnd = tmpLst[0][0], tmpLst[0][1]
        for i in range(1, len(tmpLst)):
            # print(tmpLst[i][0], tmpLst[i][1])

            if tmpLst[i][0] > rangeEnd + 1:  # nouvelle range
                print(Ansi.red, "BINGO", Ansi.norm, rangeEnd + 1, j)
                return (rangeEnd + 1) * 400000 + j
            else:  # overlap
                if tmpLst[i][1] > rangeEnd:
                    rangeEnd = tmpLst[i][1]
                    # print("overlap", rangeStart, rangeEnd)
                else:
                    # print("skip", rangeStart, rangeEnd)
                    pass
        # print()

    return None


############
### MAIN ###
############

fileName = "sample2.txt"

ROW = 10
LIMIT = 20
fileName = "sample.txt"

# ROW = 2000000
# LIMIT = 400000
# fileName = "input.txt"


readInputFile(fileName)

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
