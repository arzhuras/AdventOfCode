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
g_minMax_l = [[0, 0], [0, 0], [0, 0], [0, 0]]
MINMAX_W = 0
MINMAX_Z = 1
MINMAX_Y = 2
MINMAX_X = 3
MINMAX_MIN = 0
MINMAX_MAX = 1


def setCar2(w, z, y, x, car):
    #print(f"setCar ({w:2}, {z:2}, {y:2}, {x:2}) -> {car}")
    if (w not in g_data_d):
        g_data_d[w] = {}

    if (z not in g_data_d[w]):
        g_data_d[w][z] = {}

    if (y not in g_data_d[w][z]):
        g_data_d[w][z][y] = {}

    g_data_d[w][z][y][x] = car

    # TODO: recalculer les minmax pour car = '.'
    if (w < g_minMax_l[MINMAX_W][MINMAX_MIN]):
        g_minMax_l[MINMAX_W][MINMAX_MIN] = w
    elif (w > g_minMax_l[MINMAX_W][MINMAX_MAX]):
        g_minMax_l[MINMAX_W][MINMAX_MAX] = w

    if (z < g_minMax_l[MINMAX_Z][MINMAX_MIN]):
        g_minMax_l[MINMAX_Z][MINMAX_MIN] = z
    elif (z > g_minMax_l[MINMAX_Z][MINMAX_MAX]):
        g_minMax_l[MINMAX_Z][MINMAX_MAX] = z

    if (y < g_minMax_l[MINMAX_Y][MINMAX_MIN]):
        g_minMax_l[MINMAX_Y][MINMAX_MIN] = y
    elif (y > g_minMax_l[MINMAX_Y][MINMAX_MAX]):
        g_minMax_l[MINMAX_Y][MINMAX_MAX] = y

    if (x < g_minMax_l[MINMAX_X][MINMAX_MIN]):
        g_minMax_l[MINMAX_X][MINMAX_MIN] = x
    elif (x > g_minMax_l[MINMAX_X][MINMAX_MAX]):
        g_minMax_l[MINMAX_X][MINMAX_MAX] = x


def setCar(z, y, x, car):
    #print(f"setCar ({z}, {y}, {x}) -> {car}")
    if (z not in g_data_d):
        g_data_d[z] = {}

    if (y not in g_data_d[z]):
        g_data_d[z][y] = {}

    g_data_d[z][y][x] = car

    # TODO: recalculer les minmax pour car = '.'
    if (z < g_minMax_l[MINMAX_Z][MINMAX_MIN]):
        g_minMax_l[MINMAX_Z][MINMAX_MIN] = z
    elif (z > g_minMax_l[MINMAX_Z][MINMAX_MAX]):
        g_minMax_l[MINMAX_Z][MINMAX_MAX] = z

    if (y < g_minMax_l[MINMAX_Y][MINMAX_MIN]):
        g_minMax_l[MINMAX_Y][MINMAX_MIN] = y
    elif (y > g_minMax_l[MINMAX_Y][MINMAX_MAX]):
        g_minMax_l[MINMAX_Y][MINMAX_MAX] = y

    if (x < g_minMax_l[MINMAX_X][MINMAX_MIN]):
        g_minMax_l[MINMAX_X][MINMAX_MIN] = x
    elif (x > g_minMax_l[MINMAX_X][MINMAX_MAX]):
        g_minMax_l[MINMAX_X][MINMAX_MAX] = x


def initDataStructure2():
    global g_data_d

    g_data_d = {}

    w = 0
    z = 0
    for y in range(len(g_inputLines)):
        # print(line)
        line = g_inputLines[y]
        for x in range(len(line)):
            if (line[x] == '#'):
                setCar2(w, z, y, x, '#')


def initDataStructure():
    global g_data_d

    g_data_d = {}

    z = 0
    for y in range(len(g_inputLines)):
        # print(line)
        line = g_inputLines[y]
        for x in range(len(line)):
            if (line[x] == '#'):
                setCar(z, y, x, '#')


