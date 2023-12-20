from tools import *
import time
import math
import copy

from collections import deque
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
    modules = None

    # grid = None


data = Data()

###  /modules libraries ###
# from matrix2d import *
# from matrix3d import *

BROADCASTER = "broadcaster"
FLIP = "FLIP"
CONJ = "CONJ"
PULSE_OFF = 0
PULSE_ON = 1
PULSE_MAP = ["low", "high"]

MOD_TYPE = 0
MOD_DESTS = 1

FLIP_STATE = 2

CONJ_INPUT = 2


def initData():
    data.modules = {}

    conj = []
    for line in data.rawInput:
        line = line.replace("-", "")
        line = line.replace(">", "")
        line = line.replace(",", "")
        # line = line.replace(";","")
        # line = line.replace("="," ")
        # intFields = list(map(int,line.split()))
        fields = line.split()
        if fields[0][0] == "%":  # modType, dests, state
            data.modules[fields[0][1:]] = [
                FLIP, list(fields[1:]), PULSE_OFF]
        elif fields[0][0] == "&":  # modType, dests, input last pulse dict
            data.modules[fields[0][1:]] = [
                CONJ, list(fields[1:]), {}]
            conj.append(fields[0][1:])
        else:  # type, dest
            data.modules[BROADCASTER] = [
                BROADCASTER, list(fields[1:])]

    for src, value in data.modules.items():
        # print(key, value)
        for dest in value[MOD_DESTS]:
            if dest in conj:
                data.modules[dest][CONJ_INPUT][src] = PULSE_OFF

    print("modules:", data.modules)


##################
### PROCEDURES ###
##################

def resolve_part1():
    # global BROADCASTER, FLIP, CONJ
    modules = data.modules

    pulseCnt = [0, 0]
    for i in range(1000):
        stack = deque([(BROADCASTER, PULSE_OFF, "button")])
        pulseCnt[PULSE_OFF] += 1
        # print(modules)
        # print(f"{Ansi.blue}{i+1})\nbutton -low-> broadcaster{Ansi.norm} {pulseCnt}")

        while len(stack) > 0:
            # print(stack)
            moduleName, inPulse, src = stack.popleft()

            if moduleName not in modules:
                print("SKIP", moduleName)
                # pulseCnt[inPulse] -= 1
                continue

            module = modules[moduleName]
            modType = module[MOD_TYPE]
            modDests = module[MOD_DESTS]
            # print(moduleName, inPulse, module, pulseCnt)

            # module[MOD_LAST] = inPulse

            if modType == BROADCASTER:
                outPulse = inPulse

            elif module[MOD_TYPE] == FLIP:
                if inPulse == PULSE_ON:
                    continue

                outPulse = PULSE_ON if module[FLIP_STATE] == PULSE_OFF else PULSE_OFF
                module[FLIP_STATE] = outPulse
                # print("  ", modules[module])

            else:  # CONJUNCTION module
                module[CONJ_INPUT][src] = inPulse

                outPulse = PULSE_OFF
                for inputLast in module[CONJ_INPUT].values():
                    if inputLast == PULSE_OFF:
                        outPulse = PULSE_ON
                        break

            for dest in modDests:
                stack.append((dest, outPulse, moduleName))
                pulseCnt[outPulse] += 1
                # print(f"{Ansi.cyan}{modType} {
                # moduleName} -{PULSE_MAP[outPulse]}-> {dest}{Ansi.norm} {pulseCnt}")

    print(pulseCnt)
    return math.prod(pulseCnt)


def resolve_part2():

    return None


############
### MAIN ###
############

# MAX_ROUND = 10
inputFile = "sample.txt"
inputFile = "sample2.txt"

# MAX_ROUND = 1000
inputFile = "input.txt"

data.rawInput = readInputFile(inputFile)

initData()
res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve_part1()
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
res = resolve_part2()
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
