import sys
import os
import time

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


def initDataStructure():
    global g_data_l
    g_data_l = []
    for line in g_inputLines:
        g_data_l.append((line[0], int(line[1:])))
    # print(g_data_l)


def resolve_part2():
    #print("resolve_part1():", len(g_data_l), g_data_l, g_adj_l)

    waypoint_ew = 10  # EAST
    waypoint_ns = 1  # NORTH
    pos_ew = 0
    pos_ns = 0

    #print(f"      : POS({pos_ew:3},{pos_ns:3}) WP({waypoint_ew:3},{waypoint_ns:3})")
    for cmd, arg in g_data_l:
        #print("->", cmd, arg)
        if (cmd == "L" or cmd == "R"):
            if (cmd == "L"):
                arg = 360 - arg
            for _ in range(arg // 90):
                tmp = waypoint_ew
                waypoint_ew = waypoint_ns
                waypoint_ns = -tmp
                #print("90:", waypoint_ew, waypoint_ns)
        elif (cmd == 'N'):
            waypoint_ns += arg
        elif (cmd == 'S'):
            waypoint_ns -= arg
        elif (cmd == 'E'):
            waypoint_ew += arg
        elif (cmd == 'W'):
            waypoint_ew -= arg
        elif (cmd == 'F'):
            pos_ns += arg * waypoint_ns
            pos_ew += arg * waypoint_ew
        #print(f"{cmd} {arg:3} : POS({pos_ew:3},{pos_ns:3}) WP({waypoint_ew:3},{waypoint_ns:3})")

    print(f"POS({pos_ew:3},{pos_ns:3}) WP({waypoint_ew:3},{waypoint_ns:3})")
    return abs(pos_ew) + abs(pos_ns)


def resolve_part1():
    #print("resolve_part1():", len(g_data_l), g_data_l, g_adj_l)

    pos_ew = 0
    pos_ns = 0
    heading = 90  # EAST

    for cmd, arg in g_data_l:
        #print("->", cmd, arg)
        if (cmd == "L" or cmd == "R"):
            if (cmd == "L"):
                heading += 360 - arg
            else:
                heading += arg
            heading %= 360
        elif (cmd == 'N'):
            pos_ns += arg
        elif (cmd == 'S'):
            pos_ns -= arg
        elif (cmd == 'E'):
            pos_ew += arg
        elif (cmd == 'W'):
            pos_ew -= arg
        elif (cmd == 'F'):
            if (heading == 0):
                pos_ns += arg
            elif (heading == 90):
                pos_ew += arg
            elif (heading == 180):
                pos_ns -= arg
            else:
                pos_ew -= arg
        #print(f"{cmd} {arg:3} : ES={pos_ew:3} NS={pos_ns:3} heading={heading}")

    print(f"ES={pos_ew:3} NS={pos_ns:3} heading={heading}")
    return abs(pos_ew) + abs(pos_ns)


#inputLines = readInputFile("AoC_2020_12_sample.txt")
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

print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
