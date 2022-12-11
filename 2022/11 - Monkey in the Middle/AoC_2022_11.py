from tools import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

g_inputLines = []


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

g_data = {}


class Data:
    rawInput = []
    monkeys = []
    primeMul = 1


data = Data()


def initData():
    data.monkeys = []
    data.inspectCount = []
    curStuff = None

    for line in data.rawInput:
        inputField = line.split()
        # print(inputField)
        if len(inputField) == 0:
            # print("curStuff:", curStuff)
            # print()
            continue

        if inputField[0] == "Monkey":
            curStuff = {}
            data.monkeys.append(curStuff)
            data.inspectCount.append(0)
        elif inputField[0] == "Starting":
            curStuff["items"] = deque()
            curStuff["newItems"] = []
            for elt in inputField[2:]:
                elt = elt.replace(",", "")
                curStuff["items"].append(int(elt))
        elif inputField[0] == "Operation:":
            if inputField[5] == "old":
                curStuff["operation"] = (inputField[4], "old")
            else:
                curStuff["operation"] = (inputField[4], int(inputField[5]))
        elif inputField[0] == "Test:":
            curStuff["test"] = int(inputField[3])
            data.primeMul *= curStuff["test"]
        elif inputField[1] == "true:":
            curStuff["ifTrue"] = int(inputField[5])
        elif inputField[1] == "false:":
            curStuff["ifFalse"] = int(inputField[5])

    # for i in range(len(data.monkeys)):
    # print("### Monkey", i, "###")
    # print("-> ", data.monkeys[i])


##################
### PROCEDURES ###
##################


def inspect(monkey, mode=1):
    stuff = data.monkeys[monkey]

    # primeMul1 = 13 * 17 * 19 * 23
    # primeMul2 = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19

    for _ in range(len(stuff["items"])):
        data.inspectCount[monkey] += 1
        worry = stuff["items"][0]
        # print(f"    item {worry}")

        # print(f"      operation {stuff['operation']}")
        operand = 0
        if stuff["operation"][1] == "old":
            operand = worry
        else:
            operand = stuff["operation"][1]
        if stuff["operation"][0] == "*":
            worry = worry * operand
        elif stuff["operation"][0] == "+":
            worry = worry + operand
        # print(f"        new worry {worry}")
        if mode == 1:
            worry = worry // 3
            # print(f"        new worry 2 {worry}")

        # print(f"      test div by {stuff['test']}")
        # print(f"        ifTrue {stuff['ifTrue']}")
        # print(f"        ifFalse {stuff['ifFalse']}")

        if worry % stuff["test"] == 0:
            # print(f"          true: -> {stuff['ifTrue']}")
            if mode == 1:
                data.monkeys[stuff["ifTrue"]]["items"].append(worry)
            else:
                # data.monkeys[stuff["ifTrue"]]["items"].append(worry)
                # data.monkeys[stuff["ifTrue"]]["items"].append(worry // stuff["test"])
                # data.monkeys[stuff["ifTrue"]]["items"].append(worry % data.monkeys[stuff["ifTrue"]]["test"])
                # data.monkeys[stuff["ifTrue"]]["items"].append(worry // data.monkeys[stuff["ifTrue"]]["test"])
                # data.monkeys[stuff["ifTrue"]]["items"].append(worry // primeMul2)
                # data.monkeys[stuff["ifTrue"]]["items"].append((worry // primeMul1) + (worry % primeMul1))
                data.monkeys[stuff["ifTrue"]]["items"].append((worry % data.primeMul))
        else:
            # print(f"          false: -> {stuff['ifFalse']}")
            if mode == 1:
                data.monkeys[stuff["ifFalse"]]["items"].append(worry)
            else:
                # data.monkeys[stuff["ifFalse"]]["items"].append(worry)
                # data.monkeys[stuff["ifFalse"]]["items"].append(worry // stuff["test"])
                # data.monkeys[stuff["ifFalse"]]["items"].append(worry // data.monkeys[stuff["ifFalse"]]["test"])
                # data.monkeys[stuff["ifFalse"]]["items"].append((worry // primeMul1) + (worry % primeMul1))
                data.monkeys[stuff["ifFalse"]]["items"].append((worry % data.primeMul))
        stuff["items"].popleft()


def resolve_part1(maxRound):
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    for round in range(1, maxRound + 1):
        # print("### Round", round, "###")
        # Take new items
        # for monkey in range(len(data.monkeys)):
        # if len(data.monkeys[monkey]["newItems"]) > 0:
        # data.monkeys[monkey]["items"].append(data.monkeys[monkey]["newItems"])

        # Inspect for all monkeys
        for monkey in range(len(data.monkeys)):
            # print("  ### Monkey", monkey, "###")
            inspect(monkey)
            # print()

        # for monkey in range(len(data.monkeys)):
        # print(f"  Monkey {monkey}", data.monkeys[monkey]["items"])

        # print(data.inspectCount)
        # print()

    print(f"Inspect count after {maxRound} round: ", data.inspectCount)
    print()
    res = sorted(data.inspectCount)[-2:]
    res = res[0] * res[1]

    return res


def resolve_part2(maxRound):
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    for round in range(1, maxRound + 1):
        # print("### Round", round, "###")

        # Inspect for all monkeys
        for monkey in range(len(data.monkeys)):
            # print("  ### Monkey", monkey, "###")
            inspect(monkey, 2)
            # print()

        # for monkey in range(len(data.monkeys)):
        # print(f"  Monkey {monkey}", data.monkeys[monkey]["items"])

        # print(data.inspectCount)
        # print()

    # for monkey in range(len(data.monkeys)):
    # print(f"  Monkey {monkey}", data.monkeys[monkey]["items"])
    print(f"Inspect count after {maxRound} round: ", data.inspectCount)
    print()
    res = sorted(data.inspectCount)[-2:]
    res = res[0] * res[1]

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
res = resolve_part1(20)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2(10000)
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
