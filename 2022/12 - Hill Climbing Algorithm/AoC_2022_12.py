from tools import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

g_inputLines = []


class Data:
    rawInput = []


data = Data()


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


def initData():
    data.grid = []
    data.best = []
    data.origin = None, None
    data.dest = None, None
    data.height = len(data.rawInput)
    data.width = len(data.rawInput[0])
    data.shortest = None
    data.visited = 0

    for y in range(data.height):
        tmpLst = []
        for x in range(data.width):
            car = data.rawInput[y][x]
            if car == "S":
                tmpLst.append(ord("a"))
                data.origin = x, y
            elif car == "E":
                tmpLst.append(ord("z"))
                data.dest = x, y
            else:
                tmpLst.append(ord(car))
        data.grid.append(tuple(tmpLst))
        data.best.append([-1] * data.width)

    #print("data.grid:", data.grid)
    #print("data.best:", data.best)
    #print("data.origin:", data.origin)
    #print("data.dest:", data.dest)


##################
### PROCEDURES ###
##################

SCAN_UP = (-1, 0)
SCAN_RIGHT = (0, 1)
SCAN_DOWN = (1, 0)
SCAN_LEFT = (0, -1)


def inspectNode(curX, curY, curCost=0, depth=0):
    tab = " " * depth
    data.visited += 1
    curX, curY = curX, curY
    curHeat = data.grid[curY][curX]

    #print(tab, f"[{depth}] ({curX}, {curY}), curCost: {curCost}, best: {data.best[curY][curX]}, visited: {data.visited}/{data.width * data.height}")
    data.best[curY][curX] = curCost

    if curX == data.dest[0] and curY == data.dest[1]:
        #print(tab, "  DEST found", curCost, data.shortest)
        if data.shortest == None or data.shortest > curCost:
            data.shortest = curCost
        return

    if data.shortest != None and curCost >= data.shortest:
        return

    for scan in SCAN_UP, SCAN_RIGHT, SCAN_DOWN, SCAN_LEFT:
        nextX, nextY = curX + scan[1], curY + scan[0]
        if nextX < 0 or nextX >= data.width:
            continue
        if nextY < 0 or nextY >= data.height:
            continue

        if data.best[nextY][nextX] != -1 and data.best[nextY][nextX] <= curCost + 1:
            # print(tab, "  already visited and lower score")
            continue

        # nextHeat = data.grid[nextY][nextX]
        if data.grid[nextY][nextX] - curHeat > 1:
            continue

        inspectNode(nextX, nextY, curCost + 1, depth + 1)


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    inspectNode(data.origin[0], data.origin[1])
    #for line in data.best:
        #print(line)

    res = data.shortest
    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = []

    for y in range(data.height):
        for x in range(data.width):
            if data.grid[y][x] == ord('a'):
                print(f"Check new origin: {x},{y}")
                # reset 
                data.best = []
                data.shortest = None
                data.visited = 0
                for _ in range(data.height):
                    data.best.append([-1] * data.width)
    
                inspectNode(x, y)
                #for line in data.best:
                    #print(line)

                if data.shortest != None:
                    res.append(data.shortest)

    print(res)
    return min(res)

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

#exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
