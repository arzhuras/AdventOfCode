from tools import *
#from matrix2d import *
#from matrix3d import *

import time
#from collections import deque
#import operator

#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = None
    line = None

    bluePrint = None # Dict list

data = Data()


def initData():
    data.line = []
    data.bluePrint = []
    tmpDict = {}

    for line in data.rawInput:
        if line == "":
            data.bluePrint.append(tmpDict)    
            tmpDict = {}
            continue

        line = line.replace(".","")
        line = line.replace(":","")
        # line = line.replace(",","")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        line = line.replace("Each","")
        line = line.replace("robot costs","")
        line = line.replace("and","")
        data.line.append(line)

        fields = line.split()
        if fields[0] == "Blueprint" :
            continue
        
        tmpDict[fields[0]] = {}
        for i  in range(1, len(fields[1:]), 2):
            tmpDict[fields[0]][fields[i+1]] = int(fields[i])
    data.bluePrint.append(tmpDict)    
    tmpDict = {}
        

    #print("initData:", data.line)
    for i in range(len(data.bluePrint)):
        print(f"[{i}]")
        bp = data.bluePrint[i]
        for elt in bp.keys():
            print(f"  {elt:8s} -> {bp[elt]}")


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    return None


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"

# MAX_ROUND = 1000
# inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
