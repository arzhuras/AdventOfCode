import sys
import os
import time
from collections import defaultdict

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
    g_data["signals"] = []
    g_data["outputs"] = []
    for line in g_inputLines:
        signal, output = line.split("|")
        signal = signal.strip()
        output = output.strip()

        g_data["signals"].append(["".join(sorted(elt)) for elt in signal.split(" ")])
        g_data["outputs"].append(["".join(sorted(elt)) for elt in output.split(" ")])

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    specialOutputCount = 0
    for outputLst in g_data["outputs"]:
        for output in outputLst:
            if len(output) == 2 or len(output) == 3 or len(output) == 4 or len(output) == 7:
                # print(f"GOTCHA {output} {len(output)}")
                specialOutputCount += 1
        print(outputLst, specialOutputCount)
    return specialOutputCount


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    digitsDic = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }

    totalSum = 0
    for idx in range(len(g_data["signals"])):
        signalLst = g_data["signals"][idx]
        print("signalLst:", signalLst)
        segmentDic = defaultdict(lambda: "abcdefg")
        for signal in signalLst:
            pattern = [elt for elt in digitsDic.keys() if len(elt) == len(signal)]
            # print(f"\nsignal: {signal}, len: {len(signal)}, pattern: {pattern}")
            for segment in signal:
                tmpStr = ""
                for car in segmentDic[segment]:
                    carFound = False
                    for elt in pattern:
                        if elt.find(car) >= 0:
                            carFound = True
                            # print(f"  keep '{car}'")
                        else:
                            # print(f"  discard '{car}'")
                            pass
                    if carFound:
                        tmpStr += car
                segmentDic[segment] = tmpStr

        for key, value in segmentDic.items():
            if value != "cf":
                value = value.replace("c", "")
                segmentDic[key] = value.replace("f", "")

        for key, value in segmentDic.items():
            if value != "bd":
                value = value.replace("b", "")
                segmentDic[key] = value.replace("d", "")

        for key, value in segmentDic.items():
            if value != "a":
                segmentDic[key] = value.replace("a", "")

        # print()
        # for i in "abcedfg":
        #    print(f"  segmentDic['{i}']: {segmentDic[i]}")

        # exit()

        bdMatch = ""
        cfMatch = ""
        egMatch = ""
        for key, value in segmentDic.items():
            if value == "bd":
                bdMatch += key
            if value == "cf":
                cfMatch += key
            if value == "eg":
                egMatch += key
        # print(" ->", "bd:", bdMatch, "cf:", cfMatch, "eg:", egMatch)

        bdPattern = ""
        cfPattern = ""
        egPattern = ""
        for pattern in [elt for elt in g_data["signals"][idx] if len(elt) == 5]:
            if pattern.find(bdMatch[0]) >= 0 and pattern.find(bdMatch[1]) >= 0:
                bdPattern = pattern
                # print("bd ->5:", bdMatch, bdPattern)
            if pattern.find(cfMatch[0]) >= 0 and pattern.find(cfMatch[1]) >= 0:
                cfPattern = pattern
                # print("cf ->3:", cfMatch, cfPattern)
            if pattern.find(egMatch[0]) >= 0 and pattern.find(egMatch[1]) >= 0:
                egPattern = pattern
                # print("eg ->2:", egMatch, egPattern)

        # diff bd 5 vs cf 3
        for car in bdPattern:
            if cfPattern.find(car) == -1:
                segmentDic[car] = "b"
                if car == bdMatch[0]:
                    segmentDic[bdMatch[1]] = "d"
                else:
                    segmentDic[bdMatch[0]] = "d"
                break

        # diff cf 3 vs bd 5
        for car in cfPattern:
            if bdPattern.find(car) == -1:
                segmentDic[car] = "c"
                if car == cfMatch[0]:
                    segmentDic[cfMatch[1]] = "f"
                else:
                    segmentDic[cfMatch[0]] = "f"
                break

        # diff eg 2 vs cf 3
        for car in egPattern:
            if cfPattern.find(car) == -1:
                segmentDic[car] = "e"
                if car == egMatch[0]:
                    segmentDic[egMatch[1]] = "g"
                else:
                    segmentDic[egMatch[0]] = "g"
                break

        # print()
        # for i in "abcedfg":
        # print(f"  segmentDic['{i}']: {segmentDic[i]}")

        codeStr = ""
        for output in g_data["outputs"][idx]:
            # print(output)
            tmpStr = ""
            for car in output:
                tmpStr += segmentDic[car]
            tmpStr = "".join(sorted(tmpStr))

            codeStr += str(digitsDic[tmpStr])

        print("outputsLst:", g_data["outputs"][idx], "-> :", codeStr)
        print()
        totalSum += int(codeStr)

    return totalSum


############
### MAIN ###
############

g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
