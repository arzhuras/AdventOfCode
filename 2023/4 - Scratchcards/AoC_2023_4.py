from tools import *

# from matrix2d import *
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

    winings = None
    draws = None


data = Data()


def initData():
    data.line = []

    data.winings = []
    data.draws = []
    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)
        wining, draw = line.split(":")[1].split("|")

        data.winings.append(list(map(int, wining.split())))
        data.draws.append(list(map(int, draw.split())))

    print("wining", data.winings)
    print("draw", data.draws)

    # fields = line.split()

    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    winSum = 0
    for idx, draw in enumerate(data.draws):
        expo = 0
        # print(draw)
        for elt in draw:
            wining = data.winings[idx]
            if elt in wining:
                expo += 1
        winSum += int(2 ** (expo - 1))
    return winSum


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    winCountList = []
    winCountList = [0 for _ in range(len(data.draws))]
    print(len(data.draws), winCountList)
    for idx, draw in enumerate(data.draws):
        winCount = 0
        # print(draw)
        for elt in draw:
            wining = data.winings[idx]
            if elt in wining:
                winCount += 1
        # print(idx, winCountList[idx])
        winCountList[idx] = winCount

    print("wincountList", winCountList)
    cardCountList = [1 for _ in range(len(winCountList))]
    for idx, winCount in enumerate(winCountList):
        if winCount > 0:
            for i in range(idx + 1, idx + winCount + 1):
                cardCountList[i] += cardCountList[idx]
            print(idx, winCount, cardCountList)

    print("cardCount", cardCountList)
    return sum(cardCountList)


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
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
