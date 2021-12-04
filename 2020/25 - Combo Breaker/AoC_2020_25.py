import sys
import os
import time
import re
import copy
import math

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
g_grid_d = {}
g_flipCount_d = {}

# g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure():

    return - 1

def transform(subject_number, loop_size):
    value = 1

    for round in range(1, loop_size+1):
        value *= subject_number
        value = value % 20201227
        #print(f"[{round}]", value)

    return value

def searchLoopSize(pub_key, subject_number, max_round):
    value = 1

    round = 1
    while round < max_round:
        value *= subject_number
        value = value % 20201227
        #print(f"[{round}]", value)
        if (value == pub_key): 
            #print(pub_key, "-> loop size = ", round)
            return round
        round += 1
    
    return -1


def resolve_part2():

    return -1


def resolve_part1(card_pub, door_pub):
    print(f"resolve_part1(): card_pub: {card_pub}, door_pub: {door_pub}")

    #print("trans:", transform(7, 11))

    #res = searchLoopSize(17807724, 7, 100000)
    #print(17807724, "-> loop size = ", res)
    
    cardLoopSize = searchLoopSize(card_pub, 7, 100000000)
    print(card_pub, "-> loop size = ", cardLoopSize)

    #print("trans:", transform(7, cardLoopSize))

    doorLoopSize = searchLoopSize(door_pub, 7, 10000000000)
    print(door_pub, "-> loop size = ", doorLoopSize)

    res = transform(door_pub, cardLoopSize)

    return res


#g_inputLines = readInputFile("AoC_2020_24_sample.txt")
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
res = resolve_part1(11349501, 5107328)

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''

###
# PART 2
###

'''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

# initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
'''
