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
        g_data["line"].append(line)

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    res = 0
    for line in g_inputLines:
        a = line[: int(len(line) / 2)]
        b = line[int(len(line) / 2) :]
        print(a, b)
        car = intersection(a, b)[0]
        print("-> inter", car)

        prio = ord(car)
        if prio >= 97:
            prio = prio - 96
        else:
            prio = prio - 38
        # print(ord(car), prio)
        res += prio

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    res = 0
    for i in range(0, len(g_data["line"]), 3):
        a = g_data["line"][i]
        b = g_data["line"][i + 1]
        c = g_data["line"][i + 2]
        print("[", i, "]", a, " -", b, " -", c)
        inter_b = intersection(a, b)
        inter_c = intersection(a, c)
        inter_res = intersection(inter_b, inter_c)
        # print("  ", inter_b)
        # print("  ", inter_c)
        # print(" ", inter_res)

        car = inter_res[0]
        prio = ord(car)
        if prio >= 97:
            prio = prio - 96
        else:
            prio = prio - 38
        res += prio
        print("->", car, prio)

    return res


############
### MAIN ###
############

g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
