import sys
import os
import time
import re
import copy

from collections import namedtuple

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
g_data_d = {}
#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])

g_yLen = 0
g_xLen = 0
g_zMin = -1
g_zLen = 3


def initDataStructure():
    global g_data_d
    global g_xLen
    global g_yLen

    g_data_d = {}

    # https://pythex.org/
    # patternField = r"^([a-z ]*): (\d*)-(\d*) or (\d*)-(\d*)"
    g_data_d[-1] = []
    g_data_d[0] = []
    g_data_d[1] = []
    for line in g_inputLines:
        # print(line)
        g_data_d[0].append(list(line))

    g_yLen = len(g_data_d[0])
    g_xLen = len(g_data_d[0][0])

    #print(yLen, xLen)
    g_data_d[-1] = [['.'] * g_xLen for _ in range(g_yLen)]
    g_data_d[1] = [['.'] * g_xLen for _ in range(g_yLen)]

    # print(g_data_l)


def activeNeighbors(arg_x, arg_y, arg_z):
    activeCount = 0
    #print(f"(z:{arg_z}, y:{arg_y}, x:{arg_x}) = {g_data_l[arg_z][arg_y][arg_x]}")
    for z in range(arg_z-1, arg_z+2):
        if (z < g_zMin or z == g_zMin + g_zLen):
            #print("skip z=", z)
            continue
        #print("z=", z)
        for y in range(arg_y-1, arg_y+2):
            if (y < 0 or y == g_yLen):
                #print("  skip y=", y)
                continue
            #print("  y=", y)
            for x in range(arg_x-1, arg_x+2):
                if (x < 0 or x == g_xLen):
                    #print("    skip x=", x)
                    continue
                #print("    x=", x)
                if (z == arg_z and y == arg_y and x == arg_x):
                    #print(f"  skip (z:{z}, y:{y}, x:{x})")
                    continue
                #print(f"  (z:{z}, y:{y}, x:{x}) = {g_data_l[z][y][x]}")
                if (g_data_d[z][y][x] == '#'):
                    #print(f"  (z:{z}, y:{y}, x:{x}) = {g_data_l[z][y][x]}")
                    activeCount += 1
                    #print("  # ", activeCount)
    #print("->", activeCount)
    return activeCount


def show():
    out = [ "" for _ in range(g_yLen)]
    for z in g_data_d.keys():
        i = 0
        for y in g_data_d[z]:
            tmpStr = f"[{z:>2}]"
            for x in y:
                tmpStr += " " + x
            #print(tmpStr)
            out[i] += tmpStr + "  "
            i += 1
    for s in out:
        print(s)


def resolve_part2():
    global g_data_d

    #print("resolve_part2():", g_data_l)

    show()

    round = 0
    while (round < 5):
        print("### ROUND", round)
        tmpData_d = copy.deepcopy(g_data_d)
        for z in range(g_zMin, g_zMin + g_zLen):
            for y in range(0, g_yLen):
                for x in range(0, g_xLen):
                    res = activeNeighbors(x, y, z)
                    #print(f"  (z:{z}, y:{y}, x:{x}) = {g_data_d[z][y][x]} neighbors= {res}")
                    if (tmpData_d[z][y][x] == '#' and (res < 2 or res > 3)):
                        #print(f"  -> .")
                        tmpData_d[z][y][x] = '.'
                    elif (res == 3):
                        #print(f"  -> #")
                        tmpData_d[z][y][x] = '#'
        round += 1
        g_data_d = tmpData_d
        show()

    return -1


def resolve_part1():
    #print("resolve_part1():", g_data_l)

    return -1


g_inputLines = readInputFile("AoC_2020_17_sample.txt")
#g_inputLines = readInputFile()

res = -1

###
# PART 1
###

print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")

###
# PART 2
###

print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
