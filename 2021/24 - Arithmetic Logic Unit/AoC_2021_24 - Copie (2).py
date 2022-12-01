import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

ANSI_NORM = "\033[0m"
ANSI_GREY = "\033[30;1m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_YELLOW = "\033[33;1m"
ANSI_BLUE = "\033[34;1m"
ANSI_PURPLE = "\033[35;1m"
ANSI_CYAN = "\033[36;1m"

g_inputLines = []


def readInputFile(argFile=INPUT_FILE_NAME):
    inputLines = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    print(f"  {len(inputLines)} lignes")
    # print(inputLines)
    return inputLines


#############################
### INITIALISATION & DATA ###
#############################

g_data = {}

IS_VAL = True

INS_DIC = {"inp": 0, "add": 1, "mul": 2, "div": 3, "mod": 4, "eql": 5}
VAR_DIC = {"w": 0, "x": 1, "y": 2, "z": 3}


def initData():
    g_data["alu"] = []
    # g_data["var"] = [0, 0, 0, 0]

    alu = g_data["alu"]
    idx = -1
    for line in g_inputLines:
        if len(line) == 5:  # INP
            alu.append([])
            idx = len(alu) - 1
            alu[idx].append((INS_DIC["inp"], VAR_DIC[line[4]], line))
        else:
            ins, var1, var2 = line.split()
            if var2 in ("w", "x", "y", "z"):
                var2IsVal = not IS_VAL
                var2 = VAR_DIC[var2]
            else:
                var2IsVal = IS_VAL
                var2 = int(var2)
            alu[idx].append((INS_DIC[ins], VAR_DIC[var1], var2IsVal, var2, line))
        # print(f"{line:10}: {g_data['alu'][-1]}")

    if False:
        for idx, block in enumerate(alu):
            print("###", idx)
            for ins in block:
                print(ins)
            print()


##################
### PROCEDURES ###
##################

g_depth = [0] * 15


def runMonad(aluIdx, digit, var):
    # print(f"{ANSI_BLUE}-> {aluIdx} {digit} {var}{ANSI_NORM}")

    alu = g_data["alu"]
    for curIns in alu[aluIdx]:
        # print(f"  [{aluIdx}] {curIns}")
        if curIns[0] == 0:  # INP
            var[curIns[1]] = digit
        else:
            if curIns[0] == 1:  # ADD
                if curIns[2] == IS_VAL:
                    var[curIns[1]] += curIns[3]
                else:
                    var[curIns[1]] += var[curIns[3]]
            elif curIns[0] == 2:  # MUL
                if curIns[2] == IS_VAL:
                    var[curIns[1]] *= curIns[3]
                else:
                    var[curIns[1]] *= var[curIns[3]]
            elif curIns[0] == 3:  # DIV
                if curIns[2] == IS_VAL:
                    if curIns[3] == 0:
                        print(ANSI_RED, "DIVIDE BY ZERO", ANSI_NORM)
                        return []
                    var[curIns[1]] = int(var[curIns[1]] / curIns[3])
                else:
                    if var[curIns[3]] == 0:
                        print(ANSI_RED, "DIVIDE BY ZERO", ANSI_NORM)
                        return []
                    var[curIns[1]] = int(var[curIns[1]] / var[curIns[3]])
            elif curIns[0] == 4:  # MOD
                if curIns[2] == IS_VAL:
                    if curIns[3] <= 0:
                        print(ANSI_RED, "MOD <= 0", ANSI_NORM)
                        return []
                    var[curIns[1]] %= curIns[3]
                else:
                    if var[curIns[3]] <= 0:
                        print(ANSI_RED, "MOD <= 0", ANSI_NORM)
                        return []
                    var[curIns[1]] %= var[curIns[3]]
            elif curIns[0] == 5:  # EQL
                if curIns[2] == IS_VAL:
                    var[curIns[1]] = 1 if var[curIns[1]] == curIns[3] else 0
                else:
                    var[curIns[1]] = 1 if var[curIns[1]] == var[curIns[3]] else 0
        # print(f" {str(curIns[:-1]):20} [{aluIdx}] {str(curIns[-1]):10}-> {var}")

    return var


g_divZ = [1, 1, 1, 1, 1, 26, 1, 26, 26, 1, 26, 26, 26, 26]
g_addX = [13, 11, 12, 10, 14, -1, 14, -16, -8, 12, -16, -13, -6, -6]
g_addY = [6, 11, 5, 6, 8, 14, 9, 4, 7, 13, 11, 11, 6, 1]


def runMonadOptim(step, digit, z):
    # print("runMonadOptim:", step, digit, z)
    x = z % 26
    x += g_addX[step]

    if g_divZ[step] != 1:
        z = int(z / 26)
    if x != digit:
        z *= 26
        z += g_addY[step] + digit

    return z


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    zInputLst = []
    zInputLst.append([0] * 10)
    # print(zInputLst)
    for step in range(14):
        print(f"{ANSI_BLUE}### Step: {step}{ANSI_NORM}")
        zInputLst.append([])
        for digit in range(1, 10):
            # res = runMonad(step, digit, [666, 777, 888, zInputLst[step][digit - 1]])
            # print(f"[{step}] {digit} - z:{zInputLst[step][digit - 1]} -> {res}")
            # zInputLst[step + 1].append(res[3])
            res = runMonadOptim(step, digit, zInputLst[step][digit - 1])
            print(f"[{step}] {digit} - z:{zInputLst[step][digit - 1]} -> {res} optim")
            zInputLst[step + 1].append(res)
        print()
    print(zInputLst)

    return res


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return 0


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile("sample3.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

exit()
# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
