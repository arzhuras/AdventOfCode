from tools import *
from graph import *
import time
from collections import deque
import copy

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
    line = []
    graph = None  # Dict
    nodeFlowRate = None  # Dict
    shortestDistanceWithPath = None  # dict
    globalBestReleaseRate = 0
    processCount = 0


data = Data()


def initData():
    data.line = []
    data.graph = {}
    data.nodeFlowRate = {}
    data.shortestDistanceWithPath = {}
    data.globalBestReleaseRate = 0
    data.processCount = 0

    for line in data.rawInput:
        line = line.replace(",", "")
        line = line.replace(";", "")
        line = line.replace("=", " ")
        data.line.append(line)

        fields = line.split()
        data.graph[fields[1]] = {}
        for neighbour in fields[10:]:
            data.graph[fields[1]][neighbour] = 1
        data.nodeFlowRate[fields[1]] = int(fields[5])

    # find shortest path between each node
    for key in data.graph:
        data.shortestDistanceWithPath[key] = dijkstraAlgoWithPath(data.graph, key)

    # remove 0 flowRate node from the neighbourg
    for key in data.shortestDistanceWithPath:
        tmpLst = [key2 for key2 in data.shortestDistanceWithPath[key] if data.nodeFlowRate[key2] == 0]
        for elt in tmpLst:
            del data.shortestDistanceWithPath[key][elt]

    # showGraph(shortestDistanceWithPath)

    # print("initData:", data.line)
    # showGraph(data.graph)
    print("graph:", data.graph)
    print()
    print("nodeFlowRate:", data.nodeFlowRate)


##################
### PROCEDURES ###
##################

MAX_TIME = 30
MAX_TIME2 = 26


def recursive_dfs(graph, node, visited=None, remainingTime=MAX_TIME, curReleaseRate=0, tab=""):
    # print(f"{tab}{Ansi.blue}# {node} {remainingTime} -> {curReleaseRate} {visited}{Ansi.norm}")

    if visited is None:
        visited = {}

    if node not in visited:
        visited[node] = (
            MAX_TIME - remainingTime + 1,
            remainingTime,
            data.nodeFlowRate[node],
        )  # on garde le node initial même si son flowRate est nul
        curReleaseRate += remainingTime * data.nodeFlowRate[node]
        # print(f"{tab}  visited: {visited} curReleaseRate: {curReleaseRate}")

    # hypothesis: all nodes are accessible from all nodes
    unvisited = sorted([n for n in graph if n not in visited and data.nodeFlowRate[n] > 0])
    # print(f"{tab}  unvisited: {unvisited}")

    if len(unvisited) == 0:
        return visited, curReleaseRate

    bestVisited = visited
    bestCurReleaseRate = curReleaseRate
    for nextNode in unvisited:
        # print(f"{tab}  {node} {nextNode} {graph[node][nextNode]}")
        if remainingTime - 1 - graph[node][nextNode][0] < 0:
            continue

        tmpVisited, tmpCurReleaseRate = recursive_dfs(
            graph,
            nextNode,
            copy.deepcopy(visited),
            remainingTime - 1 - graph[node][nextNode][0],
            curReleaseRate,
            tab + "  ",
        )
        # print(f"{tab}  {tmpVisited} {tmpCurReleaseRate}")

        if tmpCurReleaseRate > bestCurReleaseRate:
            # print(f"{tab}  {Ansi.green}{node} {nextNode} best!!!!{Ansi.norm}")
            bestVisited = tmpVisited
            bestCurReleaseRate = tmpCurReleaseRate
    # print(f"{tab}  bestVisited: {bestVisited}")

    return bestVisited, bestCurReleaseRate


