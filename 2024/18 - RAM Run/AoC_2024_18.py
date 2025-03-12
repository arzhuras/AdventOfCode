import copy
import math
import time
from collections import defaultdict

from tools import *

# import re

# from collections import deque

# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

# from functools import reduce
# from functools import cache

# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None
    lineFields = None
    gridLst = None
    grid = None


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red, "O": Ansi.yellow}
# from matrix3d import *
from graph import *


def initData():
    data.lineFields = []
    # data.rules = defaultdict(lambda: set())
    # data.line = "".join(data.rawInput)

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        # intFields = list(map(int,line.split()))
        data.lineFields.append(tuple(map(int, line.split(","))))

    # print("lineFields:", data.lineFields)

    # data.grid = []
    # data.grid = loadMatrix2d(inputFile)[0]
    # showGrid(data.grid)

    # data.grids = []
    # data.grids = loadMatrix2d(inputFile)
    # showGridLst(data.grid)

    # REGEXP https://pynative.com/python-regex-findall-finditer/
    # line = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    # res = re.finditer(r"mul\((?P<a>\d+),(?P<b>\d+)\)|(do\(\))|(don\'t\(\))",data.line)
    # for match in res:
    # print(match)
    # print(match.group())
    # print(match.group(1))
    # print(match.group(2))
    # print(match.group("a"))
    # print(match.group("b"))


##################
### PROCEDURES ###
##################


def resolve_part1():
    WIDTH = 7
    HEIGHT = 7
    maxFallingBytes = 12

    WIDTH = 71
    HEIGHT = 71
    maxFallingBytes = 1024

    grid = [["." for x in range(WIDTH)] for y in range(HEIGHT)]
    # grid = data.gridLst[0]
    # grid = [["." for x in range(width)] for y in range(height)]

    for x, y in data.lineFields[:maxFallingBytes]:
        grid[y][x] = "#"
    extendGridForce(grid, eltEmpty="#")
    showGrid(grid)

    graph = buildGraphFromGrid(grid)
    # showGraph(graph)

    shortestDistanceWithPath = dijkstraAlgoWithPath(graph, (1, 1))
    # print(shortestDistanceWithPath[(WIDTH,HEIGHT)])
    for y, x in shortestDistanceWithPath[(WIDTH, HEIGHT)][1]:
        grid[y][x] = "O"
    showGrid(grid, colorset=MATRIX2D_COLORSET)

    return shortestDistanceWithPath[(WIDTH, HEIGHT)][0]


def resolve_part2():
    grid = [["." for x in range(WIDTH)] for y in range(HEIGHT)]
    for x, y in data.lineFields:
        grid[y][x] = "#"
        graph = buildGraphFromGrid(grid)
        # showGraph(graph)

        shortestDistance = dijkstraAlgo(graph, (0, 0))
        if (WIDTH - 1, HEIGHT - 1) not in shortestDistance:
            # showGrid(grid, colorset=MATRIX2D_COLORSET)
            print(f"({x},{y}) : {Ansi.red}IMPOSSIBLE{Ansi.norm}")
            return (x, y)
        # print(shortestDistance[(WIDTH - 1, HEIGHT - 1)])
        print(f"({x},{y}) : {shortestDistance[(WIDTH-1, HEIGHT-1)]}")

    return shortestDistanceWithPath[(WIDTH - 1, HEIGHT - 1)][0]


############
### MAIN ###
############

# MAX_ROUND = 10
WIDTH = 7
HEIGHT = 7
inputFile = "sample.txt"

# MAX_ROUND = 1000
WIDTH = 71
HEIGHT = 71
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.gridLst = loadMatrix2d(inputFile)


### PART 1 ###
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)
initData()
startTime = time.time()
res1 = resolve_part1()
# res1, res2 = resolve_bothpart()
endTime = time.time()
print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")


### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)
initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()
print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
