import sys
import os
import time
import re
import copy 

from collections import namedtuple
from bitarray import bitarray

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


def initDataStructure():
    global g_data_l
    g_data_l = []

    # https://pythex.org/
    patternMem = r"^(mem)\[(\d*)] *= *(\d*)"
    patternMask = r"^(mask) *= *([\d|X]*)"
    for line in g_inputLines:
        # print(line)
        result = re.match(patternMem, line)
        if (result):
            g_data_l.append(g_cmd_nt(result.group(1), int(
                result.group(2)), int(result.group(3))))
            # print("# MEM:", g_data_l[-1].name, g_data_l[-1].arg1, g_data_l[-1].arg2)
        else:
            result = re.match(patternMask, line)
            if (result):
                g_data_l.append(
                    g_cmd_nt(result.group(1), str(result.group(2)), 0))
                # print("# MASK", g_data_l[-1].name, g_data_l[-1].arg1, g_data_l[-1].arg2)

    # print(g_data_l)


def resolve_part2():
    #print("resolve_part2():", g_data_l)

    mask = ()
    memory = {}
    for cmd in g_data_l:
        # print(cmd)
        if (cmd.name == "mask"):
            mask = tuple(cmd.arg1)
            floatingCount = mask.count('X')
            #print(f"# MASK              {floatingCount} {mask}")
            continue

        address = list(bin(cmd.arg1)[2:])
        address = ['0'] * (36-len(address)) + address
        #print(f"# MEM {cmd.arg1:5} {cmd.arg2:9} {address}")

        #print(f"  MASK                {mask}")
        #print(f"  ADD1                {address}")
        for i in range(36):
            if (mask[i] == '1'):
                address[i] = '1'
        #print(f"  ADD2                {address}")

        target = [copy.deepcopy(address) for i in range(2 ** floatingCount)]
        #print(target)
        for j in range(2 ** floatingCount):
            jStr="0" * 10 + bin(j)[2:]
            k=1
            for i in range(36):
                if (mask[i] == 'X'):
                    #print(j, i, jStr, k, jStr[-k])
                    target[j][i] = jStr[-k]
                    k += 1
        #for i in range(len(target)): print(f"[{i:2}] {target[i]}")

        #exit()

        for add in target:
            newAdd = ''.join(add)
            #print(newAdd, int(newAdd, 2))
            memory[int(newAdd, 2)] = cmd.arg2
            #print(memory)
        #exit()
    #print(len(memory.keys()))

    return sum(memory.values())


def resolve_part1():
    #print("resolve_part1():", g_data_l)

    mask = ()
    memory = {}
    for cmd in g_data_l:
        # print(cmd)
        if (cmd.name == "mask"):
            mask = tuple(cmd.arg1)
            # print(f"# MASK                {mask}")
            continue

        value = list(bin(cmd.arg2)[2:])
        value = ['0'] * (36-len(value)) + value
        # print(f"# MEM {cmd.arg1:5} {cmd.arg2:9} {value}")

        for i in range(36):
            if (mask[i] != 'X'):
                value[i] = mask[i]
        #print(f"                      {mask}")
        #print(f"                      {value}")

        newValue = ''.join(value)
        #print(newValue, int(newValue, 2))
        memory[cmd.arg1] = int(newValue, 2)
    #print(memory, len(memory.keys()))

    return sum(memory.values())


#g_inputLines = readInputFile("AoC_2020_14_sample2.txt")
#g_inputLines = readInputFile("AoC_2020_14_sample.txt")
g_inputLines = readInputFile()

res = -1

a = bitarray()
a.frombytes(b'123')
print(a)

tmpStr = bin(5)[2:]
print(tmpStr, int(tmpStr, 2))

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
