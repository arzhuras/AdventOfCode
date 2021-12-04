import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
print(f"=== {SCRIPT_NAME} ===")


def sandbox():
    print("#### sandbox #####")
    '''
    a = 7
    sum_a = a
    b = 13
    sum_b = b
    c = 19
    sum_c = c
    i = 0
    print(i, a, b)
    while i < 10:
        i += 1
        sum_a += a
        sum_b += b
        sum_c += c
        print(i, sum_a, sum_b, sum_b % a, sum_c % a)

    a = 17
    b = 643
    offset = 17
    sum_a = a
    sum_b = b
    print()
    print(a, b, a * b)
    while (sum_b % a != offset):
        sum_b += b
    print(a, sum_b // a, sum_b // a * a)
    print(b, sum_b // b, sum_b)
    '''
    '''
    a = 17
    b = 643
    offset = 17
    sum_a = a
    sum_b = b
    print()
    print(a, b, a * b)
    count = 0
    while count < 16:
        #sum_a += a
        sum_b += b
        count += 1
        # if (sum_b % a != offset):
        print(count, sum_b, sum_b % a)
        #print("  ", a, sum_a // a, sum_a)
        #print("  ", b, sum_b // b, sum_b)
    '''
    '''
    a = 17
    b = 19
    offset = 3
    sum_a = a
    sum_b = b
    print()
    print(a, b, a * b)
    count = 0
    while count < 11:
        sum_b += b
        if (sum_b % a == offset):
            count += 1
            print(count)
            print("  ", a, sum_b // a, sum_b // a * a)
            print("  ", b, sum_b // b, sum_b)
    '''

def showTable(num_l, numOffset_l, max):
    numLast_l = [0] * len(num_l)
    match = 0
    tmpStr="    "
    prevLast = 0
    print("#############")
    for i in range(len(num_l)):
        tmpStr += f" {num_l[i]:3}"
    print(tmpStr)
    for i in range(max):
        for idx in range(len(num_l)):
            if (i % num_l[idx] == 0):
                #print(i,idx,"D")
                #print("zob", idx, i, numLast_l, numOffset_l[idx], match)
                if (idx == 0):
                    match = 1
                    numLast_l[0] = i
                elif (numLast_l[0] == i - numOffset_l[idx]):
                    match += 1
                    numLast_l[idx] = i
                    #print("echo", idx, i, numLast_l, numOffset_l[idx], match)
        if (match == len(num_l)):
            match = 0
            for i in range(len(numLast_l)):
                tmpStr=f"{numLast_l[i]:4}"
                for j in range(len(numLast_l)):
                    if (i == j):
                        tmpStr += "  D "
                    else:
                        tmpStr += "  . "
                tmpStr += f"{num_l[i]:3} * {int(numLast_l[i] / num_l[i])}"
                if (i == 0):
                    tmpStr += f" delta -> {numLast_l[i] - prevLast} = {num_l[i]} * {int((numLast_l[i] - prevLast)/num_l[i])}"
                print(tmpStr)
                prevLast = numLast_l[0]
            print()


#showTable([17, 13], [0, 2], 600)
#showTable([17, 13, 19], [0, 2, 3], 10000)
#showTable([67, 7], [0, 2], 4500)
#showTable([67, 7, 59], [0, 2, 3], 100000)
#showTable([67, 7, 59, 61], [0, 2, 3, 4], 4200000)


def findModulo(num_l, numOffset_l, maxRound):
    for i in range(len(num_l)):
        print(f"({num_l[i]:2},{numOffset_l[i]:2}) ", end="")
    print()

    pivot = num_l[0]
    curSum = pivot
    curStep = pivot
    for i in range(1, len(num_l)):
        #print(f"### {num_l[i]}, {numOffset_l[i]}")
        #curStep *= num_l[i]
        offset = numOffset_l[i]
        curNum = num_l[i]
        idx = 0
        #print(f"num= {curNum}, sum={curSum}, step={curStep}, pivot={pivot}, offset={offset}, mod={curSum % pivot}")
        while (curSum + offset) % curNum != 0 and idx < maxRound:
            #print(f"  [{idx}], sum={curSum}, step={curStep}, mod={curSum % pivot}")
            idx += 1
            curSum += curStep
        #print(f"-> sum={curSum}, step={curStep}")
        curStep *= curNum
    return curSum

#findModulo([17, 13], [0, 2], 10)
print(findModulo([17, 13, 19], [0, 2, 3], 100))        # 3417
#findModulo([67, 7], [0, 2], 10)
#findModulo([67, 7, 59], [0, 2, 3], 100)
print(findModulo([67, 7, 59, 61], [0, 1, 2, 3], 1000)) # 754 018
print(findModulo([67, 7, 59, 61], [0, 2, 3, 4], 1000)) # 779 210
print(findModulo([67, 7, 59, 61], [0, 1, 3, 4], 1000))  # 1 261 476
print(findModulo([1789, 37, 47, 1889], [0, 1, 2, 3], 1000))  # 1 202 161 486

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
g_baseTimestamp = 0

