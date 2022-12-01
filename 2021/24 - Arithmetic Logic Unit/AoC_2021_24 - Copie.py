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
    g_data["var"] = [0, 0, 0, 0]

    for line in g_inputLines:
        if len(line) == 5:  # INP
            g_data["alu"].append((INS_DIC["inp"], VAR_DIC[line[4]], line))
        else:
            ins, var1, var2 = line.split()
            if var2 in ("w", "x", "y", "z"):
                var2IsVal = not IS_VAL
                var2 = VAR_DIC[var2]
            else:
                var2IsVal = IS_VAL
                var2 = int(var2)
            g_data["alu"].append((INS_DIC[ins], VAR_DIC[var1], var2IsVal, var2, line))
        # print(f"{line:10}: {g_data['alu'][-1]}")

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################

g_depth = [0] * 15


def runMonad(
    curInsIdx=0,
    var=[0, 0, 0, 0],
    depth=0,
):
    if depth >= 15:
        print(ANSI_RED, "MAX DEPTH", ANSI_NORM)
        return False, ""

    tab = "  " * depth
    # print(f"{ANSI_BLUE}{tab}MONAD {depth} {curInsIdx}{ANSI_NORM}")
    tab += "  "

    alu = g_data["alu"]
    # var = g_data["var"]
    while curInsIdx < len(alu):
        curIns = alu[curInsIdx]
        # print(curInsIdx, curIns)
        if curIns[0] == 0:  # INP
            if depth == 14:
                print(f"{tab}{ANSI_RED}[{curInsIdx}] {str(curIns[:-1]):20} {str(curIns[-1]):10}-> MaxDepth{ANSI_NORM}")
                return False, ""
            for curDigit in range(9, 0, -1):
                g_depth[depth] = curDigit
                var[curIns[1]] = curDigit
                # print(
                # f"{tab}{ANSI_BLUE}[{curInsIdx}] {str(curIns[:-1]):20} {str(curIns[-1]):10}-> {curDigit} {var}{ANSI_NORM}"
                # )
                if depth <= 7:
                    print(
                        f"{tab}{ANSI_BLUE}[{curInsIdx}] depth:{depth} {g_depth} {curDigit} {var}{ANSI_NORM} {time.time() - startTime:.3f}s"
                    )
                res = runMonad(curInsIdx + 1, var.copy(), depth + 1)
                if res[0] == True:
                    return True, str(curDigit) + res[1]  # found a valid model
            g_depth[depth] = 0
            return False, ""  # no valid model found
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
                        return False, ""
                    var[curIns[1]] = int(var[curIns[1]] / curIns[3])
                else:
                    if var[curIns[3]] == 0:
                        print(ANSI_RED, "DIVIDE BY ZERO", ANSI_NORM)
                        return False, ""
                    var[curIns[1]] = int(var[curIns[1]] / var[curIns[3]])
            elif curIns[0] == 4:  # MOD
                if curIns[2] == IS_VAL:
                    if curIns[3] <= 0:
                        print(ANSI_RED, "MOD <= 0", ANSI_NORM)
                        return False, ""
                    var[curIns[1]] %= curIns[3]
                else:
                    if var[curIns[3]] <= 0:
                        print(ANSI_RED, "MOD <= 0", ANSI_NORM)
                        return False, ""
                    var[curIns[1]] %= var[curIns[3]]
            elif curIns[0] == 5:  # EQL
                if curIns[2] == IS_VAL:
                    var[curIns[1]] = 1 if var[curIns[1]] == curIns[3] else 0
                else:
                    var[curIns[1]] = 1 if var[curIns[1]] == var[curIns[3]] else 0
        # print(f"{tab}[{curInsIdx}] {str(curIns[:-1]):20} {str(curIns[-1]):10}-> {var}")
        curInsIdx += 1

    if var[3] == 0:
        print(f"{tab}{ANSI_GREEN} VALID [{curInsIdx}] {str(curIns[:-1]):20} {str(curIns[-1]):10}-> {var}{ANSI_NORM}")
        return True, ""  # valid model
    else:
        # print(f"{tab}{ANSI_GREY} INVALID [{curInsIdx}] {str(curIns[:-1]):20} {str(curIns[-1]):10}-> {var}{ANSI_NORM}")
        return False, ""  # invalid model


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    res = runMonad()

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
