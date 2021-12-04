import sys, os
import time

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
        #print(field)
        g_data_l.append(int(line))
    #print(g_data_l)

def resolve(arg_sliceWidth):
    res1 = -1
    res2 = -1
    #part1
    for idx in range(arg_sliceWidth, len(g_data_l)):
        preamble_l = g_data_l[idx - arg_sliceWidth : idx]
        sum_l = []
        #print("preamble:", preamble_l)
        for i in range(arg_sliceWidth):
            for j in range(1, arg_sliceWidth):
                tmpInt = preamble_l[i] + preamble_l[j]
                if (tmpInt not in sum_l):
                    sum_l.append(tmpInt)
        sum_l.sort()
        #print(sum_l)
        if (g_data_l[idx] in sum_l):
            #print(f"OK : {g_data_l[idx]}")
            pass
        else:
            res1 = g_data_l[idx]
            print(f"NOK: {res1}")
            break
        #print()

    #part2
    print(g_data_l)
    for idx in range(len(g_data_l)):
        curSum = g_data_l[idx]
        idx2 = idx
        while curSum < res1:
            idx2 += 1
            curSum += g_data_l[idx2]
        #print(f"idx= {idx}, [idx]= {g_data_l[idx]}, idx2= {idx2}, [idx2]= {g_data_l[idx2]}, curSum= {curSum}")
        if (curSum == res1):
            print(sum(g_data_l[idx:idx2+1]), g_data_l[idx:idx2+1])
            res2=min(g_data_l[idx:idx2+1]) + max(g_data_l[idx:idx2+1])
            break
        curSum = 0
    return [res1, res2]

#inputLines = readInputFile("AoC_2020_9_sample.txt")
#codeRange = 5
inputLines = readInputFile()
codeRange = 25
res = -1

###
### PART 1
###

print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve(codeRange)

toc = time.perf_counter()

print(f"-> result part 1 = {res[0]}")
print(f"-> result part 1 = {res[1]}")
print(f"{toc - tic:0.4f} seconds")
