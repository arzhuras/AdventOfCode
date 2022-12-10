from tools import *
import time
from collections import deque

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
        a = line.split()
        if a[0] == "noop":
            g_data["line"].append([a[0]])
        else:
            g_data["line"].append([a[0], int(a[1])])

    # print("initData:", g_data)
    # print("line:", g_data["line"])


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    cycle = 1
    regX = 1
    pipe = deque()
    nextExecutionCycle = 0
    regXLst = [None]  # fill cycle 0!

    for line in g_data["line"]:
        # print(f"[{cycle}] {regX} {line}'")
        regXLst.append(regX)

        # populate execution pipe
        if line[0] == "noop":
            if len(pipe) == 0:
                nextExecutionCycle = cycle
            pipe.append((nextExecutionCycle, "noop", 0))
            nextExecutionCycle += 1
        elif line[0] == "addx":
            if len(pipe) == 0:
                nextExecutionCycle = cycle + 1
            pipe.append((nextExecutionCycle, "addx", line[1]))
            nextExecutionCycle += 2
        else:
            print("error", line)
            exit()

        # execute the pipe
        if len(pipe) > 0 and pipe[0][0] == cycle:
            # print("  exec", pipe[0][1], pipe[0][2])
            if pipe[0][1] == "addx":
                regX += pipe[0][2]
            pipe.popleft()

        cycle += 1
        # print(" ->", regX)
        # print(pipe)

    while len(pipe) > 0:
        # print(cycle, regX)
        regXLst.append(regX)

        if pipe[0][0] == cycle:
            # print("  exec", pipe[0][1], pipe[0][2])
            if pipe[0][1] == "addx":
                regX += pipe[0][2]
            pipe.popleft()

        cycle += 1
        # print(" ->", regX)

    res = 0
    for i in range(20, 221, 40):
        print(i, regXLst[i])
        res += i * regXLst[i]

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    cycle = 1
    regX = 1
    pipe = deque()
    nextExecutionCycle = 0
    regXLst = [None]  # fill cycle 0!
    crt = [""] * 7
    crtLine = 0
    crtCol = 0

    for line in g_data["line"]:
        # print(f"[{cycle}] {regX} {line}'")
        regXLst.append(regX)

        # manage CRT
        crtLine = (cycle - 1) // 40
        crtCol = (cycle - 1) % 40
        # print(f"  crtLine: {crtLine}, crtCol: {crtCol}")
        if crtCol >= regX - 1 and crtCol <= regX + 1:
            crt[crtLine] = crt[crtLine] + "#"
        else:
            crt[crtLine] = crt[crtLine] + "."

        # populate execution pipe
        if line[0] == "noop":
            if len(pipe) == 0:
                nextExecutionCycle = cycle
            pipe.append((nextExecutionCycle, "noop", 0))
            nextExecutionCycle += 1
        elif line[0] == "addx":
            if len(pipe) == 0:
                nextExecutionCycle = cycle + 1
            pipe.append((nextExecutionCycle, "addx", line[1]))
            nextExecutionCycle += 2
        else:
            print("error", line)
            exit()

        # execute the pipe
        if len(pipe) > 0 and pipe[0][0] == cycle:
            # print("  exec", pipe[0][1], pipe[0][2])
            if pipe[0][1] == "addx":
                regX += pipe[0][2]
            pipe.popleft()

        cycle += 1
        # print(" ->", regX)
        # print(pipe)

    # print("exec remaining pipe")
    while len(pipe) > 0:
        # print(cycle, regX)
        regXLst.append(regX)

        # manage CRT
        crtLine = (cycle - 1) // 40
        crtCol = (cycle - 1) % 40
        # print(f"  crtLine: {crtLine}, crtCol: {crtCol}")
        if crtLine == 6:
            break

        if crtCol >= regX - 1 and crtCol <= regX + 1:
            crt[crtLine] = crt[crtLine] + "#"
        else:
            crt[crtLine] = crt[crtLine] + "."

        # execute the pipe
        if pipe[0][0] == cycle:
            # print("  exec", pipe[0][1], pipe[0][2])
            if pipe[0][1] == "addx":
                regX += pipe[0][2]
            pipe.popleft()

        cycle += 1
        # print(" ->", regX)

    print()
    for line in crt:
        print(line)
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
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

# exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
