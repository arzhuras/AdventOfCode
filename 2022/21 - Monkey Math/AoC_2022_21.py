from tools import *

# from matrix2d import *
# from matrix3d import *

import time

# from collections import deque
# import operator

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    monkeysYell = None  # dict
    monkeysCalc = None  # dict


data = Data()


def initData():
    data.line = []
    data.monkeysYell = {}
    data.monkeysCalc = {}

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
    print("yell:", data.monkeysYell)
    print("calc:", data.monkeysCalc)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    round = 0
    while len(data.monkeysCalc) > 0:
        print(round, "Calc:", len(data.monkeysCalc), "Yell:", len(data.monkeysYell))
        # print("Calc ->", len(data.monkeysCalc), data.monkeysCalc)
        # print("Yell ->", len(data.monkeysYell), data.monkeysYell)
        tmpMonkeyLst = []
        for monkey, calc in data.monkeysCalc.items():
            # if monkey == "root":
            # print("  ", monkey, calc)
            if calc[0] in data.monkeysYell and calc[2] in data.monkeysYell:
                print("     bingo", monkey, calc, data.monkeysYell[calc[0]], data.monkeysYell[calc[2]])
                if calc[1] == "+":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] + data.monkeysYell[calc[2]]
                elif calc[1] == "-":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] - data.monkeysYell[calc[2]]
                elif calc[1] == "*":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] * data.monkeysYell[calc[2]]
                elif calc[1] == "/":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] / data.monkeysYell[calc[2]]
                else:
                    print("error")
                    exit()
                tmpMonkeyLst.append(monkey)
        for monkey in tmpMonkeyLst:
            data.monkeysCalc.pop(monkey)
        round += 1
        # print()
    # print("Yell ->", len(data.monkeysYell), data.monkeysYell)
    print("Calc ->", len(data.monkeysCalc), data.monkeysCalc)

    return data.monkeysYell["root"]


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    round = 0
    while len(data.monkeysCalc) > 0:
        print(round, "Calc:", len(data.monkeysCalc), "Yell:", len(data.monkeysYell))
        # print("Calc ->", len(data.monkeysCalc), data.monkeysCalc)
        # print("Yell ->", len(data.monkeysYell), data.monkeysYell)
        tmpMonkeyLst = []
        for monkey, calc in data.monkeysCalc.items():
            # if monkey == "root":
            # print("  ", monkey, calc)
            if calc[0] in data.monkeysYell and calc[2] in data.monkeysYell:
                print("     bingo", monkey, calc, data.monkeysYell[calc[0]], data.monkeysYell[calc[2]])
                if calc[1] == "+":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] + data.monkeysYell[calc[2]]
                elif calc[1] == "-":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] - data.monkeysYell[calc[2]]
                elif calc[1] == "*":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] * data.monkeysYell[calc[2]]
                elif calc[1] == "/":
                    data.monkeysYell[monkey] = data.monkeysYell[calc[0]] / data.monkeysYell[calc[2]]
                else:
                    print("error")
                    exit()
                tmpMonkeyLst.append(monkey)
        for monkey in tmpMonkeyLst:
            data.monkeysCalc.pop(monkey)
        round += 1
        # print()
    # print("Yell ->", len(data.monkeysYell), data.monkeysYell)
    print("Calc ->", len(data.monkeysCalc), data.monkeysCalc)

    return data.monkeysYell["root"]


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
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
