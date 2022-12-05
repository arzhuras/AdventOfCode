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

    nbStacks = int((len(g_inputLines[0]) + 1) / 4)

    g_data["stacks"] = [deque() for i in range(nbStacks)]
    lineIdx = 0
    while (g_inputLines[lineIdx][1] != "1"):
        #print("->", g_inputLines[lineIdx][2])
        for i in range(nbStacks):
            car  = g_inputLines[lineIdx][1+(4*i)]
            if (car != " "):
                g_data["stacks"][i].appendleft(car)
        lineIdx += 1

    lineIdx += 2
    g_data["moves"] = []
    while (lineIdx < len(g_inputLines)):
        _, a,_,b,_,c = g_inputLines[lineIdx].split()
        g_data["moves"].append((int(a),int(b)-1,int(c)-1))
        lineIdx += 1

    #print("line  : ", g_data["line"])
    #print("stacks: ", g_data["stacks"])
    #print("moves: ", g_data["moves"])


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    stacks = g_data["stacks"]
    moves = g_data["moves"]

    for count, src, dst in moves:
        #print(count, stacks[src], stacks[dst])
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())
        #print(stacks)
    
    res = ""
    for elt in stacks:
        res+= elt[-1]
    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    stacks = g_data["stacks"]
    moves = g_data["moves"]

    for count, src, dst in moves:
        #print(count, "[", src, "]", stacks[src], "[", dst, "]", stacks[dst])
        tmpDeq = deque()
        for _ in range(count):
            tmpDeq.append(stacks[src].pop())
        #print("tmpDeq", tmpDeq)
        for _ in range(count):
            stacks[dst].append(tmpDeq.pop())
        #print("->",stacks)
    
    res = ""
    for elt in stacks:
        res+= elt[-1]
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

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
