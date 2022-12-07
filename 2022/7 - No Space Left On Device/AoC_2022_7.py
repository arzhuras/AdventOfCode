from tools import *
import time

from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

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

init_script()

g_data = {}


def showTree(root, tab=""):
    print(tab, "-", root[0])
    for elt in root[1]:
        showTree(elt, tab=tab + "  ")
    for elt in root[2]:
        print(elt)


def initData():
    g_data["line"] = []

    for line in g_inputLines:
        g_data["line"].append(line)

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    sizeDict = {}
    # sizeDict["/"] = 0

    path = deque()
    curSize = 0

    for line in g_inputLines:
        # print("->", line)
        if line[0] == "$":
            if len(line) > 4:  # cd
                # store current dirSize
                # print("  SIZE: ", tuple(path), curSize)
                if tuple(path) not in sizeDict:
                    sizeDict[tuple(path)] = 0
                tmpPath = deque(path)
                for i in range(len(tuple(tmpPath))):
                    sizeDict[tuple(tmpPath)] += curSize
                    tmpPath.pop()
                curSize = 0
                # print("  sizeDict", sizeDict)

                if line[5] == ".":  # cd ..
                    # print("->  cd ..")
                    path.pop()
                else:  # cd <dir>
                    dirName = line[5:]
                    # print("->  cd", dirName)
                    path.append(dirName)
                    # print("  path", path)
        else:
            a, b = line.split()
            if a == "dir":
                # print("  # dir", b)
                pass
            else:
                # print("-> file", a, b)
                curSize += int(a)

        # store current dirSize
        # print("  SIZE: ", tuple(path), curSize)
        if tuple(path) not in sizeDict:
            sizeDict[tuple(path)] = 0
        tmpPath = deque(path)
        for i in range(len(tuple(tmpPath))):
            sizeDict[tuple(tmpPath)] += curSize
            tmpPath.pop()
        curSize = 0

    print("  sizeDict", sizeDict)
    res = 0
    for elt in sizeDict.values():
        if elt <= 100000:
            res += elt

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0
    sizeDict = {}

    path = deque()
    curSize = 0

    for line in g_inputLines:
        # print("->", line)
        if line[0] == "$":
            if len(line) > 4:  # cd
                # store current dirSize
                # print("  SIZE: ", tuple(path), curSize)
                if tuple(path) not in sizeDict:
                    sizeDict[tuple(path)] = 0
                tmpPath = deque(path)
                for i in range(len(tuple(tmpPath))):
                    sizeDict[tuple(tmpPath)] += curSize
                    tmpPath.pop()
                curSize = 0
                # print("  sizeDict", sizeDict)

                if line[5] == ".":  # cd ..
                    # print("->  cd ..")
                    path.pop()
                else:  # cd <dir>
                    dirName = line[5:]
                    # print("->  cd", dirName)
                    path.append(dirName)
                    # print("  path", path)
        else:
            a, b = line.split()
            if a == "dir":
                # print("  # dir", b)
                pass
            else:
                # print("-> file", a, b)
                curSize += int(a)

        # store current dirSize
        # print("  SIZE: ", tuple(path), curSize)
        if tuple(path) not in sizeDict:
            sizeDict[tuple(path)] = 0
        tmpPath = deque(path)
        for i in range(len(tuple(tmpPath))):
            sizeDict[tuple(tmpPath)] += curSize
            tmpPath.pop()
        curSize = 0

    totalSize = sizeDict[("/",)]
    print("totalSize", totalSize)
    deltaSize = 30000000 - (70000000 - totalSize)
    print("deltaSize", deltaSize)

    sizeLst = []
    for elt in sizeDict.items():
        if elt[1] > deltaSize:  # on prend même les répertoires intermédiaires -> plus grand que les feuilles
            # print(elt[0], elt[1])
            sizeLst.append(elt[1])

    return min(sizeLst)


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

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
