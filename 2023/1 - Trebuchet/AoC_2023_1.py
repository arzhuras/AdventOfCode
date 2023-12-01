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

    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    calibrationSum = 0
    for elt in data.line:
        digit1 = None
        digit2 = None
        for car in elt:
            if car > "0" and car <= "9":
                # print(car)
                if digit1 == None:
                    digit1 = car
                else:
                    digit2 = car
        if digit1 == None:
            digit1 = "0"
        if digit2 == None:
            digit2 = digit1
        print(int(digit1 + digit2))
        calibrationSum += int(digit1 + digit2)

    return calibrationSum


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    number = {"one": "1", "two": "2", "three": "3", "four": "4",
              "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    calibrationSum = 0
    for elt in data.line:
        print(elt)
        digit1 = None
        digit2 = None
        carIdx = 0
        while carIdx < len(elt):
            # print(carIdx, elt)
            if elt[carIdx] > "0" and elt[carIdx] <= "9":
                if digit1 == None:
                    digit1 = elt[carIdx]
                else:
                    digit2 = elt[carIdx]
                carIdx += 1
                continue

            for key in number.keys():
                minIdx = -1
                curNum = None
                idx = elt.find(key, carIdx)
                if idx != -1 and idx == carIdx:
                    if minIdx == -1 or idx < minIdx:
                        minIdx = idx
                        curNum = key
                    print("  found", key, minIdx)
                if minIdx != -1:
                    if digit1 == None:
                        digit1 = number[curNum]
                    else:
                        digit2 = number[curNum]
            carIdx += 1
            # print(carIdx, elt)

        if digit1 == None:
            digit1 = "0"
        if digit2 == None:
            digit2 = digit1
        print("->", int(digit1 + digit2))
        calibrationSum += int(digit1 + digit2)

    return calibrationSum


############
### MAIN ###
############
# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"

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

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
