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

PRG_INS = 0
PRG_ARG = 1
g_prg_l = []

def initDataStructure():
    global g_prg_l
    g_prg_l = []
    for line in inputLines:
        field = line.split()
        #print(field)
        g_prg_l.append([field[0], int(field[1])])
    #print(g_prg_l)

def validate_prg(arg_idx, arg_acc):
    idx = arg_idx
    acc = arg_acc
    maxIdx = len(g_prg_l)
    prg_exec_l = [False] * maxIdx

    while idx < maxIdx:
        #print(f"> {g_prg_l[idx][PRG_INS]} {g_prg_l[idx][PRG_ARG]:2} {prg_exec_l[idx]:5} before: idx= {idx}, acc= {acc}")
        if (prg_exec_l[idx] == True):
            #print(f"INFINITE [{idx}]= {acc}")
            return {"idx" : idx, "acc" : acc, "valid" : False}
        
        prg_exec_l[idx] = True
        if (g_prg_l[idx][PRG_INS] == 'acc'):
            acc += g_prg_l[idx][PRG_ARG]
            idx += 1
            #print(f"idx={idx}, acc={acc}")
        elif (g_prg_l[idx][PRG_INS] == 'jmp'):
            idx += g_prg_l[idx][PRG_ARG]
            #print(f"idx={idx}, acc={acc}")
        elif (g_prg_l[idx][PRG_INS] == 'nop'):
            idx += 1

    return {"idx" : idx, "acc" : acc, "valid" : True}

def resolve_part1():
    res = validate_prg(arg_idx=0, arg_acc=0)
    return res["acc"]

def resolve_part2():
    idx = 0
    acc = 0
    maxIdx = len(g_prg_l)
    prg_exec_l = [False] * maxIdx

    while idx < maxIdx:
        #print(f"> {g_prg_l[idx][PRG_INS]} {g_prg_l[idx][PRG_ARG]:2} {g_prg_l[idx][PRG_EXECUTED]:5} before: idx= {idx}, acc= {acc}")
        if (prg_exec_l[idx] == True):
            print(f"ERROR [{idx}]= {acc}") # impossible d'être la normalement :)
            break

        prg_exec_l[idx] = True
        if (g_prg_l[idx][PRG_INS] == 'acc'):
            acc += g_prg_l[idx][PRG_ARG]
            idx += 1
            #print(f"idx={idx}, acc={acc}")
        else:
            # on simule avec le jump
            res = validate_prg(arg_idx=idx+g_prg_l[idx][PRG_ARG], arg_acc=acc)
            if (res["valid"] == True):
                print(f"FAULT INSTRUCTION FOUND: {g_prg_l[idx]}")
                idx = maxIdx
                acc = res["acc"]
                break

            # on simule avec le nop
            res = validate_prg(arg_idx=idx+1, arg_acc=acc)
            if (res["valid"] == True):
                print(f"FAULT INSTRUCTION FOUND: [{idx}] : {g_prg_l[idx]}")
                idx = maxIdx
                acc = res["acc"]
                break
            # les simulation on échouée, on continue normalement
            if (g_prg_l[idx][PRG_INS] == 'jmp'):
                idx += g_prg_l[idx][PRG_ARG]
                #print(f"idx={idx}, acc={acc}")
            elif (g_prg_l[idx][PRG_INS] == 'nop'):
                idx += 1
    return acc

#inputLines = readInputFile("AoC_2020_8_sample.txt")
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
