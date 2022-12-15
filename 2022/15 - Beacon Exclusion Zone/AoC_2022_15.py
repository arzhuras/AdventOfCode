from tools import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################


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
        man = abs(sX - bX) + abs(sY - bY)
        data.sensors.append(((sX, sY), (bX, bY), man))

        data.line.append(line)

    # print("initData:", data.line)
    print("sensors:", data.sensors)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    for elt in data.sensors:
        print("##", elt, "##")
        sX, sY = elt[0]
        bX, bY = elt[1]
        man = elt[2]

        for scanLen in range(1, man + 1):
            # above and below
            for y in sY - scanLen, sY + scanLen:
                if y not in data.scanLine:
                    data.scanLine[y] = []
                data.scanLine[y].append((sX - y, sX + y, elt[0], man))
                print("  ", scanLen, y, data.scanLine[y][-1])

        # same line
        y = sY
        if y not in data.scanLine:
            data.scanLine[y] = []
        data.scanLine[y].append((sX - y, sX + y, elt[0], man))
        print("  ", scanLen, y, data.scanLine[y][-1])

        print(data.scanLine[10])
        print()

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    return res


############
### MAIN ###
############

readInputFile("sample.txt")
# readInputFile("sample2.txt")
# readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
