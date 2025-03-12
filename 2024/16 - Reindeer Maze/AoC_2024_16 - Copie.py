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
# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    fields = None
    line = None
    gridLst = None
    grid = None

    startPos = None
    endPos = None


data = Data()

###  /modules libraries ###
from matrix2d import *

MATRIX2D_COLORSET = {
    "#": Ansi.cyan,
    "X": Ansi.red,
    "S": Ansi.yellow,
    "E": Ansi.red,
    ">": Ansi.green,
    "<": Ansi.green,
    "v": Ansi.green,
    "^": Ansi.green,
}
# from matrix3d import *
from graph import *


def initData():
    data.grid = data.gridLst[0]
    data.startPos = None
    data.endPos = None
    for y in range(len(data.grid)):
        for x in range(len(data.grid[y])):
            if data.grid[y][x] == "S":
                # data.grid[y][x] = "."
                data.startPos = (y, x)
            if data.grid[y][x] == "E":
                data.endPos = (y, x)
                # data.grid[y][x] = "."
    showGrid(data.grid, MATRIX2D_COLORSET)
    print(data.startPos, data.endPos)


##################
### PROCEDURES ###
##################


def resolve_part1():

    return None


# [coord entrante][coord sortante] -> cout
COST_FROM_ORIGIN = {
    OFFSET.N: {
        OFFSET.E: 1000 * 1 + 1,
        OFFSET.S: 1,
        OFFSET.W: 1000 * 1 + 1,
        OFFSET.N: 1000 * 2 + 1,
    },
    OFFSET.E: {
        OFFSET.S: 1000 * 1 + 1,
        OFFSET.W: 1,
        OFFSET.N: 1000 * 1 + 1,
        OFFSET.E: 1000 * 2 + 1,
    },
    OFFSET.S: {
        OFFSET.W: 1000 * 1 + 1,
        OFFSET.N: 1,
        OFFSET.E: 1000 * 1 + 1,
        OFFSET.S: 1000 * 2 + 1,
    },
    OFFSET.W: {
        OFFSET.N: 1000 * 1 + 1,
        OFFSET.E: 1,
        OFFSET.S: 1000 * 1 + 1,
        OFFSET.W: 1000 * 2 + 1,
    },
}


def buildGraphFromGrid(grid):
    graph = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                continue
            graph[(y, x)] = {}  # coordonnées y, x du noeud + direction entrante
            for offset in OFFSET.CROSS:
                if grid[y + offset.y][x + offset.x] != "#":
                    graph[(y, x)][(y + offset.y, x + offset.x)] = None
    return graph


def dijkstraAlgoWithPath(graph: dict, startNode: str) -> list:
    """
    Dijkstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale + le chemin depuis la source
    """
    queue = deque([startNode])  # inDir = W par défaut
    distance = {startNode: (0, [startNode], OFFSET.W, [(0, OFFSET.W.label)], [])}
    while queue:
        curNode = queue.popleft()
        inDir = distance[curNode][2]
        print("cur:", curNode, inDir.label, distance[curNode][0])
        if curNode in [(7, 5), (8, 3)]:
            print(Ansi.green, "     cur", curNode, distance[curNode], Ansi.norm)
        for nextNode in graph[curNode]:
            print("   next: ", nextNode)
            outDir = OFFSET.MAP_OFFSET[
                (nextNode[0] - curNode[0], nextNode[1] - curNode[1])
            ]
            nouvelle_distance = distance[curNode][0] + COST_FROM_ORIGIN[inDir][outDir]
            if nextNode in [(7, 5), (8, 3)]:
                print(
                    Ansi.blue,
                    "     next",
                    nextNode,
                    inDir.label,
                    outDir.label,
                    nouvelle_distance,
                    Ansi.norm,
                )

            # if nextNode not in distance or (
            #     distance[curNode][2] != inDir
            #     and nouvelle_distance < distance[nextNode][0]
            # ):
            if nextNode not in distance or nouvelle_distance < distance[nextNode][0]:
                if nextNode not in distance:
                    print(
                        "     NEW",
                        nextNode,
                        OFFSET.OPPOSITE[outDir].label,
                        nouvelle_distance,
                        distance[curNode],
                    )
                elif nouvelle_distance < distance[nextNode][0]:
                    print(
                        "     SHORT",
                        nextNode,
                        OFFSET.OPPOSITE[outDir].label,
                        nouvelle_distance,
                        # distance[nextNode][0],
                    )
                distance[nextNode] = (
                    nouvelle_distance,  # [0] distance
                    distance[curNode][1] + [nextNode],  # [1] path list
                    OFFSET.OPPOSITE[outDir],  # [2] inDir
                    distance[curNode][3]  # [3] cost list
                    + [
                        (COST_FROM_ORIGIN[inDir][outDir], OFFSET.OPPOSITE[outDir].label)
                    ],
                    [],  # [4] alt path list
                )
                queue.append(nextNode)
            elif nouvelle_distance == distance[nextNode][0]:
                print(
                    Ansi.yellow,
                    "    EQUAL",
                    nextNode,
                    OFFSET.OPPOSITE[outDir].label,
                    nouvelle_distance,
                    # distance[nextNode][0],
                    Ansi.norm,
                )
                distance[nextNode][4].append(distance[curNode][1] + [nextNode])

    # remove the node itself from the list
    del distance[startNode]

    return distance


def resolve_bothpart():
    grid = data.grid
    showGrid(grid, MATRIX2D_COLORSET)

    graph = buildGraphFromGrid(grid)
    # showGraph(graph)
    distance = dijkstraAlgoWithPath(graph, data.startPos)

    # print(distance)
    # print()
    # for key in sorted(distance.keys()):
    #     print(key, len(distance[key]))
    print(distance[data.endPos])

    prevNode = data.startPos
    for node in distance[data.endPos][1][1:-1]:
        grid[node[0]][node[1]] = OFFSET.MAP_OFFSET[
            (node[0] - prevNode[0], node[1] - prevNode[1])
        ].move
        prevNode = node
    showGrid(grid, MATRIX2D_COLORSET, 2)
    print(distance[data.endPos][0])
    print(len(distance[data.endPos][1]))
    print(data.endPos, distance[data.endPos])
    for node, cost, alt in zip(
        distance[data.endPos][1], distance[data.endPos][3], distance[data.endPos][4]
    ):
        print(node, cost, alt)

    print()
    # print(distance[(7, 6)])
    # print(distance[(7, 5)])

    # get all path
    nodes = set(distance[data.endPos][1])
    print(nodes)

    return distance[data.endPos][0], None


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"
# inputFile = "sample3.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.gridLst = loadMatrix2d(inputFile)


### PART 1 ###
year, dayTitle = os.path.dirname(sys.argv[0]).split("/")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
# res1 = resolve_part1()
res1, res2 = resolve_bothpart()
endTime = time.time()

print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")

if res2 == None:
    exit()

### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
# res2 = resolve_part2()
endTime = time.time()

print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
