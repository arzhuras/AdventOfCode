import sys
import os
import time
import re
import copy

from collections import namedtuple

ANSI_NORM = "\033[0m"
#ANSI_GREEN = "\033[32;1;4m"
#ANSI_RED = "\033[31;1;4m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

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
#g_data_d = {}
#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure():
    global g_data_d

    g_data_d = {}
    g_data_d["rules"] = {}
    g_data_d["msg"] = []

    # https://pythex.org/
    #patternRule = r"^(\d*): (\d*) (\d*) \| (\d*)-(\d*)"
    for i in range(len(g_inputLines)):
        line = g_inputLines[i]
        # print(line)

        if (line == ''):
            break
        line = line.replace(':', '')
        line = line.replace('"', '')
        field = line.split()

        if (field[1].isalpha()):
            g_data_d["rules"][int(field[0])] = field[1]
        else:
            group = 0
            tmp_l = []
            g_data_d["rules"][int(field[0])] = []
            # print(field[1:])
            for num in field[1:]:
                if (num == '|'):
                    g_data_d["rules"][int(field[0])].append(tmp_l)
                    group += 1
                    tmp_l = []
                else:
                    tmp_l.append(int(num))
                    # print(tmp_l)
            g_data_d["rules"][int(field[0])].append(tmp_l)

    for i in range(i+1, len(g_inputLines)):
        line = g_inputLines[i]
        # print(line)

        g_data_d["msg"].append(line)
    '''
    for key, value in g_data_d["rules"].items():
        print(f"[{key}] - {value}")

    print()
    for i in range(len(g_data_d["msg"])):
        print(f"[{i}] - {g_data_d['msg'][i]}")
    '''


def tree(arg_rule, arg_tab=""):
    #print(f"{arg_tab}# {arg_rule} ")

    rules = g_data_d["rules"]

    #print(f"{arg_tab}RULE {rules[arg_rule]}")
    if (type(rules[arg_rule]) is str):
        #print(f"{arg_tab}{arg_rule} = {rules[arg_rule]}")
        print(f"{arg_tab}tree({arg_rule})", [rules[arg_rule]])
        return [rules[arg_rule]]

    ruleLst = []
    resLst = []
    for grpIdx in range(len(rules[arg_rule])):
        group = rules[arg_rule][grpIdx]
        print(f"{arg_tab}{arg_rule}[{grpIdx}] = {group}")

        groupLst = []
        for ruleIdx in range(len(group)):
            rule = group[ruleIdx]
            resLst = tree(rule, arg_tab + "  ")
            #print(f"{arg_tab}group", groupLst)
            if (len(groupLst) == 0):
                groupLst = resLst
                #print(f"{arg_tab}1st",groupLst)
            else:
                tmpLst = []
                print(groupLst, resLst)
                for a in groupLst:
                    for b in resLst:
                        tmpLst.append(a + " " + b)
                groupLst = tmpLst
                print(f"{arg_tab} group {arg_rule}[{grpIdx}] = {groupLst}")
            #print(f"{arg_tab}group {rule}[{grpIdx}]{groupLst}")
        #print(f"{arg_tab}rule", ruleLst)
        ruleLst += groupLst
        #print(f"{arg_tab}rule {arg_rule}[{grpIdx}]", ruleLst)

    print(f"{arg_tab}tree({arg_rule})", ruleLst)
    return ruleLst

def tree2(arg_rule, arg_tab=""):
    #print(f"{arg_tab}# {arg_rule} ")

    rules = g_data_d["rules"]

    #print(f"{arg_tab}RULE {rules[arg_rule]}")
    if (type(rules[arg_rule]) is str):
        #print(f"{arg_tab}{arg_rule} = {rules[arg_rule]}")
        print(f"{arg_tab}tree({arg_rule})", [rules[arg_rule]])
        return [rules[arg_rule]]

    ruleLst = []
    resLst = []
    for grpIdx in range(len(rules[arg_rule])):
        group = rules[arg_rule][grpIdx]
        print(f"{arg_tab}{arg_rule}[{grpIdx}] = {group}")

        groupLst = []
        for ruleIdx in range(len(group)):
            rule = group[ruleIdx]
            resLst = tree(rule, arg_tab + "  ")
            #print(f"{arg_tab}group", groupLst)
            if (len(groupLst) == 0):
                groupLst = resLst
                #print(f"{arg_tab}1st",groupLst)
            else:
                tmpLst = []
                print(groupLst, resLst)
                for a in groupLst:
                    for b in resLst:
                        tmpLst.append(a + " " + b)
                groupLst = tmpLst
                print(f"{arg_tab} group {arg_rule}[{grpIdx}] = {groupLst}")
            #print(f"{arg_tab}group {rule}[{grpIdx}]{groupLst}")
        #print(f"{arg_tab}rule", ruleLst)
        ruleLst += groupLst
        #print(f"{arg_tab}rule {arg_rule}[{grpIdx}]", ruleLst)

    print(f"{arg_tab}tree({arg_rule})", ruleLst)
    return ruleLst

