from tools import *
import time
import math
import copy

# from collections import deque
import operator
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
    workflows = None
    parts = None

    # grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# from matrix3d import *


opFunc = {">": operator.gt, "<": operator.lt}
catMap = {"x": 0, "m": 1, "a": 2, "s": 3}


def initData():
    data.fields = []
    data.workflows = {}
    data.parts = []

    lineIdx = 0
    while lineIdx < len(data.rawInput):
        line = data.rawInput[lineIdx]
        if line == "":
            break
        line = line.replace("{", " ")
        line = line.replace("}", " ")
        line = line.replace(",", " ")
        fields = line.split()

        label = fields[0]
        rules = []
        for field in fields[1:-1]:
            rule, target = field.split(":")
            rules.append((catMap[rule[0]], rule[1], int(rule[2:]), target))
        rules.append((None, None, None, fields[-1]))
        data.workflows[label] = rules
        lineIdx += 1
    lineIdx += 1
    while lineIdx < len(data.rawInput):
        line = data.rawInput[lineIdx]
        line = line.replace("{", "")
        line = line.replace("}", "")
        line = line.replace("=", "")
        line = line.replace("x", "")
        line = line.replace("m", "")
        line = line.replace("a", "")
        line = line.replace("s", "")
        line = line.replace(",", " ")
        data.parts.append(tuple(map(int, line.split())))
        lineIdx += 1

    # print("workflows:", data.workflows)
    # print()
    # print("parts:", data.parts)


##################
### PROCEDURES ###
##################

def resolve_part1():

    sumParts = 0
    for part in data.parts:
        # print("part:", part)
        workflow = "in"
        while workflow != "A" and workflow != "R":
            # print("  workflow", workflow, data.workflows[workflow])
            for rule in data.workflows[workflow]:
                if rule[0] == None:
                    workflow = rule[3]
                    # print("    default ->", workflow)
                    break

                if opFunc[rule[1]](part[rule[0]], rule[2]) == True:
                    workflow = rule[3]
                    # print("   ", part[rule[0]], rule[1],
                    # rule[2], "->", workflow)
                    break
                # print("   ", part[rule[0]], rule[1], rule[2], "-> NOMATCH")
        if workflow == "A":
            sumParts += sum(part)
            # print(part, "A", sumParts)

    return sumParts


# accepted (minCatVal, maxCatVal, path)
def applyWorkflow(workflow, minCatVal, maxCatVal, accepted, path=[], level=0):
    tab = "  " * level
    print(tab, level, "  workflow", workflow,
          "min", minCatVal, "max", maxCatVal, path)

    if workflow == "R":
        print(tab, level, Ansi.red, "REJECTED", Ansi.norm)
        return

    if workflow == "A":
        accepted.append((minCatVal, maxCatVal, path))
        print(tab, level, Ansi.green, "ACCEPTED", accepted[-1], Ansi.norm)
        return

    path.append(workflow)
    print(tab, level, "  rules", data.workflows[workflow])

    if level > 10:
        print("MAX REC DEPTH")
        exit()

    for ruleCat, ruleOp, ruleVal, ruleWorkflow in data.workflows[workflow]:
        if ruleCat == None:
            print(tab, level, "    default ->", ruleWorkflow)
            applyWorkflow(ruleWorkflow, minCatVal.copy(),
                          maxCatVal.copy(), accepted, path.copy(), level + 1)
        else:
            tmpMinCatVal = minCatVal.copy()
            tmpMaxCatVal = maxCatVal.copy()
            # on valide la règle
            if (ruleOp == ">" and maxCatVal[ruleCat] > ruleVal) or (ruleOp == "<" and minCatVal[ruleCat] < ruleVal):
                if ruleOp == ">":
                    tmpMinCatVal[ruleCat] = ruleVal + 1  # accepted case
                    maxCatVal[ruleCat] = ruleVal  # rejected case: next rule
                else:
                    tmpMaxCatVal[ruleCat] = ruleVal - 1  # accepted case
                    minCatVal[ruleCat] = ruleVal  # rejected case: next rule
                applyWorkflow(ruleWorkflow, tmpMinCatVal,
                              tmpMaxCatVal, accepted, path.copy(), level + 1)

    return


def resolve_part2():
    minCatVal = [1, 1, 1, 1]
    maxCatVal = [4000, 4000, 4000, 4000]
    accepted = []

    applyWorkflow("in", minCatVal, maxCatVal, accepted)

    print()
    sumCombi = 0
    for elt in accepted:
        print(elt)
        sumCombi += math.prod(map(lambda l: l[1] -
                              l[0] + 1, zip(elt[0], elt[1])))

    return sumCombi


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

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

# exit()

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
