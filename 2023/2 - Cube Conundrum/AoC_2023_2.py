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

    gameDic = None


data = Data()


def initData():
    data.line = []
    data.gameDic = {}

    for line in data.rawInput:
        line = line.replace("Game ", "")
        gameid, gameGrab = line.split(":")
        gameSets = gameGrab.split(";")
        # print(gameid, gameSet)
        setLst = []
        for elt in gameSets:
            setDuo = []
            for duo in elt.split(","):
                a, b = duo.split()
                setDuo.append((int(a), b))
            setLst.append(setDuo)
        data.gameDic[int(gameid)] = setLst

        # print(gameid, setLst)

        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)
    # print(data.gameDic)
    """
    for gameId in data.gameDic.keys():
        print(gameId)
        for gameSet in data.gameDic[gameId]:
            print("  ", end="")
            for duo in gameSet:
                print(duo, end="")
            print()
    """
    # fields = line.split()

    # print("initData:", data.line)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    bagContent = {"red": 12, "green": 13, "blue": 14}
    gameDic = data.gameDic

    validGame = []
    for gameId in gameDic.keys():
        # print(gameId)
        isValid = True
        for gameSet in data.gameDic[gameId]:
            # print("  ", end="")
            for duo in gameSet:
                # print(duo, end="")
                if (duo[0] > bagContent[duo[1]]):
                    # print(Ansi.red, f"  Invalid duo: {duo}", Ansi.norm)
                    isValid = False
                    break
            # print()
            if isValid == False:
                break
        if isValid == True:
            validGame.append(gameId)
    print(validGame)
    return sum(validGame)


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    gameDic = data.gameDic

    gamePower = []
    for gameId in gameDic.keys():
        # print(gameId)

        bagContent = {"red": 0, "green": 0, "blue": 0}
        for gameSet in data.gameDic[gameId]:
            # print("  ", end="")
            for duo in gameSet:
                # print(duo, end="")
                if (duo[0] > bagContent[duo[1]]):
                    bagContent[duo[1]] = duo[0]
            # print()
            tmpPower = 1
        # print(bagContent)
        for key, value in bagContent.items():
            tmpPower *= value
        gamePower.append(tmpPower)
    print("gamePower", gamePower)
    return sum(gamePower)


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