def recursive_dfs2(graph, nodeLst, visited=None, remainingTimeLst=[MAX_TIME2, MAX_TIME2], curReleaseRate=0, tab=""):
    """node and remainingTime are lists. First node is the one with lower or equal remainingTime"""
    # print(f"{tab}{Ansi.blue}# {nodeLst} {remainingTimeLst} -> {curReleaseRate} {visited}{Ansi.norm}")

    if curReleaseRate > 20000:
        print("curReleaseRate", curReleaseRate)
        exit()

    if visited is None:
        visited = {}

    # compute state update for the current node
    if nodeLst[0] not in visited:
        visited[nodeLst[0]] = (
            MAX_TIME2 - remainingTimeLst[0] + 1,
            remainingTimeLst[0],
            data.nodeFlowRate[nodeLst[0]],
        )  # on garde le node initial même si son flowRate est nul
        curReleaseRate += remainingTimeLst[0] * data.nodeFlowRate[nodeLst[0]]

        if curReleaseRate > data.globalBestReleaseRate:
            data.globalBestReleaseRate = curReleaseRate
            print(Ansi.green, "globalBestReleaseRate1", curReleaseRate, visited, Ansi.norm)

        """
        tmpRate = 0
        for val in visited.values():
            tmpRate = tmpRate + val[1] * val[2]

        # print(f"{tab}  visited: {nodeLst[0]} -> {visited} curReleaseRate: {curReleaseRate} {tmpRate}")
        if curReleaseRate != tmpRate:
            print("updt1", nodeLst[0], curReleaseRate, visited, tmpRate)
            exit()
        """

    # hypothesis: all nodes are accessible from all nodes
    unvisited = [n for n in graph if n not in visited and n != nodeLst[1] and data.nodeFlowRate[n] > 0]
    # print(f"{tab}  unvisited: {unvisited}")

    # if len(unvisited) == 0:
    # return visited, curReleaseRate

    bestVisited = visited
    bestCurReleaseRate = curReleaseRate
    for nextNode in unvisited:
        # print(f"{tab}  Check {nodeLst[0]} {nextNode} {graph[nodeLst[0]][nextNode][0]}")
        nextRemainingTime = remainingTimeLst[0] - 1 - graph[nodeLst[0]][nextNode][0]
        if nextRemainingTime < 0:
            continue

        # tri du prochain noeud en fonction du remainingTime
        if nextRemainingTime > remainingTimeLst[1]:
            nextNodeLst = [nextNode, nodeLst[1]]
            nextRemainingTimeLst = [nextRemainingTime, remainingTimeLst[1]]
        else:
            nextNodeLst = [nodeLst[1], nextNode]
            nextRemainingTimeLst = [remainingTimeLst[1], nextRemainingTime]

        tmpVisited, tmpCurReleaseRate = recursive_dfs2(
            graph,
            copy.deepcopy(nextNodeLst),
            copy.deepcopy(visited),
            copy.deepcopy(nextRemainingTimeLst),
            curReleaseRate,
            tab + "  ",
        )
        # print(f"{tab}  Res  {nodeLst[0]}, {nextNodeLst} {tmpVisited} {tmpCurReleaseRate}")

        if tmpCurReleaseRate > bestCurReleaseRate:
            # print(f"{tab}  {Ansi.green}Best {nodeLst[0]} {nextNode} -> {tmpVisited} {tmpCurReleaseRate}{Ansi.norm}")
            bestVisited = tmpVisited
            bestCurReleaseRate = tmpCurReleaseRate

    # s'il reste un second noeud, on l'ignore, il a forcément moins de remainingTime
    # print(f"{tab}{Ansi.blue}# final node {nodeLst[1]} {remainingTimeLst[1]} -> {curReleaseRate} {visited}{Ansi.norm}")
    if nodeLst[1] not in bestVisited:
        bestVisited[nodeLst[1]] = (
            MAX_TIME2 - remainingTimeLst[1] + 1,
            remainingTimeLst[1],
            data.nodeFlowRate[nodeLst[1]],
        )  # on garde le node initial même si son flowRate est nul
        bestCurReleaseRate += remainingTimeLst[1] * data.nodeFlowRate[nodeLst[1]]
        # print(
        # f"{tab}  {Ansi.red}final node: {nodeLst[1]} {remainingTimeLst[1]} -> visited: {bestVisited} curReleaseRate: {bestCurReleaseRate}{Ansi.norm}"
        # )
        if bestCurReleaseRate > data.globalBestReleaseRate:
            data.globalBestReleaseRate = bestCurReleaseRate
            print(Ansi.green, "globalBestReleaseRate2", bestCurReleaseRate, bestVisited, Ansi.norm)

        data.processCount += 1
        if data.processCount % 100000 == 0:
            print(f"Processing [{data.processCount}] : {nodeLst[0]} {curReleaseRate} {visited}")

        """
        tmpRate = 0
        for val in bestVisited.values():
            tmpRate = tmpRate + val[1] * val[2]

        if tmpRate != bestCurReleaseRate:
            print("updt2", nodeLst[0], bestCurReleaseRate, bestVisited, tmpRate)
            exit()
        """

    return bestVisited, bestCurReleaseRate


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    visited, curReleaseRate = recursive_dfs(data.shortestDistanceWithPath, "AA")
    print()
    print("best", curReleaseRate, visited)

    return curReleaseRate


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    visited, curReleaseRate = recursive_dfs2(data.shortestDistanceWithPath, ["AA", "AA"])
    print()
    print("best", curReleaseRate, visited)

    return curReleaseRate


############
### MAIN ###
############

readInputFile("sample.txt")
readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# LOW 2101
# LOW 2152
# LOW 2284