def activeNeighbors2(arg_w, arg_z, arg_y, arg_x, arg_tmp_data_d):
    activeCount = 0
    #print(f"activeNeighbors2 (w:{arg_w}, z:{arg_z}, y:{arg_y}, x:{arg_x})")

    for w in range(arg_w - 1, arg_w + 1 + 1):
        for z in range(arg_z - 1, arg_z + 1 + 1):
            for y in range(arg_y - 1, arg_y + 1 + 1):
                for x in range(arg_x - 1, arg_x + 1 + 1):
                    if (w == arg_w and z == arg_z and y == arg_y and x == arg_x):
                        #print(f"  skip (w:{w}, z:{z}, y:{y}, x:{x})")
                        continue

                    #print(f"  (w:{w}, z:{z}, y:{y}, x:{x})")
                    if (w in arg_tmp_data_d and z in arg_tmp_data_d[w] and y in arg_tmp_data_d[w][z] and x in arg_tmp_data_d[w][z][y] and arg_tmp_data_d[w][z][y][x] == '#'):
                        activeCount += 1

    #print("->", activeCount)
    return activeCount


def activeNeighbors(arg_z, arg_y, arg_x, arg_tmp_data_d):
    activeCount = 0
    #print(f"(z:{arg_z}, y:{arg_y}, x:{arg_x}) = {g_data_l[arg_z][arg_y][arg_x]}")

    for z in range(arg_z-1, arg_z + 1 + 1):
        for y in range(arg_y-1, arg_y + 1 + 1):
            for x in range(arg_x-1, arg_x + 1 + 1):
                if (z == arg_z and y == arg_y and x == arg_x):
                    #print(f"  skip (z:{z}, y:{y}, x:{x})")
                    continue

                if (z in arg_tmp_data_d and y in arg_tmp_data_d[z] and x in arg_tmp_data_d[z][y] and arg_tmp_data_d[z][y][x] == '#'):
                    activeCount += 1

    #print("->", activeCount)
    return activeCount


def show2():
    for w in range(g_minMax_l[MINMAX_W][MINMAX_MIN], g_minMax_l[MINMAX_W][MINMAX_MAX] + 1):
        for z in range(g_minMax_l[MINMAX_Z][MINMAX_MIN], g_minMax_l[MINMAX_Z][MINMAX_MAX] + 1):
            print(f"z={z:2} w={w:2}")

            tmpStr = "  "
            for x in range(g_minMax_l[MINMAX_X][MINMAX_MIN], g_minMax_l[MINMAX_X][MINMAX_MAX] + 1):
                tmpStr += f"{x:2}"
            print(tmpStr)

            for y in range(g_minMax_l[MINMAX_Y][MINMAX_MIN], g_minMax_l[MINMAX_Y][MINMAX_MAX] + 1):
                tmpStr = f"{y:2}"
                for x in range(g_minMax_l[MINMAX_X][MINMAX_MIN], g_minMax_l[MINMAX_X][MINMAX_MAX] + 1):
                    if (w in g_data_d and z in g_data_d[w] and y in g_data_d[w][z] and x in g_data_d[w][z][y] and g_data_d[w][z][y][x] == '#'):
                        tmpStr += " #"
                    else:
                        tmpStr += " ."
                print(tmpStr)
    print()


def show():
    for z in range(g_minMax_l[MINMAX_Z][MINMAX_MIN], g_minMax_l[MINMAX_Z][MINMAX_MAX] + 1):
        print(f"z={z:2}")

        tmpStr = "  "
        for x in range(g_minMax_l[MINMAX_X][MINMAX_MIN], g_minMax_l[MINMAX_X][MINMAX_MAX] + 1):
            tmpStr += f"{x:2}"
        print(tmpStr)

        for y in range(g_minMax_l[MINMAX_Y][MINMAX_MIN], g_minMax_l[MINMAX_Y][MINMAX_MAX] + 1):
            tmpStr = f"{y:2}"
            for x in range(g_minMax_l[MINMAX_X][MINMAX_MIN], g_minMax_l[MINMAX_X][MINMAX_MAX] + 1):
                if (z in g_data_d and y in g_data_d[z] and x in g_data_d[z][y] and g_data_d[z][y][x] == '#'):
                    tmpStr += " #"
                else:
                    tmpStr += " ."
            print(tmpStr)
    print()


