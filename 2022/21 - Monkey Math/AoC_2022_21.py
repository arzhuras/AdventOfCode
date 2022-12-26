from tools import *

# from matrix2d import *
# from matrix3d import *

import time

# from collections import deque
import operator

opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    monkeysYell = None  # Dict
    monkeysCalc = None  # Dict
    history = None  # Dict


data = Data()


def initData():
    data.line = []
    data.monkeysYell = {}
    data.monkeysCalc = {}
    data.history = {}

    for line in data.rawInput:
        line = line.replace(":", "")
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        data.line.append(line)

        fields = line.split()
        if len(fields) == 2:
            data.monkeysYell[fields[0]] = int(fields[1])
        else:
            data.monkeysCalc[fields[0]] = (fields[1], fields[2], fields[3])

    # print("initData:", data.line)
    # print("yell:", data.monkeysYell)
    # print("calc:", data.monkeysCalc)


##################
### PROCEDURES ###
##################


def compute(yellDict, calcDict):
    roundNum = 0
    history = {}

    # yellDict["humn"] = 3712643961892
    # calcDict["root"] = (data.monkeysCalc["root"][0], "-", data.monkeysCalc["root"][2])

    while len(calcDict) > 0:
        print(roundNum, "Calc:", len(calcDict), "Yell:", len(yellDict))
        # print("Yell ->", len(data.monkeysYell), data.monkeysYell)
        # print("Calc ->", len(data.monkeysCalc), data.monkeysCalc)
        tmpMonkeyLst = []
        for monkey, calc in calcDict.items():
            if calc[0] in yellDict and calc[2] in yellDict:
                yellDict[monkey] = opFunc[calc[1]](yellDict[calc[0]], yellDict[calc[2]])
                # """
                print(
                    "     bingo",
                    monkey,
                    calc,
                    yellDict[calc[0]],
                    yellDict[calc[2]],
                    yellDict[monkey],
                )
                # """
                history[monkey] = (
                    monkey,
                    calc,
                    yellDict[calc[0]],
                    yellDict[calc[2]],
                    yellDict[monkey],
                )
                tmpMonkeyLst.append(monkey)
        for monkey in tmpMonkeyLst:
            calcDict.pop(monkey)
        roundNum += 1
        # print()
    # print("Yell ->", len(data.monkeysYell), data.monkeysYell)
    # print("Calc ->", len(data.monkeysCalc), data.monkeysCalc)

    data.history = history

    return history


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    history = compute(data.monkeysYell.copy(), data.monkeysCalc.copy())
    return history["root"][-1]


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    ancestorsLst = []
    curAncestor = "humn"
    for ancestor in data.history:
        if data.history[ancestor][1][0] == curAncestor or data.history[ancestor][1][2] == curAncestor:
            ancestorsLst.append(data.history[ancestor][0])
            curAncestor = data.history[ancestor][0]
            # print(data.history[ancestor])
    ancestorsLst.reverse()
    ancestorsLst.append("humn")
    print(ancestorsLst)

    if data.history["root"][1][1] == ancestorsLst[1]:
        target = data.history["root"][2]
    else:
        target = data.history["root"][3]
    print("final target:", target)

    ancestor = "root"
    print(
        f"{ancestor}: {data.history[ancestor][1]} {data.history[ancestor][2]} {data.history[ancestor][1][1]} {data.history[ancestor][3]} =  {target} -> {data.history[ancestor][4]}"
    )
    for i in range(1, len(ancestorsLst) - 1):
        ancestor = ancestorsLst[i]
        print(
            f"  {ancestor}: {data.history[ancestor][1]} {data.history[ancestor][2]} {data.history[ancestor][1][1]} {data.history[ancestor][3]} =  {target} -> {data.history[ancestor][4]}"
        )
        if data.history[ancestor][1][0] == ancestorsLst[i + 1]:
            findLeft = True
            arg = data.history[ancestor][3]
            print(f"    {data.history[ancestor][1][0]} = ", end="")
        else:
            findLeft = False
            arg = data.history[ancestor][2]
            print(f"    {data.history[ancestor][1][2]} = ", end="")

        op = data.history[ancestor][1][1]
        if op == "+":
            print(f"{op} {target} - {arg} = {target - arg}")
            target = target - arg
        elif op == "-":
            if findLeft:
                print(f"{op} {target} + {arg} = {target + arg}")
                target = target + arg
            else:
                print(f"{op} -({target} - {arg}) = {-(target - arg)}")
                target = -(target - arg)

        elif op == "*":
            print(f"{op} {target} / {arg} = {target / arg}")
            target = target / arg
        elif op == "/":
            if findLeft:
                print(f"{op} {target} * {arg} = {target * arg}")
                target = target * arg
            else:
                print(f"{op} {arg} / {target} = {arg / target}")
                target = target * arg

    return target


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()

# data.monkeysYell["humn"] = 301
# data.monkeysYell["humn"] = 3712643961892
# data.monkeysCalc["root"] = (data.monkeysCalc["root"][0], "-", data.monkeysCalc["root"][2])
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
print()

# exit()

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
