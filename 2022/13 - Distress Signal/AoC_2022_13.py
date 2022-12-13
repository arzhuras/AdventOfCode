from tools import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################


def readInputFile(argFile=INPUT_FILE_NAME):
    data.rawInput = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            data.rawInput.append(line)
    print(f"  {len(data.rawInput)} lignes")
    # print(inputLines)
    return data.rawInput


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = []


data = Data()


def initData():
    data.line = []

    data.left = []
    data.right = []
    for i in range(0, len(data.rawInput), 3):
        data.left.append(data.rawInput[i])
        data.right.append(data.rawInput[i + 1])

    # print("data.left:", data.left)
    # print("data.right:", data.right)


##################
### PROCEDURES ###
##################


def getNextElt(lstStr, idx):  # forcément une liste avec [ & ]
    # print("getNextElt", lstStr[idx:], idx)
    if idx >= len(lstStr) - 1 or len(lstStr) == 2:  # liste terminée
        # print("  getNextElement: no more element")
        return -1, None

    if idx == 0:
        idx += 1
    startIdx = idx
    if lstStr[idx] == "[":  # it's a sublist
        # scan till the end of the sub list
        depth = 1
        idx += 1
        while idx < len(lstStr) and depth != 0:
            if lstStr[idx] == "[":
                depth += 1
            elif lstStr[idx] == "]":
                depth -= 1
            idx += 1
        idx += 1
        elt = lstStr[startIdx : idx - 1]
        # print("  getNextElement: list", elt, "idx", idx)
        return idx, elt

    # else it's a number
    # print(lstStr[idx:])
    elt = 0
    if lstStr[idx + 1] == "," or lstStr[idx + 1] == "]":
        elt = int(lstStr[idx])
        idx += 2
    else:
        elt = int(lstStr[idx : idx + 2])
        idx += 3

    # print("  getNextElement: number", elt, "idx", idx)
    return idx, elt


def check(a, b, tab=""):
    # print("check", a, b)
    idxA = 0
    idxB = 0
    print(f"{tab}- Compare {a} vs {b}")
    while True:
        idxA, eltA = getNextElt(a, idxA)
        idxB, eltB = getNextElt(b, idxB)
        # print(f"{tab}  nextElt {eltA} vs {eltB} idx: {idxA}, {idxB}")

        if eltA == None and eltB == None:
            print(f"{tab}  -> End of the list: continue")
            return "continue"

        if eltA == None and eltB != None:
            print(f"{tab}  -> a shorter than b: right order")
            return "right"

        if eltA != None and eltB == None:
            print(f"{tab}  -> a longer than b: not right order")
            return "not right"

        if isinstance(eltA, int) and isinstance(eltB, int):
            # print(f"{tab}  '{eltA}' vs '{eltB}' idxA: {idxA} idxB: {idxB} ")
            print(f"{tab}  - Compare {eltA} vs {eltB}")
            if eltA < eltB:
                print(f"{tab}  -> a < b: right order")
                return "right"
            elif eltA > eltB:
                print(f"{tab}  -> a > b: not right order")
                return "not right"
            else:
                # print(f"{tab}  -> a = b: continue")
                ret = "continue"
                pass
        elif isinstance(eltA, str) and isinstance(eltB, int):
            ret = check(eltA, "[" + str(eltB) + "]", tab + "  ")
        elif isinstance(eltA, int) and isinstance(eltB, str):
            ret = check("[" + str(eltA) + "]", eltB, tab + "  ")
        else:
            ret = check(eltA, eltB, tab + "  ")

        # subsequent check False
        if ret == "right":
            print(f"{tab}  ret right")
            return "right"
        elif ret == "not right":
            print(f"{tab}  ret not right")
            return "not right"

        # else "continue"


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    validPairs = []
    for i in range(len(data.left)):
        print(f"== Pair {i+1} ==")
        valid = check(data.left[i], data.right[i])
        print(valid)
        if valid == "right":
            validPairs.append(i + 1)
        print()

    print("validPairs:", validPairs)
    res = sum(validPairs)

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    packets = []
    for line in data.rawInput:
        if len(line) > 0:
            line = line.replace("[", "")
            line = line.replace("]", "")
            tmpStr = ""
            for field in line.split(","):
                field = "0" + field
                tmpStr += field[-2:]
            packets.append(tmpStr)
            # print(line)
    packets.append("02")
    packets.append("06")
    packets.sort()
    # for elt in packets:
    # print(elt)
    print("[[2]]", packets.index("02") + 1)
    print("[[6]]", packets.index("06") + 1)
    res = (packets.index("02") + 1) * (packets.index("06") + 1)
    return res


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# 371 low

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# 16999 low
# 32116 high
