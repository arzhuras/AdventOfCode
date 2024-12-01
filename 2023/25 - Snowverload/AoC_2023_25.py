from tools import *
import time
import math
import copy

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
    # components = None
    components = None

    # grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan}
# from matrix3d import *


def initData():
    fields = []
    # data.components = {}
    data.components = {}

    for line in data.rawInput:
        line = line.replace(":", "")
        fields = line.split()

        # print(fields)
        for field in fields:
            tmpLst = list(filter(lambda f: f != field, fields))
            if field not in data.components:
                # data.components[field] = [tmpLst]
                data.components[field] = set(tmpLst)
            else:
                # data.components[field].append(tmpLst)
                data.components[field].update(tmpLst)
    # for component, componentLink in data.components.items():
        # print(component, componentLink)

    for component, componentLink in data.components.items():
        print(component, sorted(componentLink))

##################
### PROCEDURES ###
##################


class Hub:
    predecessor = []
    curLink = set()
    newLink = set()


def resolve_part1():
    hubs = {}

    for curComponent in data.components:
        break  # première clé du dict!

    hub = Hub()
    hub.predecessor = []
    hub.curLink = set(data.components[curComponent])
    hub.curLink.add(curComponent)
    hub.newLink = data.components[curComponent]
    hubs[curComponent] = hub
    for newComponent in sorted(hub.newLink):
        print(f"{curComponent}->{newComponent}")
        newHub = Hub()
        newHub.predecessor = curComponent
        print("  ", hub.predecessor, sorted(hub.curLink))
        print("  ", newComponent, sorted(data.components[newComponent]))
        print(" ->", sorted(data.components[newComponent].difference(
            hub.curLink)))

    """
    for componentId, componentLinks in data.components.items():
        components[componentId] = set()
        for subComponentId in componentLinks
    """
    return None


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
