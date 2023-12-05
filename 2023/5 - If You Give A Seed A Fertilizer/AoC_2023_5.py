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

    seeds = None
    chainMap = None


data = Data()


def initData():
    data.line = []
    data.chainMap = {}

    curChainName = ""
    line = data.rawInput[0]
    data.seeds = list(map(int, line.split(":")[1].split()))
    print("seeds", data.seeds)
    for line in data.rawInput[1:]:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        # fields = line.split()

        if line == "":
            continue

        if not line[0].isdigit():
            curChainName = line.split()[0].split("-")[2]
            # print("curChainName", curChainName)
            data.chainMap[curChainName] = []
        else:
            data.chainMap[curChainName].append(list(map(int, line.split())))

    # print("initData:", data.line)
    for chainName, chainMap in data.chainMap.items():
        print(f"{chainName}")
        for chain in chainMap:
            print(f"  {chain}")


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    chainNames = ("soil", "fertilizer", "water", "light",
                  "temperature", "humidity", "location")
    locations = []
    for seed in data.seeds:
        curId = seed
        print(Ansi.blue, f"Seed {curId}", Ansi.norm)
        for chainName in chainNames:
            matchFound = False
            for dst, src, span in data.chainMap[chainName]:
                if (curId >= src and curId < src + span):
                    print(
                        f"     src {src} <= {Ansi.green}{curId}{Ansi.norm} < {src + span} ({span}): dst {dst} + delta {curId - src} = {Ansi.green}{dst + (curId - src)}{Ansi.norm}")
                    curId = dst + (curId - src)
                    matchFound = True
                    break
                else:
                    print(
                        f"     src {src} <= {Ansi.red}{curId}{Ansi.norm} < {src + span} ({span})")
            if matchFound == False:
                print(Ansi.yellow, "    Not found", Ansi.norm)
            print(Ansi.green, f"  {curId} {chainName}", Ansi.norm)
        locations.append(curId)
        print()

    print(len(locations), locations)
    return min(locations)


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
