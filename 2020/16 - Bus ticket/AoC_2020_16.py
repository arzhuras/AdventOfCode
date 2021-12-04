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
#g_data_l = []
g_field_d = {}
g_ticket_l = []
g_nearby_l = []
#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure():
    #global g_data_l
    global g_field_d
    global g_ticket_l
    global g_nearby_l

    #g_data_l = []
    g_field_d = {}
    g_ticket_l = []
    g_nearby_l = []

    # https://pythex.org/
    patternField = r"^([a-z ]*): (\d*)-(\d*) or (\d*)-(\d*)"
    for i in range(len(g_inputLines)):
        line = g_inputLines[i]
        i += 1
        # print(line)
        if (line == ""):
            break
        result = re.match(patternField, line)
        g_field_d[result.group(1)] = [(int(result.group(2)), int(
            result.group(3))), (int(result.group(4)), int(result.group(5)))]

    for i in range(i+1, len(g_inputLines)):
        line = g_inputLines[i]
        i += 1
        # print(line)
        if (line == ""):
            break

        g_ticket_l = [int(num) for num in line.split(",")]

    for i in range(i+1, len(g_inputLines)):
        line = g_inputLines[i]
        i += 1
        # print(line)
        if (line == ""):
            break

        g_nearby_l.append([int(num) for num in line.split(",")])

    #print("# FIELD ", g_field_d)
    #print("# TICKET ", g_ticket_l)
    #print("# NEARBY ", g_nearby_l)
    # print(g_data_l)


def checkValidity():
    errorRate = 0
    invalidCount = 0
    for i in range(len(g_nearby_l)):
        nearbyTicket = g_nearby_l[i - invalidCount]
        #print("nearbyTicket", nearbyTicket)
        for field in nearbyTicket:
            #print(" field", field)
            valid = False
            for rule_t in g_field_d.values():
                #print("  rule_t", rule_t)
                if ((field >= rule_t[0][0] and field <= rule_t[0][1]) or
                        (field >= rule_t[1][0] and field <= rule_t[1][1])):
                    valid = True
                    break
            if (valid == False):
                #print("ERROR", i, field, errorRate, invalidCount)
                g_nearby_l.pop(i - invalidCount)
                errorRate += field
                invalidCount += 1
                break

    return errorRate


def resolve_part2():
    #print("resolve_part2():", g_nearby_l)

    #print(g_nearby_l)
    checkValidity()
    #print(g_nearby_l)

    rejected_l = [[] for _ in g_nearby_l[0]]
    #print(g_field_d)
    for nearbyTicket in g_nearby_l:
        #print("nearbyTicket", nearbyTicket)
        for fieldIdx in range(len(nearbyTicket)):
            field = nearbyTicket[fieldIdx]
            #print(" field", field)
            for ruleName, rule_t in g_field_d.items():
                #print("  rule_t", rule_t)
                if ((field >= rule_t[0][0] and field <= rule_t[0][1]) or
                        (field >= rule_t[1][0] and field <= rule_t[1][1])):
                    pass
                    #print(f"MATCH [{fieldIdx}] {field:3} {ruleName:10} {rule_t}")
                else:
                    #print(f"NOMATCH [{fieldIdx}] {field:3} {ruleName:10} {rule_t}")

                    if (ruleName not in rejected_l):
                        rejected_l[fieldIdx].append(ruleName)
    
    nbField = len(rejected_l)
    found = 0
    valid_l = [[] for _ in range(nbField)]
    #print("###", rejected_l)
    while found < nbField:
        for pos in range(len(rejected_l)):
            rejected = rejected_l[pos]
            #print("rejected ", pos, rejected)
            if (len(rejected) == 0):
                #print(" done")
                continue
            if (len(rejected) == nbField - 1):
                #print(" full")
                for field in g_field_d.keys():
                    #print("  field", field)
                    if (field not in rejected):
                        found += 1
                        #print("   FOUND !!! ", pos, field)
                        valid_l[pos] = field
                        for rej in rejected_l:
                            #print("    rej", pos, field, rej)
                            if (field not in rej):
                                rej.append(field)
                                #print("###", rejected_l)
    #print(rejected_l)
    print(valid_l)
    score = 1
    for i in range(len(valid_l)):
        if (valid_l[i].split()[0] == "departure"):
            print(valid_l[i], g_ticket_l[i])
            score *= g_ticket_l[i]

    return score


def resolve_part1():
    #print("resolve_part1():", g_data_l)

    return checkValidity()


#g_inputLines = readInputFile("AoC_2020_16_sample2.txt")
#g_inputLines = readInputFile("AoC_2020_16_sample.txt")
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
