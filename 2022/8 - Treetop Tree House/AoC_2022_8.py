from tools import *
import time

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


def initData():
    g_data["line"] = []

    for line in g_inputLines:
        g_data["line"].append(tuple((int(car) for car in line)))

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    width = len(g_inputLines[0])
    height = len(g_inputLines)

    visibleCount = 0
    for y in range(1, width - 1):
        for x in range(1, height - 1):
            curHeight = g_inputLines[y][x]
            # print(f"[{y}, {x}] {curHeight}")

            # scan right
            if x < width - 1:
                visible = True
                y2 = y
                for x2 in range(x + 1, width):
                    if g_inputLines[y2][x2] >= curHeight:
                        # print(f"  [{y2}, {x2}] {g_inputLines[y2][x2]} -> FALSE RIGHT")
                        visible = False
                        break
                if visible == True:
                    # print(f"[{y}, {x}] {curHeight} VISIBLE RIGHT")
                    visibleCount += 1

            # scan left
            if visible == False and x > 0:
                visible = True
                y2 = y
                for x2 in range(x - 1, -1, -1):
                    if g_inputLines[y2][x2] >= curHeight:
                        # print(f"  [{y2}, {x2}] {g_inputLines[y2][x2]} -> FALSE LEFT")
                        visible = False
                        break
                if visible == True:
                    # print(f"[{y}, {x}] {curHeight} VISIBLE LEFT")
                    visibleCount += 1

            # scan up
            if visible == False and y > 0:
                visible = True
                x2 = x
                for y2 in range(y - 1, -1, -1):
                    if g_inputLines[y2][x2] >= curHeight:
                        # print(f"  [{y2}, {x2}] {g_inputLines[y2][x2]} -> FALSE LEFT")
                        visible = False
                        break
                if visible == True:
                    # print(f"[{y}, {x}] {curHeight} VISIBLE UP")
                    visibleCount += 1

            # scan down
            if visible == False and y > 0:
                visible = True
                x2 = x
                for y2 in range(y + 1, height):
                    if g_inputLines[y2][x2] >= curHeight:
                        # print(f"  [{y2}, {x2}] {g_inputLines[y2][x2]} -> FALSE LEFT")
                        visible = False
                        break
                if visible == True:
                    # print(f"[{y}, {x}] {curHeight} VISIBLE DOWN")
                    visibleCount += 1

    res = visibleCount + 2 * width + 2 * (height - 2)

    return res


# scan mode (y,x) -1, 0, 1
SCAN_TOP = (-1, 0)
SCAN_RIGHT = (0, 1)
SCAN_DOWN = (1, 0)
SCAN_LEFT = (0, -1)


def getViewDist(x, y, treeHeight, scan):  # scan mode (x,y) -1, 0, 1
    width = len(g_inputLines[0])
    height = len(g_inputLines)
    print("->", x, y, treeHeight, scan)
    # y
    if scan[0] == -1:
        minY = y - 1
        maxY = 0
        incY = -1
    elif scan[0] == 0:
        minY = y
        maxY = y + 1
        incY = 1
    else:
        minY = y + 1
        maxY = height
        incY = 1

    # x
    if scan[1] == -1:
        minX = x - 1
        maxX = 0
        incX = -1
    elif scan[1] == 0:
        minX = x
        maxX = x + 1
        incX = 1
    else:
        minX = x + 1
        maxX = width
        incX = 1

    viewDist = 0
    for y2 in range(minY, maxY, incY):
        print("y2", y2)
        for x2 in range(minX, maxX, incX):
            print("  x2", x2)
            viewDist += 1
            if g_inputLines[y2][x2] >= treeHeight:
                break
    return viewDist


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    width = len(g_inputLines[0])
    height = len(g_inputLines)

    scenicScoreLst = []
    for y in range(width):
        for x in range(height):
            treeHeight = g_inputLines[y][x]
            # print(f"[{y}, {x}] {curHeight}")

            scenicScore = 1

            # scan right
            viewDist = 0
            y2 = y
            for x2 in range(x + 1, width):
                viewDist += 1
                if g_inputLines[y2][x2] >= treeHeight:
                    break
            scenicScore *= viewDist
            # print(viewDist, getViewDist(x, y, treeHeight, SCAN_RIGHT))

            # scan left
            viewDist = 0
            y2 = y
            for x2 in range(x - 1, -1, -1):
                viewDist += 1
                if g_inputLines[y2][x2] >= treeHeight:
                    break
            scenicScore *= viewDist

            # scan up
            viewDist = 0
            x2 = x
            for y2 in range(y - 1, -1, -1):
                viewDist += 1
                if g_inputLines[y2][x2] >= treeHeight:
                    break
            scenicScore *= viewDist

            # scan down
            viewDist = 0
            x2 = x
            for y2 in range(y + 1, height):
                viewDist += 1
                if g_inputLines[y2][x2] >= treeHeight:
                    break
            scenicScore *= viewDist

            scenicScoreLst.append(scenicScore)

    # print(scenicScoreLst)
    print(getViewDist(2, 3, "5", SCAN_RIGHT))
    print(getViewDist(2, 3, "5", SCAN_LEFT))
    res = max(scenicScoreLst)

    return res


############
### MAIN ###
############

g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile()

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
