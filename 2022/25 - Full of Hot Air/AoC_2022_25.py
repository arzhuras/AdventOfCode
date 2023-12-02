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

    print("initData:", data.line)


##################
### PROCEDURES ###
##################

snafuDic = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def snafu2dec(snafuVal: str) -> int:
    exposant = len(snafuVal) - 1
    decVal = 0
    for car in snafuVal:
        decVal += snafuDic[car] * (5 ** exposant)
        exposant -= 1
    print(snafuVal, "->", decVal)
    return decVal


def dec2snafu(decVal: int) -> str:
    exposant = 0
    tmpVal = 0  # somme max de tout les digits (exposant) précédent
    while True:
        tmpVal += 2 * (5 ** exposant)
        # print("tmpVal", tmpVal)
        # On a le bon exposant. Il faut trouver le bon facteur: 1 ou 2
        if tmpVal >= abs(decVal):
            factor = 1
            if tmpVal - (5 ** exposant) < abs(decVal):
                factor = 2
            if decVal < 0:  # le facteur est négatif si decVal est négatif
                factor = -factor
            curExpVal = factor * (5 ** exposant)
            break
        exposant += 1
    reminder = decVal - curExpVal
    print(f"[{decVal:5}] exposant= {exposant},  factor= {factor:2} -> {curExpVal:5}, reminder= {reminder}")
    if reminder != 0:
        dec2snafu(reminder)

    return decVal


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    sumDec = 0
    for elt in data.line:
        sumDec += snafu2dec(elt)

    for i in range(10):
        print(f"{i} {5 ** i:<10} {2 * (5 ** i):<10}")

    dec2snafu(2022)
    print()
    dec2snafu(12345)
    snafu2dec("=11-2")
    print()

    # return None
    return dec2snafu(sumDec)


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
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
