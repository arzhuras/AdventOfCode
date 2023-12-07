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

    hands = None


data = Data()


def initData():
    data.line = []
    data.hands = {}

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        hand, bid = line.split()
        data.hands[hand] = bid

    print(data.hands)
    # print("initData:", data.line)


##################
### PROCEDURES ###
##################

HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
FULL_HOUSE = 4
FOUR_OF_A_KIND = 5
FIVE_OF_A_KIND = 6


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    handsType = [[] for _ in range(7)]
    for hand in data.hands.keys():
        uniqueCard = set(hand)
        uniqueCardLen = len(uniqueCard)
        print(uniqueCard.pop())

        if uniqueCardLen == 5:
            handsType[HIGH_CARD].append(hand)
        elif uniqueCardLen == 4:
            handsType[ONE_PAIR].append(hand)
        elif uniqueCardLen == 3:
            card = uniqueCard.pop()
            if card == 3:
                handsType[THREE_OF_A_KIND].append(hand)
            elif card == 2:
                handsType[TWO_PAIR].append(hand)
            else:
                card = uniqueCard.pop()
                if card == 2:
                    handsType[TWO_PAIR].append(hand)
                else:
                    handsType[THREE_OF_A_KIND].append(hand)
        elif uniqueCardLen == 2:
            card = uniqueCard.pop()
            if card == 1:
                handsType[FOUR_OF_A_KIND].append(hand)
            elif card == 4:
                handsType[FOUR_OF_A_KIND].append(hand)
            else:
                handsType[FULL_HOUSE].append(hand)
        elif uniqueCardLen == 1:
            handsType[FIVE_OF_A_KIND].append(hand)

    print(handsType)
    return None


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