def initDataStructure():
    global g_data_l
    global g_baseTimestamp
    g_data_l = []
    g_baseTimestamp = int(g_inputLines[0])
    field_l = g_inputLines[1].split(",")
    for field in field_l:
        if (field == 'x'):
            continue
        g_data_l.append(int(field))
    #print(g_baseTimestamp, g_data_l)


def initDataStructure2():
    global g_data_l
    g_data_l = {}
    g_data_l = {"bus": [], "offset": {}}
    field_l = g_inputLines[1].split(",")
    offset = -1
    for field in field_l:
        offset += 1
        if (field == 'x'):
            continue
        g_data_l["bus"].append(int(field))
        g_data_l["offset"][int(field)] = offset
        if (offset == 0):
            g_data_l["pivot"] = int(field)
    #g_data_l["bus"].sort(reverse=True)
    if (g_data_l["bus"][0] != g_data_l["pivot"]):
        g_data_l["greater"] = g_data_l["bus"][0]
    else:
        g_data_l["greater"] = g_data_l["bus"][1]
    # print(g_data_l)


def initFirstCommon():
    pivot = g_data_l["pivot"]
    g_data_l["base_ref"] = {}
    for bus in g_data_l["bus"]:
        offset = g_data_l["offset"][bus]
        sum_bus = bus
        while(sum_bus < offset):
            sum_bus += bus

        if (offset >= pivot):
            offset = offset % pivot

        print()
        print(pivot, bus, sum_bus, g_data_l["offset"][bus], offset, sum_bus % pivot)
        idx = 0
        while sum_bus % pivot != offset and idx < 2000:
            #print(idx, sum_bus, pivot, sum_bus % pivot, bus, offset)
            #print("  ", pivot, sum_bus // pivot, sum_bus // pivot * pivot)
            #print("  ", bus, sum_bus // bus, sum_bus)
            idx += 1
            sum_bus += bus
        if (sum_bus % pivot != offset):
            print(sum_bus, "NOGOOD")
        else:
            print("GOOD", sum_bus/bus, sum_bus, sum_bus - g_data_l["offset"][bus], (sum_bus - g_data_l["offset"][bus]) / pivot,
                  (idx+1) * bus, sum_bus // pivot * pivot)
        # exit()
        g_data_l["base_ref"][bus] = sum_bus // pivot * pivot
    print(g_data_l)
    #exit()


def resolve_part2():
    print("resolve_part2():", g_data_l)

    initFirstCommon()

    pivot = g_data_l["pivot"]
    matchCount = 0
    base_ref_d = g_data_l["base_ref"]
    cur_sum = base_ref_d[g_data_l["greater"]]
    sum_step = g_data_l["greater"] * pivot
    print("->", cur_sum, sum_step)
    while matchCount != len(g_data_l["bus"]):
        cur_sum += sum_step
        matchCount = 0
        for bus in g_data_l["bus"]:
            base_ref = base_ref_d[bus]
            delta = cur_sum - base_ref
            # print("#", cur_sum, bus, base_ref, delta)
            if (delta < bus):
                #print("  break: delta < bus", cur_sum, bus, base_ref, delta)
                break
            #print(delta % bus)
            if (delta % bus != 0):
                #print("  break %", cur_sum, base_ref)
                break
            matchCount += 1
    print(cur_sum, matchCount)

    return cur_sum


def resolve_part1():
    print("resolve_part1():", g_baseTimestamp, len(g_data_l), g_data_l)

    bestTimestamp = 0
    bestBus = 0
    for bus in g_data_l:
        #print(g_baseTimestamp,bus, g_baseTimestamp // bus, g_baseTimestamp % bus)
        nextTimestamp = ((g_baseTimestamp // bus) * bus) + bus
        #print(bus, nextTimestamp)
        if (bestTimestamp == 0 or nextTimestamp < bestTimestamp):
            bestTimestamp = nextTimestamp
            bestBus = bus
            # print("#", bestBus, bestTimestamp)
    return bestBus * (bestTimestamp - g_baseTimestamp)


#g_inputLines = readInputFile("AoC_2020_13_sample2.txt")
#g_inputLines = readInputFile("AoC_2020_13_sample3.txt")
#g_inputLines = readInputFile("AoC_2020_13_sample4.txt")
#g_inputLines = readInputFile("AoC_2020_13_sample5.txt")
#g_inputLines = readInputFile("AoC_2020_13_sample6.txt")
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

#initDataStructure2()
#res = resolve_part2()
res = findModulo([17, 41, 643, 23, 13, 29, 433, 37, 19], [0, 7, 17, 25, 30, 46, 48, 54, 67], 10000)  # 1 202 161 486

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