def resolve_part2():
    MAX_CYCLE = 6
    print("resolve_part2():")
    print("g_data_d", g_data_d)
    print("g_minMax_l", g_minMax_l)

    show2()

    cycle = 0
    while (cycle < MAX_CYCLE):
        print("### CYCLE", cycle + 1)
        tmp_data_d = copy.deepcopy(g_data_d)
        for w in range(g_minMax_l[MINMAX_W][MINMAX_MIN] - 1, g_minMax_l[MINMAX_W][MINMAX_MAX] + 1 + 1):
            for z in range(g_minMax_l[MINMAX_Z][MINMAX_MIN] - 1, g_minMax_l[MINMAX_Z][MINMAX_MAX] + 1 + 1):
                for y in range(g_minMax_l[MINMAX_Y][MINMAX_MIN] - 1, g_minMax_l[MINMAX_Y][MINMAX_MAX] + 1 + 1):
                    for x in range(g_minMax_l[MINMAX_X][MINMAX_MIN] - 1, g_minMax_l[MINMAX_X][MINMAX_MAX] + 1 + 1):
                        activeNeighbor = activeNeighbors2(w, z, y, x, tmp_data_d)
                        #print(f"({w:2}, {z:2}, {y:2}, {x:2}) -> {activeNeighbor}")
                        if (w in tmp_data_d and z in tmp_data_d[w] and y in tmp_data_d[w][z] and x in tmp_data_d[w][z][y] and tmp_data_d[w][z][y][x] == '#'):
                            if (tmp_data_d[w][z][y][x] == '#' and (activeNeighbor < 2 or activeNeighbor > 3)):
                                setCar2(w, z, y, x, '.')
                            else:
                                if (tmp_data_d[w][z][y][x] == '.' and activeNeighbor == 3):
                                    setCar2(w, z, y, x, '#')
                        else:
                            if (activeNeighbor == 3):
                                setCar2(w, z, y, x, '#')

        cycle += 1
        #show2()

    activeCount = 0
    for w in g_data_d.keys():
        for z in g_data_d[w].keys():
            for y in g_data_d[w][z].keys():
                for x in g_data_d[w][z][y].keys():
                    if (g_data_d[w][z][y][x] == '#'):
                        activeCount += 1

    return activeCount


def resolve_part1():
    MAX_CYCLE = 6
    print("resolve_part1():")
    print("g_data_d", g_data_d)
    print("g_minMax_l", g_minMax_l)

    show()

    cycle = 0
    while (cycle < MAX_CYCLE):
        print("### CYCLE", cycle + 1)
        tmp_data_d = copy.deepcopy(g_data_d)
        for z in range(g_minMax_l[MINMAX_Z][MINMAX_MIN] - 1, g_minMax_l[MINMAX_Z][MINMAX_MAX] + 1 + 1):
            for y in range(g_minMax_l[MINMAX_Y][MINMAX_MIN] - 1, g_minMax_l[MINMAX_Y][MINMAX_MAX] + 1 + 1):
                for x in range(g_minMax_l[MINMAX_X][MINMAX_MIN] - 1, g_minMax_l[MINMAX_X][MINMAX_MAX] + 1 + 1):
                    activeNeighbor = activeNeighbors(z, y, x, tmp_data_d)
                    #print(f"({z}, {y}, {x}) -> {activeNeighbor}")
                    if (z in tmp_data_d and y in tmp_data_d[z] and x in tmp_data_d[z][y]):
                        if (tmp_data_d[z][y][x] == '#' and (activeNeighbor < 2 or activeNeighbor > 3)):
                            setCar(z, y, x, '.')
                        else:
                            if (tmp_data_d[z][y][x] == '.' and activeNeighbor == 3):
                                setCar(z, y, x, '#')
                    else:
                        if (activeNeighbor == 3):
                            setCar(z, y, x, '#')

        cycle += 1
        # show()

    activeCount = 0
    for z in g_data_d.keys():
        for y in g_data_d[z].keys():
            for x in g_data_d[z][y].keys():
                if (g_data_d[z][y][x] == '#'):
                    activeCount += 1

    return activeCount


#g_inputLines = readInputFile("AoC_2020_17_sample.txt")
g_inputLines = readInputFile()

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

# '''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

g_minMax_l = [[0, 0], [0, 0], [0, 0], [0, 0]]
initDataStructure2()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''
