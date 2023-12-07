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

    bids = None
    bids2 = None


data = Data()


def initData():
    data.line = []
    data.bids = {}
    data.bids2 = {}

    for line in data.rawInput:
        data.line.append(line)

        hand, bid = line.split()
        hand = hand.replace("A","E")
        hand = hand.replace("K","D")
        hand = hand.replace("Q","C")
        hand = hand.replace("J","B")
        hand = hand.replace("T","A")
        data.bids[hand] = int(bid)
    
        # On remplace les jokers par des 1 pour la part2
        hand = hand.replace("B","1")
        data.bids2[hand] = int(bid)

    #print(data.bids)
    #print(data.bids2)

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
    for hand in data.bids.keys():
        uniqueCardLst = list(set(hand))
        uniqueCardCnt = len(uniqueCardLst)
        if uniqueCardCnt == 5:
            handsType[HIGH_CARD].append(hand)
        elif uniqueCardCnt == 4:
            handsType[ONE_PAIR].append(hand)
        elif uniqueCardCnt == 3:
            if hand.count(uniqueCardLst[0]) == 2 or hand.count(uniqueCardLst[1]) == 2:
                handsType[TWO_PAIR].append(hand)
            else:
                handsType[THREE_OF_A_KIND].append(hand)
        elif uniqueCardCnt == 2:
            if hand.count(uniqueCardLst[0]) == 1 or hand.count(uniqueCardLst[0]) == 4:
                handsType[FOUR_OF_A_KIND].append(hand)
            else:
                handsType[FULL_HOUSE].append(hand)
        elif uniqueCardCnt == 1:
            handsType[FIVE_OF_A_KIND].append(hand)

    score = 0
    rank = 1
    for hands in handsType:
        hands.sort()
        for hand in hands:
            score += data.bids[hand] * rank
            rank += 1

    return score


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    handsType = [[] for _ in range(7)]
    for hand in data.bids2.keys():

        uniqueCardLst = list(set(hand))
        uniqueCardCnt = len(uniqueCardLst)

        if uniqueCardCnt == 5:
            if hand.count("1") == 1:
                handsType[ONE_PAIR].append(hand) # promote
            else:
                handsType[HIGH_CARD].append(hand)
        elif uniqueCardCnt == 4:
            if hand.count("1") >= 1:
                handsType[THREE_OF_A_KIND].append(hand) # promote
            else:
                handsType[ONE_PAIR].append(hand)
        elif uniqueCardCnt == 3:
            if hand.count(uniqueCardLst[0]) == 2 or hand.count(uniqueCardLst[1]) == 2:
                if hand.count("1") == 1:
                    handsType[FULL_HOUSE].append(hand) # promote
                elif hand.count("1") == 2:
                    handsType[FOUR_OF_A_KIND].append(hand) # promote
                else:
                    handsType[TWO_PAIR].append(hand)
            else:
                if hand.count("1") >= 1:
                    handsType[FOUR_OF_A_KIND].append(hand) # promote
                else:
                    handsType[THREE_OF_A_KIND].append(hand)
        elif uniqueCardCnt == 2:
            if hand.count(uniqueCardLst[0]) == 1 or hand.count(uniqueCardLst[0]) == 4:
                if hand.count("1") >= 1:
                    handsType[FIVE_OF_A_KIND].append(hand) # promote
                else:
                    handsType[FOUR_OF_A_KIND].append(hand)
            else:
                if hand.count("1") >= 1:
                    handsType[FIVE_OF_A_KIND].append(hand) # promote
                else:
                    handsType[FULL_HOUSE].append(hand)
        elif uniqueCardCnt == 1:
            handsType[FIVE_OF_A_KIND].append(hand)

    score = 0
    rank = 1
    for hands in handsType:
        hands.sort()
        for hand in hands:
            score += data.bids2[hand] * rank
            rank += 1

    return score


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

#exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
