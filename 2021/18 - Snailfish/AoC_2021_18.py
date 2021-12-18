import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

g_inputLines = []


def readInputFile(argFile=INPUT_FILE_NAME):
    inputLines = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    print(f"  {len(inputLines)} lignes")
    # print(inputLines)
    return inputLines


#############################
### INITIALISATION & DATA ###
#############################

g_data = {}


def initData():
    g_data["line"] = []

    for line in g_inputLines:
        g_data["line"].append(line)

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def searchExplode(snailfishNumber):
    depth = 0
    res = False
    for posStart, elt in enumerate(snailfishNumber):
        # calcul la profondeur
        if elt == "[":
            depth += 1
        elif elt == "]":
            depth -= 1
        else:
            continue

        if depth < 5:
            continue

        # Isole la paire de profondeur 5
        posEnd = posStart
        while snailfishNumber[posEnd] != "]":
            posEnd += 1
        eltLeft, eltRight = snailfishNumber[posStart + 1 : posEnd].split(",")
        eltLeft = int(eltLeft)
        eltRight = int(eltRight)

        # searchLeft
        posStartLeft = -1
        idx = posStart - 1
        posEndLeft = -1
        valLeft = 0

        while idx >= 2:
            if posEndLeft == -1 and snailfishNumber[idx].isdigit():
                posEndLeft = idx
            elif posEndLeft != -1 and posStartLeft == -1 and not snailfishNumber[idx].isdigit():
                posStartLeft = idx + 1
                break
            idx -= 1
        if posStartLeft != -1:
            # print(posStartLeft, posEndLeft, snailfishNumber[posStartLeft : posEndLeft + 1])
            valLeft = int(snailfishNumber[posStartLeft : posEndLeft + 1])
        lenLeft = posEndLeft - posStartLeft + 1

        # searchRight
        posStartRight = -1
        idx = posEnd + 1
        posEndRight = -1
        while idx <= len(snailfishNumber) - 1:
            if posStartRight == -1 and snailfishNumber[idx].isdigit():
                posStartRight = idx
            elif posStartRight != -1 and posEndRight == -1 and not snailfishNumber[idx].isdigit():
                posEndRight = idx - 1
                break
            idx += 1
        if posStartRight != -1:
            valRight = int(snailfishNumber[posStartRight : posEndRight + 1])
        lenRight = posEndRight - posStartRight + 1

        tmpStr = ""

        # reconstruit le nouveau snailfishNumber
        if posStartLeft > 0:
            # print(
            # f"  EXPLODE {snailfishNumber[:posStartLeft]}{ANSI_BLUE}{snailfishNumber[posStartLeft:posStartLeft + lenLeft]}{ANSI_NORM}{snailfishNumber[posStartLeft + lenLeft:posStart]}",
            # end="",
            # )
            tmpStr += snailfishNumber[:posStartLeft]
            tmpStr += str(valLeft + eltLeft)
            tmpStr += snailfishNumber[posStartLeft + lenLeft : posStart]
        else:
            # print(f"  EXPLODE {snailfishNumber[:posStart]}", end="")
            tmpStr += snailfishNumber[:posStart]

        # print(f"{ANSI_GREEN}{snailfishNumber[posStart:posEnd+1]}{ANSI_NORM}", end="")
        tmpStr += "0"

        if posStartRight > 0:
            # print(
            # f"{snailfishNumber[posEnd+1:posStartRight]}{ANSI_BLUE}{snailfishNumber[posStartRight:posStartRight + lenRight]}{ANSI_NORM}{snailfishNumber[posStartRight + lenRight:]}"
            # )
            tmpStr += snailfishNumber[posEnd + 1 : posStartRight]
            tmpStr += str(valRight + eltRight)
            tmpStr += snailfishNumber[posStartRight + lenRight :]
        else:
            # print(f"{snailfishNumber[posEnd+1:]}")
            tmpStr += snailfishNumber[posEnd + 1 :]

        snailfishNumber = tmpStr
        # print("    ->", tmpStr)
        res = True
        break

    return res, snailfishNumber


def searchSplit(snailfishNumber):
    res = False
    for pos in range(len(snailfishNumber) - 2):
        if snailfishNumber[pos : pos + 2].isdigit():
            val = int(snailfishNumber[pos : pos + 2])
            # print(
            # f"  SPLIT {snailfishNumber[:pos]}{ANSI_BLUE}{snailfishNumber[pos:pos+2]}{ANSI_NORM}{snailfishNumber[pos+2:]}"
            # )
            tmpStr = f"{snailfishNumber[:pos]}[{int(val/2)},{int(val/2)+int(val%2)}]{snailfishNumber[pos+2:]}"
            snailfishNumber = tmpStr
            # print("    ->", tmpStr)
            res = True
            break

    return res, snailfishNumber


def magnitude(snailfishNumberLst):
    totalMagnitude = 0

    if isinstance(snailfishNumberLst[0], list):
        res = magnitude(snailfishNumberLst[0])
    else:
        res = snailfishNumberLst[0]
    totalMagnitude += 3 * res

    if isinstance(snailfishNumberLst[1], list):
        res = magnitude(snailfishNumberLst[1])
    else:
        res = snailfishNumberLst[1]
    totalMagnitude += 2 * res

    return totalMagnitude


def addSnailfishNumber(snailfishNumberA, snailfishNumberB):
    snailfishNumber = "[" + snailfishNumberA + "," + snailfishNumberB + "]"
    # print(f"Reduce snailfish number: {snailfishNumber}")
    while True:
        res, snailfishNumber = searchExplode(snailfishNumber)
        if res == True:
            continue
        res, snailfishNumber = searchSplit(snailfishNumber)
        if res == True:
            continue
        break
    # print("->", snailfishNumber)
    # print()
    return snailfishNumber


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    snailfishNumber = g_data["line"][0]
    for line in range(1, len(g_data["line"])):
        snailfishNumber = addSnailfishNumber(snailfishNumber, g_data["line"][line])

    snailfishNumberLst = eval(snailfishNumber)

    return magnitude(snailfishNumberLst)


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    magnitudeLst = []
    for i in range(len(g_data["line"]) - 1):
        for j in range(i + 1, len(g_data["line"])):
            snailfishNumber = addSnailfishNumber(g_data["line"][i], g_data["line"][j])
            magnitudeLst.append(magnitude(eval(snailfishNumber)))
            snailfishNumber = addSnailfishNumber(g_data["line"][j], g_data["line"][i])
            magnitudeLst.append(magnitude(eval(snailfishNumber)))

    return max(magnitudeLst)


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample-explode.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
