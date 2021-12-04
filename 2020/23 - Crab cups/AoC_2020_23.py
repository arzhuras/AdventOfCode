import sys
import os
import time
import re
import copy
import math
import timeit
from collections import deque

#from collections import namedtuple

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
print(f"=== {SCRIPT_NAME} ===")


def readInputFile(file=INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines


g_inputLines = []
g_data_l = []
# g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])

# testcode = '''


def test():
    lst = [i for i in range(1000000)]
    lst.insert(0, "zorro")
    # lst.insert(999998,"zorro")
    # print(lst[:10])
    # print(lst[-10:])
    print("deque: insert 0/100000 ", timeit.timeit(
        setup="from collections import deque; lst = deque([i for i in range(100000)])", stmt='lst.insert(0,-1)', number=100000))
    print("deque: insert 99990/100000 ", timeit.timeit(
        setup="from collections import deque; lst = deque([i for i in range(100000)])", stmt='lst.insert(99990, -1)', number=100000))
    print("list: insert 0/100000 ", timeit.timeit(
        setup="lst = [i for i in range(100000)]", stmt='lst.insert(0,-1)', number=100000))
    print("list: insert 99990/100000 ", timeit.timeit(
        setup="lst = [i for i in range(100000)]", stmt='lst.insert(99990, -1)', number=100000))
# '''

def initDataStructure():
    global g_data_l

    g_data_l = []

    # https://pythex.org/
    # patternRule = r"^(\d*): (\d*) (\d*) \| (\d*)-(\d*)
    for line in g_inputLines:
        g_data_l.append(list(line))

def show2(curCup, nextCup_l):
    DISPLAY = 15
    if (len(nextCup_l) < DISPLAY):
        DISPLAY = len(nextCup_l) - 1
    
    tmpStr = f"cups: ({curCup})"
    curCup = nextCup_l[curCup]
    for _ in range(1, DISPLAY):
        tmpStr += f" {curCup}"
        curCup = nextCup_l[curCup]
    print(tmpStr)


def moveCup2(curCup, nextCup_l):
    #show2(curCup, nextCup_l)

    # step 1: pick up
    a = nextCup_l[curCup]
    b = nextCup_l[a]
    c = nextCup_l[b]

    #print(f"pick up: {a}, {b}, {c}")

    # step 2 : select destination
    destination = curCup - 1
    while (destination == a or destination == b or destination == c) and destination > 0:
        destination -= 1
    if (destination == 0):
        destination = len(nextCup_l) - 1
        while (destination == a or destination == b or destination == c) and destination > 0:
            destination -= 1

    #print(f"destination : {destination}")

    # step 3 : insert
    nextCup_l[curCup] = nextCup_l[c]
    tmpCup = nextCup_l[destination]
    nextCup_l[destination] = a
    nextCup_l[c] = tmpCup

    curCup = nextCup_l[curCup]

    return curCup, nextCup_l


def resolve_part2():
    MAX_MOVE = 10000000
    #MAX_MOVE = 15

    #INPUT_CUP = "389125467"  # sample
    INPUT_CUP = "326519478" # OFFICIAL INPUT

    nextCup_l = [i for i in range(1, 1000000+2)]
    nextCup_l[1000000] = int(INPUT_CUP[0])

    # set initial cup
    cup_l = [int(cup) for cup in list(INPUT_CUP)]
    for i in range(len(cup_l)-1):
        nextCup_l[cup_l[i]] = cup_l[i+1]
    nextCup_l[cup_l[i+1]] = len(cup_l) + 1

    curCup = int(INPUT_CUP[0])

    show2(curCup, nextCup_l)
    show2(1000000, nextCup_l)

    moveCount = 0
    while (moveCount < MAX_MOVE):
        #print(f"-- move {moveCount+1} --")
        curCup, nextCup_l = moveCup2(curCup, nextCup_l)
        moveCount += 1
        #show2(1000000, nextCup_l)
        #print()

    print(f"-- final ({moveCount}) --")
    show2(curCup, nextCup_l)

    a = nextCup_l[1]
    b = nextCup_l[a]
    print("answer:", a, b, a * b)
    show2(1, nextCup_l)

    return a * b


def resolve_part1():
    MAX_MOVE = 100
    #INPUT_CUP = "389125467"
    INPUT_CUP = "326519478"

    # set initial cup
    nextCup_l = [0] * (len(INPUT_CUP) + 1)
    for i in range(len(INPUT_CUP) - 1):
        nextCup_l[int(INPUT_CUP[i])] = int(INPUT_CUP[i+1])
    nextCup_l[(int(INPUT_CUP[i+1]))] = int(INPUT_CUP[0])

    curCup = int(INPUT_CUP[0])

    show2(curCup, nextCup_l)

    moveCount = 0
    while (moveCount < MAX_MOVE):
        #print(f"-- move {moveCount+1} --")
        curCup, nextCup_l = moveCup2(curCup, nextCup_l)
        moveCount += 1
        #print()

    print(f"-- final ({moveCount}) --")
    show2(curCup, nextCup_l)

    tmpStr = ""
    cup = 1
    for _ in range(len(INPUT_CUP)-1):
        tmpStr += str(nextCup_l[cup])
        cup = nextCup_l[cup]

    return tmpStr


#g_inputLines = readInputFile("AoC_2020_23_sample.txt")
#g_inputLines = readInputFile()

res = -1

###
# PART 1
###

# '''
print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''

###
# PART 2
###

# '''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

# initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''
