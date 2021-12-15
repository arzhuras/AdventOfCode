import sys
import os
import time
from collections import deque
import copy

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
    g_data["grid"] = []
    for lineVal in g_inputLines:
        g_data["grid"].append([int(digit) for digit in lineVal])

    """
    # [[list(0, 0, False)] * len(lineVal) for _ in range(len(g_inputLines))]
    maxCoord = len(g_inputLines)
    g_data["risk"] = []
    for line in range(maxCoord):
        g_data["risk"].append([])
        for col in range(maxCoord):
            g_data["risk"][line].append([])
            g_data["risk"][line][col] = [0, 0, False]  # ORIGIN, RISK, OPTIMAL
    # g_data["risk"][0][0][0] = 666
    """

    # print("initData:", g_data)


def initData2():
    NB_TEMPLATES = 5
    initData()

    # g_data["gridTemplate"] = [[] * NB_TEMPLATES for _ in range(NB_TEMPLATES)]
    g_data["gridTemplate"] = [0] * 10

    grid = g_data["grid"]
    gridTemplate = g_data["gridTemplate"]

    gridTemplate[0] = copy.deepcopy(grid)

    maxCoord = len(g_inputLines)
    for i in range(1, 10):
        for line in range(maxCoord):
            for col in range(maxCoord):
                grid[line][col] += 1
                if grid[line][col] > 9:
                    grid[line][col] = 1
        gridTemplate[i] = copy.deepcopy(grid)

    """
    for line in range(maxCoord):
        for i in range(10):
            print(gridTemplate[i][line], end="")
        print()
    print()
    """

    grid = [[0] * maxCoord * NB_TEMPLATES for _ in range(maxCoord * NB_TEMPLATES)]
    # print(grid)
    for gridLine in range(0, NB_TEMPLATES):
        for gridCol in range(0, NB_TEMPLATES):
            # print("gridLine:", gridLine, "gridCol:", gridCol, "template:", (gridLine + gridCol) % 10)
            for line in range(maxCoord):
                for col in range(maxCoord):
                    grid[(gridLine * maxCoord) + line][(gridCol * maxCoord) + col] = gridTemplate[
                        (gridLine + gridCol) % 10
                    ][line][col]
    """
    for line in grid:
        print(line)
    """

    g_data["grid"] = grid

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def getVoisin(t, maxCoord):
    lst = []
    for voisin in [(t[0] - 1, t[1]), (t[0], t[1] + 1), (t[0] + 1, t[1]), (t[0], t[1] - 1)]:
        if voisin[0] < 0 or voisin[0] >= maxCoord or voisin[1] < 0 or voisin[1] >= maxCoord:
            # print("  SKIP", voisin)
            continue
        lst.append(voisin)
    return lst


def dijkstra(cell):  # cell = tuple (ligne, colonne)
    grid = g_data["grid"]

    queue = deque([cell])
    distanceDic = {cell: 0}

    while queue:
        t = queue.popleft()
        # print(ANSI_BLUE, "SOMMET " + str(t), ANSI_NORM)

        for voisin in getVoisin(t, len(grid)):
            # print("  VOISIN", voisin, grid[voisin[0]][voisin[1]])
            # queue.append(voisin) # optim on ne rajoute que les noeuds modifiés dans la liste des noeuds a parcourir
            nouvelle_distance = distanceDic[t] + grid[voisin[0]][voisin[1]]
            if voisin not in distanceDic or nouvelle_distance < distanceDic[voisin]:
                distanceDic[voisin] = nouvelle_distance
                queue.append(voisin)
                # print(ANSI_RED, "  UPDATE " + str(voisin) + " : " + str(nouvelle_distance), ANSI_NORM)
            # print("  -> ", distance, queue)

    return distanceDic[(len(grid) - 1, len(grid) - 1)]


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    res = dijkstra((0, 0))

    return res


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    res = dijkstra((0, 0))

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
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData2()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