def valid(arg_rule, arg_idx, arg_msg, arg_tab=""):
    #print(f"{arg_tab}# {arg_rule} {arg_idx} {arg_msg[arg_idx:]}")
    # print(f"{arg_tab}# {arg_rule} {arg_idx} {arg_msg}")

    rules = g_data_d["rules"]

    if (arg_idx >= len(arg_msg)):
        return -1
        
    #print(f"{arg_tab}RULE {rules[arg_rule]}")
    if (type(rules[arg_rule]) is str):
        if(arg_msg[arg_idx] == rules[arg_rule]):
            print(f"{arg_tab}# {arg_rule} OK")
            return arg_idx
        return -1

    for grpIdx in range(len(rules[arg_rule])):
        group = rules[arg_rule][grpIdx]
        print(f"{arg_tab}# {arg_rule}:{grpIdx} {group} {arg_idx} {arg_msg[arg_idx:]}")
        #print(f"{arg_tab}RULE {arg_rule} -> [{grpIdx}]{group}")
        validCount = 0
        curIdx = arg_idx
        res = -1
        for ruleIdx in range(len(group)):
            rule = group[ruleIdx]
            #print(f"{arg_tab}TEST {rule} {curIdx}")
            res = valid(rule, curIdx, arg_msg, arg_tab + "  ")
            if(res != -1):
                #print(f"{arg_tab}VALID {rule}")
                validCount += 1
                curIdx = res + 1
            else:
                #print(f"{arg_tab}NOT VALID {rule}")
                break
            print(f"{arg_tab} validCount:{validCount}, len(group):{len(group)} {arg_rule}:{grpIdx} {ruleIdx} {group}")
        if (validCount == len(group)):
            break

    if (validCount == len(group)):
        print(f"{arg_tab} {ANSI_BLUE}-> {arg_rule}:{grpIdx} OK ({arg_idx},{curIdx - 1})={arg_msg[arg_idx:curIdx]}{ANSI_NORM}")
        return curIdx - 1
    else:
        print(f"{arg_tab} -> {arg_rule}:{grpIdx} KO {-1}")
        return -1

def resolve_part2():
    # print("resolve_part2():", g_data_d}

    #print(valid(0, 0, "babbbbaabbbbbabbbbbbaabaaabaaa"))
    #return 0

    res = 0
    validCount = 0
    #for i in range(len(g_data_d["msg"])):
    for i in range(2):
        msg = g_data_d['msg'][i]
        #print(f"[{i}] - {msg}")
        res = valid(0, 0, msg)
        if (res == len(msg) - 1):
            validCount += 1
            print(f"{ANSI_GREEN}### MSG VALID {msg}{ANSI_NORM}")
        else:
            print(f"{ANSI_RED}### MSG NOT VALID {msg}{ANSI_NORM}")
            pass
        # print()

    return validCount

def resolve_part1():
    #print("resolve_part1():", g_data_d)

    res = 0
    validCount = 0
    for i in range(len(g_data_d["msg"])):
        msg = g_data_d['msg'][i]
        #print(f"[{i}] - {msg}")
        res = valid(0, 0, msg)
        if (res == len(msg) - 1):
            validCount += 1
            print(f"{ANSI_GREEN}### MSG VALID {msg}{ANSI_NORM}")
        else:
            print(f"{ANSI_RED}### MSG NOT VALID {msg}{ANSI_NORM}")
            pass
        # print()

    return validCount


g_inputLines = readInputFile("AoC_2020_19_sample3.txt")
#g_inputLines = readInputFile("AoC_2020_19_sample2.txt")
#g_inputLines = readInputFile()

#initDataStructure()
#res=tree(0)
#print()
#print("###")
#for toto in res:
    #print(toto)
#exit()

res = -1

###
# PART 1
###

'''
print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")
'''

###
# PART 2
###

#'''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
print("before  8:", g_data_d["rules"][8])  #  8 : [[42]]
g_data_d["rules"][8].append([42, 8])
print("after   8:", g_data_d["rules"][8])   #  8 : [[42], [42, 8]]
print("before 11:", g_data_d["rules"][11]) # 11 : [[42, 31]]
g_data_d["rules"][11].append([42, 11, 31])
print("after  11:", g_data_d["rules"][11])  # 11 : [[42, 31], [42, 11, 31]]

res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
#'''

'''
initDataStructure()
res=tree(42)
print()
print("###")
for toto in res:
    print(toto)
exit()
'''