from tools import *

from matrix2d import *
# from matrix3d import *

import time

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

import copy

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    grid = None


data = Data()


def initData():
    data.line = []

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        # fields = line.split()

    data.grid = loadMatrix2d(inputFile)[0]
    extendGrid(data.grid)
    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_both_part():
    print()
    # print(Ansi.red, "### PART 1 ###", Ansi.norm)

    grid = data.grid
    # showGrid(grid)

    partNumbersSum = 0
    starDic = {}
    for y in range(len(grid)):
        # print(f"### {y} ##")
        for x in range(len(grid[y])):
            if grid[y][x].isdigit():
                offsetLst = [OFFSET.N, OFFSET.S]
                # number start
                if not grid[y][x-1].isdigit():
                    numberStart = x
                    symbolCount = 0
                    starCount = 0
                    offsetLst += [OFFSET.NW, OFFSET.W, OFFSET.SW]

                # number end
                if not grid[y][x+1].isdigit():
                    number = "".join(grid[y][numberStart:x+1])
                    offsetLst += [OFFSET.NE, OFFSET.E, OFFSET.SE]

                # check the symbol (part 1) and star (part 2) around
                for offset in offsetLst:
                    if grid[y + offset[0]][x + offset[1]] != ".":
                        symbolCount += 1
                    if grid[y + offset[0]][x + offset[1]] == "*":
                        starCount += 1
                        starCoord = (y + offset[0], x + offset[1])

                # number end
                if not grid[y][x+1].isdigit():
                    if symbolCount > 1:
                        print(Ansi.red, number, "SYMBOL",
                              symbolCount, Ansi.norm)
                    if symbolCount > 0:  # part number found!
                        # print("IN", number, y, numberStart)
                        partNumbersSum += int(number)
                    else:
                        # print("  OUT", number, numberStart)
                        pass

                    if starCount > 1:
                        print(Ansi.red, number, "STAR", starCount, Ansi.norm)
                    if starCount > 0:
                        if starCoord not in starDic:
                            starDic[starCoord] = [number]
                        else:
                            starDic[starCoord].append(number)

    # part 2 count gear ratio
    gearRatiosSum = 0
    for value in starDic.values():
        if len(value) == 2:
            gearRatiosSum += int(value[0]) * int(value[1])

    return partNumbersSum, gearRatiosSum


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    return None


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
res = resolve_both_part()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res[0]}{Ansi.norm}")
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res[1]}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
