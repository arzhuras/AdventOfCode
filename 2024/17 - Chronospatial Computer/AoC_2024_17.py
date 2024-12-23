import copy
import math
import time
from collections import defaultdict

from tools import *

# import re

# from collections import deque
# import operator
# opFunc = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# from functools import reduce
# import itertools


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    fields = None
    line = None
    gridLst = None
    grid = None

    A = None
    B = None
    C = None
    program = None
    pointer = None
    out = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}
# from matrix3d import *


def initData():
    data.A = int(data.rawInput[0][12:])
    data.B = int(data.rawInput[1][12:])
    data.C = int(data.rawInput[2][12:])
    data.program = list(map(int, data.rawInput[4][9:].split(",")))
    data.pointer = 0
    data.out = []

    # print(data.A, data.B, data.C, data.program)


##################
### PROCEDURES ###
##################


def getCombo(operand):
    if operand >= 0 and operand <= 3:
        combo = operand
    elif operand == 4:
        combo = data.A
    elif operand == 5:
        combo = data.B
    elif operand == 6:
        combo = data.C
    else:
        print("INVALID COMBO", operand)
        exit()
    return combo


def resolve_part1():
    if False:
        data.C = 9
        program = [2, 6]

        data.A = 10
        program = [5, 0, 5, 1, 5, 4]

        data.A = 2024
        program = [0, 1, 5, 4, 3, 0]

        data.B = 29
        program = [1, 7]

        data.B = 2024
        data.C = 43690
        program = [4, 0]

    execute()

    # print()
    print(Ansi.green, "FINAL", data.A, data.B, data.C, data.out, Ansi.norm)
    out1 = ""
    for elt in data.out:
        out1 = out1 + str(elt) + ","

    return out1[:-1]


def execute(part2=False):
    pointer = 0
    while pointer < len(data.program) - 1:
        # print(
        # "->", pointer, data.program[pointer], "-", data.A, data.B, data.C, data.out
        # )
        opcode = data.program[pointer]
        operand = data.program[pointer + 1]
        if opcode == 0:
            combo = getCombo(operand)
            A = data.A
            res = A // (2**combo)
            data.A = res
            # print(f"  ADV {operand}: {A} // {2**combo} = {res} -> A")
        elif opcode == 1:
            B = data.B
            res = B ^ operand
            data.B = res
            # print(f"  BXL {operand}: {B} ^ {operand} = {res} -> B")
        elif opcode == 2:
            combo = getCombo(operand)
            res = combo % 8
            data.B = res
            # print(f"  BST {operand}: {combo} % 8 = {res} -> B")
        elif opcode == 3:
            if data.A == 0:
                pass
                # print(f"  JNZ SKIP {data.A}")
            else:
                pointer = operand
                # print(f"  JNZ JUMP {operand}")
                continue
        elif opcode == 4:
            B = data.B
            C = data.C
            res = B ^ C
            data.B = res
            # print(f"  BXC {operand}: {B} ^ {C} = {res} -> B")
        elif opcode == 5:
            combo = getCombo(operand)
            res = combo % 8
            data.out.append(res)
            idx = len(data.out) - 1
            # print(f"  OUT {operand}: {combo} % 8 = {res}", idx)
            if part2 == True:
                if idx < len(data.program) and data.program[idx] != res:
                    return False
                if len(data.out) == len(data.program):
                    return True
        elif opcode == 6:
            combo = getCombo(operand)
            A = data.A
            res = A // (2**combo)
            data.B = res
            # print(f"  BDV {operand}: {A} // {2**combo} = {res} -> B")
        elif opcode == 7:
            combo = getCombo(operand)
            A = data.A
            res = A // (2**combo)
            data.C = res
            # print(f"  CDV {operand}: {A} // {2**combo} = {res} -> C")
        pointer += 2
    return False


def resolve_part2():
    if False:
        # data.A = 2024
        data.A = 117440
        data.B = 0
        data.C = 0
        data.out = []
        data.program = [0, 3, 5, 4, 3, 0]

    print(Ansi.yellow, data.program, Ansi.norm)
    for A in range(100_000_000):
        # for A in range(117440 - 2, 117440 + 2):
        # for A in range(500_000_000, 1_000_000_000):

        if A % 100_000 == 0:
            print(f"{A:_}")
        data.A = A
        data.B = 0
        data.C = 0
        data.out = []
        res = execute(part2=False)
        if (
            (len(data.out) == 1 and data.out[0] == data.program[0])
            or (
                len(data.out) == 2
                and data.out[0] == data.program[0]
                and data.out[1] == data.program[1]
            )
            or (
                len(data.out) == 3
                and data.out[0] == data.program[0]
                and data.out[1] == data.program[1]
                and data.out[2] == data.program[2]
            )
            or (
                len(data.out) == 4
                and data.out[0] == data.program[0]
                and data.out[1] == data.program[1]
                and data.out[2] == data.program[2]
                and data.out[3] == data.program[3]
            )
            or (
                len(data.out) >= 5
                and data.out[0] == data.program[0]
                and data.out[1] == data.program[1]
                and data.out[2] == data.program[2]
                and data.out[3] == data.program[3]
                and data.out[4] == data.program[4]
            )
        ):
            print(
                Ansi.blue,
                A,
                ":",
                data.A,
                data.B,
                data.C,
                data.program,
                data.out,
                Ansi.norm,
            )
        if res == True:
            pass
            print(Ansi.yellow, "PROGRAM EQUAL", A, Ansi.norm)
            return A
        else:
            pass
            # print(Ansi.red, "PROGRAM DIFF", A, Ansi.norm)

    # print()
    print(Ansi.green, "FINAL", data.A, data.B, data.C, data.out, Ansi.norm)

    return A


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)
# data.gridLst = loadMatrix2d(inputFile)


### PART 1 ###
print(sys.argv[0])
year, dayTitle = os.path.dirname(sys.argv[0]).split("\\")[-2:]
print(Ansi.green, f"--- {year} {dayTitle} ---", Ansi.norm)
print(Ansi.red, "### PART 1 ###", Ansi.norm)

initData()
startTime = time.time()
res1 = resolve_part1()
# res1, res2 = resolve_bothpart()
endTime = time.time()

print(f"-> part 1 ({endTime - startTime:.6f}s): {Ansi.blue}{res1}{Ansi.norm}")

### PART 2 ###
print(Ansi.red, "### PART 2 ###", Ansi.norm)

initData()
startTime = time.time()
res2 = resolve_part2()
endTime = time.time()

print(f"-> part 2 ({endTime - startTime:.6f}s): {Ansi.blue}{res2}{Ansi.norm}")
