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
    # print("seeds", data.seeds)
    for line in data.rawInput[1:]:
        data.line.append(line)

        if line == "":
            continue

        if not line[0].isdigit():
            curChainName = line.split()[0].split("-")[2]
            data.chainMap[curChainName] = []
        else:
            data.chainMap[curChainName].append(list(map(int, line.split())))

    # print("initData:", data.line)
    # for chainName, chainMap in data.chainMap.items():
        # print(f"{chainName}")
        # for chain in chainMap:
            # print(f"  {chain}")


def initData2():
    data.line = []
    data.chainMap = {}

    curChainName = ""
    line = data.rawInput[0]

    seeds = line.split(":")[1].split()
    data.seeds = [(int(seed), int(span))
                  for seed, span in zip(seeds[0::2], seeds[1::2])]
    # print("seeds", data.seeds)
    for line in data.rawInput[1:]:
        data.line.append(line)

        if line == "":
            continue

        if not line[0].isdigit():
            curChainName = line.split()[0].split("-")[2]
            data.chainMap[curChainName] = []
        else:
            data.chainMap[curChainName].append(list(map(int, line.split())))

    # print("initData:", data.line)
    """
    for chainName, chainMap in data.chainMap.items():
        print(f"{chainName}")
        for chain in chainMap:
            print(f"  {chain}")
    """

##################
### PROCEDURES ###
##################


chainNames = ("soil", "fertilizer", "water", "light",
              "temperature", "humidity", "location")

# chainNames = ("soil", "fertilizer")
# chainNames = ("soil", "fertilizer", "water")
# chainNames = ("soil", "fertilizer", "water", "light")


# arg range: (start , span)
# return: [range overlap, [cut1], [cut2], case_for_debug]


def overlap(range1: tuple, range2: tuple) -> list:
    start1, span1 = range1
    start2, span2 = range2
    if start1 == start2 and span1 == span2:
        return [(start1, span1), [], [], 1]  # 1 et 2 égaux

    # gere l'overlap dans les 2 sens et renvoi le cuts des parties non overlap
    if start1 >= start2 and start1 < start2 + span2:
        if start1 + span1 - 1 < start2 + span2:  # 1 inclus dans 2
            if start1 == start2 and start1 + span1 < start2 + span2:  # limite gauche
                return [(start1, span1), [], [(start1 + span1, start2 + span2 - start1 - span1)], 2]
            elif start1 + span1 == start2 + span2:  # limite droite
                return [(start1, span1), [], [(start2, start1 - start2)], 3]
            else:  # milieux
                return [(start1, span1), [], [(start2, start1 - start2), (start1 + span1, start2 + span2 - start1 - span1)], 4]
        elif start2 < start1:  # debut de 1 dans fin de 2, 2 démarre avant 1
            return [(start1, start2 + span2 - start1), [(start2 + span2, start1 + span1 - start2 - span2)], [(start2, start1 - start2)], 5]

    if start2 >= start1 and start2 < start1 + span1:
        if start2 + span2 - 1 < start1 + span1:  # 2 inclus dans 1
            if start2 == start1 and start2 + span2 < start1 + span1:  # limite gauche
                return [(start2, span2), [(start2 + span2, start1 + span1 - start2 - span2)], [], 6]
            elif start2 + span2 == start1 + span1:  # limite droite
                return [(start2, span2), [(start1, start2 - start1)], [], 7]
            else:  # milieux
                return [(start2, span2), [(start1, start2 - start1), (start2 + span2, start1 + span1 - start2 - span2)], [], 8]
        elif start1 < start2:  # debut de 2 dans fin de 1, 1 démarre avant 2
            return [(start2, start1 + span1 - start2), [(start1, start2 - start1)], [(start1 + span1, start2 + span2 - start1 - span1)], 9]

    return [(-1, 0), [], [], 10]  # no overlap ->


