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
g_data_l = []
g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure(arg_data):
    global g_data_l
    g_data_l = []

    g_data_l = arg_data

    print(g_data_l)


def resolve_part2():
    #print("resolve_part2():", g_data_l)

    return -1


def resolve_part1(arg_num_t, arg_max):
    print("resolve_part1():", arg_num_t, arg_max)

    lastRound_d = {}
    nextNum_d = {}
    firstTime = True
    for round in range(1, len(arg_num_t) + 1):
        num = arg_num_t[round - 1]
        lastRound_d[num] = round
        #print(f"[{round}] {num:2} {lastRound_d[num]:2} {prevLastRound_d[num]:2} {firstTime}")

    for round in range(len(arg_num_t) + 1, arg_max + 1):
        if (firstTime):
            num = 0
        else:
            num = nextNum_d[num]

        if (num not in lastRound_d):
            firstTime = True
        else:
            firstTime = False
            nextNum_d[num] = round - lastRound_d[num]
        lastRound_d[num] = round
        #print(f"[{round}] {num:2} {lastRound_d[num]:2} {prevLastRound_d[num]:2} {firstTime}")
    
    return num


#g_inputLines = readInputFile("AoC_2020_14_sample2.txt")
#g_inputLines = readInputFile("AoC_2020_14_sample.txt")
#g_inputLines = readInputFile()

res = -1

###
# PART 1
###

print()
print(f"### PART 1 ###")

tic = time.perf_counter()

#initDataStructure()
# initDataStructure()
print(resolve_part1((0, 3, 6), 2020))
print(resolve_part1((1, 3, 2), 2020))
print(resolve_part1((2, 1, 3), 2020))
print(resolve_part1((1, 2, 3), 2020))
print(resolve_part1((2, 3, 1), 2020))
print(resolve_part1((3, 2, 1), 2020))
print(resolve_part1((3, 1, 2), 2020))


res = resolve_part1((0,13,16,17,1,10,6), 2020)
toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")

###
# PART 2
###

print()
print(f"### PART 2 ###")

#print(resolve_part1((0, 3, 6), 30000000))

tic = time.perf_counter()

# initDataStructure()
res = resolve_part1((0,13,16,17,1,10,6), 30000000)

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
