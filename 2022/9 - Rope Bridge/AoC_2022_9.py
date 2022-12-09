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
        a, b = line.split()
        g_data["line"].append((a, int(b)))

    # print("initData:", g_data)

    # print("line", g_data["line"])


def showGrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x], end="")
        print()


class Data:
    gridMove = []
    gridHeat = []
    head = (0, 0)  # x, y
    tail = (0, 0)  # x, y
    knotLst = []


data = Data()


def move(offset):  # offset_x, offset_y
    # print("move", data.head, data.tail, "->", offset[0], offset[1])

    data.gridMove[data.head[1]][data.head[0]] = "."
    data.gridMove[data.tail[1]][data.tail[0]] = "."

    data.head = data.head[0] + offset[0], data.head[1] + offset[1]
    if abs(data.head[0] - data.tail[0]) <= 1 and abs(data.head[1] - data.tail[1]) <= 1:
        pass
        # print("  no tail move")
    else:
        deltaX = data.head[0] - data.tail[0]
        if deltaX < 0:
            deltaX = -1
        elif deltaX > 0:
            deltaX = 1

        deltaY = data.head[1] - data.tail[1]
        if deltaY < 0:
            deltaY = -1
        elif deltaY > 0:
            deltaY = 1
        data.tail = data.tail[0] + deltaX, data.tail[1] + deltaY

    # print(" ", "head:", data.head, "tail", data.tail)
    data.gridMove[data.tail[1]][data.tail[0]] = "T"
    data.gridMove[data.head[1]][data.head[0]] = "H"
    data.gridHeat[data.tail[1]][data.tail[0]] = "#"


def move2(offset, knotCount):  # offset_x, offset_y, knotCount = last knot
    # print(f"move head {data.knotLst[0]} from {offset} with {knotCount} trailing knots")

    # clear gridMove
    for i in range(knotCount + 1):  # head + n knots
        data.gridMove[data.knotLst[i][1]][data.knotLst[i][0]] = "."

    # set header move
    data.knotLst[0] = data.knotLst[0][0] + offset[0], data.knotLst[0][1] + offset[1]

    # update all the nodes
    for i in range(1, knotCount + 1):
        # print(f"  [{i}] {data.knotLst[i - 1]} {data.knotLst[i]}")
        if (
            abs(data.knotLst[i - 1][0] - data.knotLst[i][0]) <= 1
            and abs(data.knotLst[i - 1][1] - data.knotLst[i][1]) <= 1
        ):
            # print(f"  [{i}] : no move")
            break
        else:
            deltaX = data.knotLst[i - 1][0] - data.knotLst[i][0]
            if deltaX < 0:
                deltaX = -1
            elif deltaX > 0:
                deltaX = 1

            deltaY = data.knotLst[i - 1][1] - data.knotLst[i][1]
            if deltaY < 0:
                deltaY = -1
            elif deltaY > 0:
                deltaY = 1
            # print(f"  [{i}] : move ({deltaX}, {deltaY})")
            data.knotLst[i] = data.knotLst[i][0] + deltaX, data.knotLst[i][1] + deltaY

    # update gridMove
    for i in range(knotCount, -1, -1):  # head + n knots
        data.gridMove[data.knotLst[i][1]][data.knotLst[i][0]] = str(i)

    data.gridHeat[data.knotLst[knotCount][1]][data.knotLst[knotCount][0]] = "#"


##################
### PROCEDURES ###
##################


def resolve_part1(width, height, init_x, init_y):
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    data.gridMove = [["."] * width for _ in range(height)]
    data.gridHeat = [["."] * width for _ in range(height)]

    data.gridMove[init_y][init_x] = "s"
    data.gridHeat[init_y][init_x] = "#"
    # showGrid(data.gridMove)
    data.head = (init_x, init_y)
    data.tail = (init_x, init_y)

    MOVE_OFFSET = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}  # offset_x, offset_y

    for line in g_data["line"]:
        # print("==", line[0], line[1], "==")
        for _ in range(line[1]):
            move(MOVE_OFFSET[line[0]])
            # showGrid(data.gridMove)
            # print()
        # print()

    # print()
    # print("HeatMap")
    # showGrid(data.gridHeat)

    res = 0

    for y in range(len(data.gridHeat)):
        for x in range(len(data.gridHeat[0])):
            if data.gridHeat[y][x] == "#":
                res += 1

    return res


def resolve_part2(width, height, init_x, init_y, knotCount):
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    data.gridMove = [["."] * width for _ in range(height)]
    data.gridHeat = [["."] * width for _ in range(height)]

    data.gridMove[init_y][init_x] = "s"
    data.gridHeat[init_y][init_x] = "#"
    # showGrid(data.gridMove)

    # init head + knots
    for i in range(knotCount + 1):  # head + n knots
        data.knotLst.append((init_x, init_y))
    print(data.knotLst)

    MOVE_OFFSET = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}  # offset_x, offset_y

    for line in g_data["line"]:
        # print("==", line[0], line[1], "==")
        for _ in range(line[1]):
            move2(MOVE_OFFSET[line[0]], knotCount)
            # showGrid(data.gridMove)
            # print()
        # showGrid(data.gridMove)
        # print()

    # print("HeatMap")
    # showGrid(data.gridHeat)

    res = 0

    for y in range(len(data.gridHeat)):
        for x in range(len(data.gridHeat[0])):
            if data.gridHeat[y][x] == "#":
                res += 1

    return res


def getBound(grid, empty):
    minY, maxY = sys.maxsize, -1
    minX, maxX = sys.maxsize, -1

    print(sys.maxsize)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != empty:
                if y < minY:
                    minY = y
                elif y > maxY:
                    maxY = y

                if x < minX:
                    minX = x
                elif x > maxX:
                    maxX = x
    print(f"x [{minX}, {maxX}]")
    print(f"y [{minY}, {maxY}]")

    return ((minX, maxX), ((minY), (maxY)))


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
# res = resolve_part1(6, 5, 0, 4)
# res = resolve_part1(1000, 1000, 500, 500)
res = resolve_part2(1000, 1000, 500, 500, 1)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

initData()
data.gridMove = []
data.gridHeat = []
data.knotLst = []

### PART 2 ###
startTime = time.time()
# res = resolve_part2(6, 5, 0, 4, 9)
# res = resolve_part2(40, 30, 20, 15, 9)
res = resolve_part2(1000, 1000, 500, 500, 9)
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

getBound(data.gridMove, ".")