def test_overlap():
    print("7, 15, 7, 15  : 1 et 2 égaux                  ",
          overlap((7, 15), (7, 15)))
    print()

    print("3, 5, 3, 10   : 1 inclus dans 2, limite gauche",
          overlap((3, 5), (3, 10)))
    print("7, 4, 5, 6    : 1 inclus dans 2, limite droite", overlap((7, 4), (5, 6)))
    print("10, 15, 3, 30 : 1 inclus dans 2, milieux      ",
          overlap((10, 15), (3, 30)))
    print("20, 15, 3, 30 : debut de 1 dans fin de 2      ",
          overlap((20, 15), (3, 30)))
    print()

    print("0, 15, 0, 10  : 2 inclus dans 1, limite gauche",
          overlap((0, 15), (0, 10)))
    print("0, 10, 5, 5   : 2 inclus dans 1, limite droite",
          overlap((0, 10), (5, 5)))
    print("0, 50, 10, 30 : 2 inclus dans 1, milieux      ",
          overlap((0, 50), (10, 30)))
    print("2, 15, 3, 30  : debut de 2 dans fin de 1      ",
          overlap((2, 15), (3, 30)))

    print()
    print("7, 15, 30, 8  : pas de overlap                ",
          overlap((7, 15), (30, 8)))


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    locations = []
    for seed in data.seeds:
        curId = seed
        # print(Ansi.blue, f"Seed {curId}", Ansi.norm)
        for chainName in chainNames:
            matchFound = False
            for dst, src, span in data.chainMap[chainName]:
                if (curId >= src and curId < src + span):
                    # print(
                    # f"     src {src} <= {Ansi.green}{curId}{Ansi.norm} < {src + span} ({span}): dst {dst} + delta {curId - src} = {Ansi.green}{dst + (curId - src)}{Ansi.norm}")
                    curId = dst + (curId - src)
                    matchFound = True
                    break
                # else:
                    # print(
                    # f"     src {src} <= {Ansi.red}{curId}{Ansi.norm} < {src + span} ({span})")
            # if matchFound == False:
                # print(Ansi.yellow, "    Not found", Ansi.norm)
            # print(Ansi.green, f"  {curId} {chainName}", Ansi.norm)
        locations.append(curId)
        # print()

    # print(len(locations), locations)
    return min(locations)


def checkchain(seedRange: tuple, chainIdx=0) -> int:
    # print("checkchain", seedRange, chainIdx)
    locations = []

    curSeedsRange = [seedRange]
    curSeedRangeIdx = 0
    while curSeedRangeIdx < len(curSeedsRange):
        curSeed = curSeedsRange[curSeedRangeIdx]
        # print(
        # f"{Ansi.blue}{chainNames[chainIdx]} {curSeed[0]} -> {curSeed[0] + curSeed[1] - 1} ({curSeed[1]}){Ansi.norm}")
        matchFound = False
        for dst, src, span in data.chainMap[chainNames[chainIdx]]:
            resOverlap = overlap(curSeed, (src, span))
            if resOverlap[0][0] != -1:
                matchFound = True
                tmpCurSeed = (dst + (resOverlap[0][0] - src), resOverlap[0][1])
                # print(
                # f"  {src} -> {src+span-1} ({span}) dst {dst} -> {Ansi.green}{resOverlap}{Ansi.norm} MATCH curSeed {tmpCurSeed}")
                curSeedsRange += resOverlap[1]
                # print("curSeedsRange", curSeedsRange,
                # "curSeedRangeIdx", curSeedRangeIdx)

                # on a une location, fin de la recursion
                if chainIdx == len(chainNames) - 1:
                    # print("curSeedsRange", curSeedsRange,"curSeedRangeIdx", curSeedRangeIdx)
                    locations.append(tmpCurSeed[0])
                    # print("gotcha loc 1:", "locations", locations)
                else:  # chain suivante par recursion
                    resCheckChain = checkchain(tmpCurSeed, chainIdx+1)
                    locations.append(resCheckChain)
                break
            # else:
                # print(
                # f"  {src} -> {src+span-1} ({span}) dst {dst} -> {Ansi.red}{resOverlap}{Ansi.norm} NO MATCH")

        if matchFound == False:
            if chainIdx == len(chainNames) - 1:
                # print("curSeedsRange", curSeedsRange,"curSeedRangeIdx", curSeedRangeIdx)
                locations.append(curSeed[0])
                # print("gotcha loc 2:", "locations", locations)
            else:  # chain suivante par recursion
                resCheckChain = checkchain(curSeed, chainIdx+1)
                locations.append(resCheckChain)
        curSeedRangeIdx += 1

    # print("location", len(locations), locations)
    return min(locations)


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    locations = []
    for idx, seedRange in enumerate(data.seeds):
        locations.append(checkchain(seedRange))
        # print(Ansi.yellow, idx, seedRange, locations, Ansi.norm)

    # print(len(locations), locations)
    return min(locations)


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
# inputFile = "sample2.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

# test_overlap()
# exit()

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")


initData2()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
