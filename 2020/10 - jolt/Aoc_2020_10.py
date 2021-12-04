import sys, os
import time
import copy

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

inputLines = []

def readInputFile(file = INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines

g_data_l = []

def initDataStructure():
    global g_data_l
    g_data_l = []
    for line in inputLines:
        g_data_l.append(int(line))
    g_data_l.sort()
    #print(g_data_l)

def resolve_part1():
    print("resolve():", len(g_data_l), g_data_l)
    joltDiff = [0, 0, 0]
    curJolt = 0
    diff1=[]
    diff3=[]
    for jolt in g_data_l:
        if (jolt-curJolt == 1):
            diff1.append(jolt)
        if (jolt-curJolt == 3):
            diff3.append([curJolt, jolt])
        joltDiff[jolt-curJolt-1] += 1
        print(curJolt, jolt, joltDiff)
        curJolt = jolt
    joltDiff[2] += 1
    print(joltDiff)
    print("diff1:", len(diff1), diff1)
    print("diff3:", len(diff3), diff3)
    return joltDiff[0] * joltDiff[2]

def checkJolt(arg_curJolt, arg_jolt_l, arg_arrCount, lvl=0):
    #print(lvl, "checkJolt(): ", arg_curJolt, arg_jolt_l, arg_arrCount)
    jolt = arg_jolt_l.pop(0)
    
    if (len(arg_jolt_l) == 0):
        arg_arrCount += 1
        #print(lvl, f"arg_arrCount: {arg_arrCount}")
        return arg_arrCount
    
    arg_arrCount = checkJolt(jolt, copy.deepcopy(arg_jolt_l), arg_arrCount, lvl + 1)

    while len(arg_jolt_l) > 0:
        #print(lvl, arg_curJolt, arg_jolt_l)
        if  arg_jolt_l[0] - arg_curJolt > 2:
            #print(lvl, "break")
            break
        arg_arrCount = checkJolt(jolt, copy.deepcopy(arg_jolt_l), arg_arrCount, lvl + 1)
        arg_jolt_l.pop(0)
    if len(arg_jolt_l) == 0:
        arg_arrCount += 1
        #print(lvl, f"arg_arrCount: {arg_arrCount}")
        return arg_arrCount
    return arg_arrCount

def resolve_part2():
    #print("resolve():", len(g_data_l), g_data_l)
    prevJolt = 0
    sliceStart = 0
    sliceLen = 1
    arrCount = 1
    for jolt in g_data_l:
        #print(prevJolt)
        
        if (jolt-prevJolt == 1):
            sliceLen += 1
            prevJolt = jolt
            continue

        #print("sliceStart:", sliceStart, "sliceLen:", sliceLen)
        if (sliceLen < 3):
            pass
        elif (sliceLen == 3):
            arrCount *= 2
        elif (sliceLen == 4):
            arrCount *= 4
        elif (sliceLen == 5):
            arrCount *= 7
        else:
            print("ERROR")
            exit()

        prevJolt = jolt
        sliceStart = jolt
        sliceLen = 1
    #print("sliceStart:", sliceStart, "sliceLen:", sliceLen)
    if (sliceLen < 3):
        pass
    elif (sliceLen == 3):
        arrCount *= 2
    elif (sliceLen == 4):
        arrCount *= 4
    elif (sliceLen == 5):
        arrCount *= 7
    else:
        print("ERROR")
        exit()
    return arrCount


#inputLines = readInputFile("AoC_2020_10_sample2.txt")
inputLines = readInputFile()

res = -1

###
### PART 1
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
### PART 2
###

print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
