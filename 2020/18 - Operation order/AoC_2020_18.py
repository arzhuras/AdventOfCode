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
#g_data_d = {}
#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure():
    global g_data_l

    g_data_l = []

    # https://pythex.org/
    # patternField = r"^([a-z ]*): (\d*)-(\d*) or (\d*)-(\d*)"
    for line in g_inputLines:
        # print(line)
        line = line.replace(' ', '')
        g_data_l.append(list(line))

    # print(g_data_l)


def calc2(arg_eq_l, tab=""):
    #print(tab, "# CALC 2", arg_eq_l)
    res = 0

    op = ''
    left = None
    group = 0
    sub_l = []
    mul_l = []
    for elt in arg_eq_l:
        if (group > 0):
            #print(tab, "    group:", group, elt)
            if (elt == ')' and group == 1):
                if (left == None):
                    left = calc2(sub_l, tab + "  ")
                else:
                    right = calc2(sub_l, tab + "  ")
                    if (op == '+'):
                        res = left + right
                        #mul_l.append(res)
                        left = res
                    else:
                        #res = left * right
                        #mul_l.append(left)
                        left = right
                        pass
                    #print(f"{tab}    #1 {left} {op} {right} ->", res)
                    op = ''
                sub_l = []
                group = 0
            else:
                if (elt == '('):
                    group += 1
                elif (elt == ')'):
                    group -= 1
                sub_l.append(elt)
            continue

        if(left == None and elt.isdigit()):
            #print("  left:", elt)
            left = int(elt)
        elif(elt.isdigit() and op != ''):
            #print("  right:", elt)
            right = int(elt)
            if (op == '+'):
                res = left + right
                #mul_l.append(res)
                #print(f"{tab}    #2 {left} {op} {right} ->", res)
                left = int(res)
            else:
                #res = left * right
                #mul_l.append(left)
                left = int(elt)
                #print("new left", left, op)
            op = ''
        elif(elt == '('):
            #print(tab, "  open group:", elt)
            group = 1
        elif (elt == '+'):
            op = '+'
            #print("  op:", op)
        elif (elt == '*'):
            op = '*'
            mul_l.append(left)
            #print("  op:", op)
        else:
            print(tab, "ERROR", elt, left, op, right)
            exit()
    mul_l.append(left)

    res=1
    for num in mul_l:
        res *= num
    #print("mul:", mul_l, res)

    return res


def calc(arg_eq_l, tab=""):
    # print(tab, "# CALC", arg_eq_l)
    res = 0

    op = ''
    left = None
    group = 0
    sub_l = []
    for elt in arg_eq_l:
        if (group > 0):
            #print(tab, "    group:", group, elt)
            if (elt == ')' and group == 1):
                if (left == None):
                    left = calc(sub_l, tab + "  ")
                else:
                    right = calc(sub_l, tab + "  ")
                    if (op == '+'):
                        res = left + right
                    else:
                        res = left * right
                    #print(f"{tab}    {left} {op} {right} ->", res)
                    left = res
                    op = ''
                sub_l = []
                group = 0
            else:
                if (elt == '('):
                    group += 1
                elif (elt == ')'):
                    group -= 1
                sub_l.append(elt)
            continue

        if(left == None and elt.isdigit()):
            #print("  left:", elt)
            left = int(elt)
        elif(elt.isdigit() and op != ''):
            #print("  right:", elt)
            right = int(elt)
            if (op == '+'):
                res = left + right
            else:
                res = left * right
            #print(f"{tab}    {left} {op} {right} ->", res)
            left = res
            op = ''
        elif(elt == '('):
            #print(tab, "  open group:", elt)
            group = 1
        elif (elt == '+'):
            op = '+'
            #print("  op:", op)
        elif (elt == '*'):
            op = '*'
            #print("  op:", op)
        else:
            print(tab, "ERROR", elt, left, op, right)
            exit()

    return res


def resolve_part2():
    #print("resolve_part2():", g_data_l)

    resSum = 0

    print(calc2(['1', '+', '2', '*', '3', '+', '4', '*', '5', '+', '6']))
    print(calc2(['1', '+', '(', '2', '*', '3', ')', '+',
                 '(', '4', '*', '(', '5', '+', '6', ')', ')']))
    print(calc2(['2', '*', '3', '+', '(', '4', '*', '5', ')']))
    print(calc2(['5', '+', '(', '8', '*', '3', '+',
                 '9', '+', '3', '*', '4', '*', '3', ')']))
    print(calc2(['5', '*', '9', '*', '(', '7', '*', '3', '*', '3', '+',
                 '9', '*', '3', '+', '(', '8', '+', '6', '*', '4', ')', ')']))
    print(calc2(['(', '(', '2', '+', '4', '*', '9', ')', '*', '(', '6', '+', '9',
                 '*', '8', '+', '6', ')', '+', '6', ')', '+', '2', '+', '4', '*', '2']))
    
    for eq in g_data_l:
        res = calc2(eq)
        resSum += res
        print(f"{res:5} {resSum:5} {eq}")

    return resSum


def resolve_part1():
    #print("resolve_part1():", g_data_l)
    resSum = 0

    print(calc(['1', '+', '2', '*', '3', '+', '4', '*', '5', '+', '6']))
    print(calc(['1', '+', '(', '2', '*', '3', ')', '+',
                '(', '4', '*', '(', '5', '+', '6', ')', ')']))
    print(calc(['2', '*', '3', '+', '(', '4', '*', '5', ')']))
    print(calc(['5', '+', '(', '8', '*', '3', '+',
                '9', '+', '3', '*', '4', '*', '3', ')']))
    print(calc(['5', '*', '9', '*', '(', '7', '*', '3', '*', '3', '+',
                '9', '*', '3', '+', '(', '8', '+', '6', '*', '4', ')', ')']))
    print(calc(['(', '(', '2', '+', '4', '*', '9', ')', '*', '(', '6', '+', '9',
                '*', '8', '+', '6', ')', '+', '6', ')', '+', '2', '+', '4', '*', '2']))

    for eq in g_data_l:
        res = calc(eq)
        resSum += res
        #print(f"{res:5} {resSum:5} {eq}")

    return resSum


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

print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
