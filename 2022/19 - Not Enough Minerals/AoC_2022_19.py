from tools import *

# from matrix2d import *
# from matrix3d import *

import time

# from collections import deque
# import operator

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    bluePrint = None  # Dict list
    robots = None  # dict
    ingredients = None  # Dict

    maxGeode = None  # number of open geode
    receipt = None  # receipt path


data = Data()


def initData():
    data.line = []
    data.bluePrint = []
    data.robots = {}
    data.ingredients = {}
    maxGeode = 0
    receipt = [None] * 24

    tmpDict = {}

    for line in data.rawInput:
        if line == "":
            data.bluePrint.append(tmpDict)
            tmpDict = {}
            continue

        line = line.replace(".", "")
        line = line.replace(":", "")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        line = line.replace("Each", "")
        line = line.replace("robot costs", "")
        line = line.replace("and", "")
        data.line.append(line)

        fields = line.split()
        if fields[0] == "Blueprint":
            continue

        tmpDict[fields[0]] = {}
        if fields[0] not in data.robots:
            data.robots[fields[0]] = 0
            data.ingredients[fields[0]] = 0
        for i in range(1, len(fields[1:]), 2):
            tmpDict[fields[0]][fields[i + 1]] = int(fields[i])
    data.bluePrint.append(tmpDict)
    tmpDict = {}
    data.robots["ore"] = 1

    # print("initData:", data.line)
    for i in range(len(data.bluePrint)):
        print(f"[{i}]")
        bp = data.bluePrint[i]
        for elt in bp.keys():
            print(f"  {elt:8s} -> {bp[elt]}")

    print("robots", data.robots)
    print("ingredients", data.ingredients)


##################
### PROCEDURES ###
##################

MAX_MINUTE = 24


def checkBuildable(ingredient, bp, ingedients):
    print("checkBuildable")


def doReceipt(robots, ingredients, receipt, bpIdx, minute, tab=""):
    print(tab, "== Minute ", minute, "== bp:", bpIdx)

    bp = data.bluePrint[bpIdx]

    # building
    print(tab, "--- check building ---")
    print(tab, bp)
    for ingredient in bp.keys():
        # print(ingredient, bp[ingredient].keys())
        buildable = True
        for elt in bp[ingredient].keys():
            if ingredients[elt] >= bp[ingredient][elt]:
                print(tab, "  ", elt, bp[ingredient][elt], ingredients[elt], "OK")
                pass
            else:
                print(tab, "  ", elt, bp[ingredient][elt], ingredients[elt], "NOP")
                buildable = False
                break
        print()

        # collecting
        print(tab, "--- collecting ---")
        for robot in robots.keys():
            if robots[robot] > 0:
                print(tab, "collecting", robots[robot], robot)
                ingredients[robot] += robots[robot]
        print()

        # build
        print(tab, "--- building ---")
        if buildable == True:
            print(tab, "  -> Build", ingredient)
        print()

        # next minute
        print(tab, "  -> Next minute", minute + 1)
        print()
        if minute >= 3:
            return
        doReceipt(robots, ingredients, receipt, bpIdx, minute + 1, tab="  ")
    print()


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    # for bpIdx in range(len(data.bluePrint)):
    for bpIdx in range(1):
        doReceipt(data.robots, data.ingredients, data.receipt, bpIdx, 1)
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
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
