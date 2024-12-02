from tools import *
import time
import math
import copy

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

    # grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# MATRIX2D_COLORSET = {"#": Ansi.cyan}
# from matrix3d import *


def initData():
    data.fields = []

    for line in data.rawInput:
        # line = line.replace(".","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        # intFields = list(map(int,line.split()))
        data.fields.append(list(map(int,line.split())))

    #print("fields:", data.fields)

    # data.grid = []
    # data.grid = loadMatrix2d(inputFile)[0]
    # showGrid(data.grid)

    # data.grids = []
    # data.grids = loadMatrix2d(inputFile)
    # showGridLst(data.grid)


##################
### PROCEDURES ###
##################

def checkReport(report):
    #print("   ", report)
    flagDec = False
    flagInc = False
    for levelIdx in range(1,len(report)):
        delta = report[levelIdx] - report[levelIdx-1]
        if delta < 0 :
            if flagInc == True:
                #print(f"    {report} DEC: {levelIdx+1}")
                return "DEC", levelIdx
            flagDec = True
        if delta > 0 :
            if flagDec == True:
                #print(f"    {report} INC: {levelIdx+1}")
                return "INC", levelIdx
            flagInc = True
        if abs(delta) < 1 or abs(delta) > 3:
            #print(f"    {report} DELTA {delta}: {levelIdx+1}")
            return f"DELTA {delta}",levelIdx
    #print(f"    {report} OK")
    return "OK",-1


def resolve_part1():
    return(sum(is_safe(report) for report in data.fields))

    safeCount = 0

    for reportIdx, report in enumerate(data.fields):
        res = checkReport(report)
        if res[0] == "OK" :
            #print(f"{Ansi.green}{reportIdx:04} -> {report}{Ansi.norm} SAFE")
            safeCount += 1
        else:
            #print(f"{Ansi.red}{reportIdx:04} -> {report[0:res[1]]}{Ansi.norm},{Ansi.yellow}{report[res[1]]}{Ansi.norm},{Ansi.red}{report[res[1]+1:]}{Ansi.norm} UNSAFE {res[0]} {res[1]+1}")
            pass

    return safeCount


def resolve_part2():
    directSafeCount = 0
    skippedSafeCount = 0

    for reportIdx, report in enumerate(data.fields):
        res = checkReport(report)
        if res[0] == "OK" :
            #print(f"{Ansi.green}{reportIdx:04} -> {report}{Ansi.norm} DIRECT SAFE")
            directSafeCount += 1
        else:
            #skip a level n, n-1, n-2
            for skip in (res[1], res[1]-1, res[1]-2):
                res2 = checkReport(report[0:skip] + report[skip+1:])
                if res2[0] == "OK":
                    #print(f"{Ansi.green}{reportIdx:04} -> {report[0:skip]}{Ansi.norm},{Ansi.yellow}{report[skip]}{Ansi.norm},{Ansi.green}{report[skip+1:]}{Ansi.norm} SKIPPED SAFE {skip+1}")
                    skippedSafeCount += 1
                    break
            # unsafe
            if res2[0] != "OK":
                #print(f"{Ansi.red}{reportIdx:04} -> {report[0:res[1]]}{Ansi.norm},{Ansi.yellow}{report[res[1]]}{Ansi.norm},{Ansi.red}{report[res[1]+1:]}{Ansi.norm} UNSAFE {res[0]} {res[1]+1}")
                pass

    return f"{Ansi.green}Direct: {directSafeCount}{Ansi.norm} - {Ansi.yellow}Skipped: {skippedSafeCount}{Ansi.norm} - {Ansi.blue}Total: {directSafeCount + skippedSafeCount}{Ansi.norm}"


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None


# part1 avec des sets!!!
def is_safe(row):
    inc = {row[i + 1] - row[i] for i in range(len(row) - 1)}
    return inc <= {1, 2, 3} or inc <= {-1, -2, -3}

print(type(is_safe(report) for report in data.fields))
print(sum(is_safe(report) for report in data.fields))

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.6f}s): {Ansi.blue}{res}{Ansi.norm}")

#exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.6f}s): {Ansi.blue}{res}{Ansi.norm}")
