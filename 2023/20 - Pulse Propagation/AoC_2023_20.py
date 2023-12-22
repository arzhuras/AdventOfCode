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

    # part 2
    rxAncestor = ""
    inversorNames = []
    inversorCycles = []


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
    data.rxAncestor = ""
    data.inversorNames = []
    data.inversorCycles = []

    conj = []
    for line in data.rawInput:
        line = line.replace("-", "")
        line = line.replace(">", "")
        line = line.replace(",", "")
        fields = line.split()

        # recherche de l'ancestor de 'rx' pour la partie 2
        if fields[1] == "rx":
            data.rxAncestor = fields[0][1:]

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

        # recherche des inverseurs pour la partie 2
        if data.rxAncestor in value[MOD_DESTS]:
            data.inversorNames.append(src)

    # print("modules:", data.modules)


# construit une edge list à partir de l'input pour le site de dessin de graphe: https://graphonline.ru/fr/
# il doit être aussi possible d'utiliser le module python graphviz
def edgeList():
    for moduleName, module in data.modules.items():
        # print(moduleName, module[MOD_TYPE], module[MOD_DESTS])
        for dest in module[MOD_DESTS]:
            if moduleName == "broadcaster":
                print(f"brd>{dest}")
            else:
                if module[MOD_TYPE] == FLIP:
                    print(f"{moduleName}>{dest}")
                else:
                    print(f"{moduleName}>{dest}")

##################
### PROCEDURES ###
##################


def resolve(buttonPress):
    modules = data.modules
    # print(modules)

    pulseCnt = [0, 0]
    for buttonPressCnt in range(buttonPress):
        stack = deque([(BROADCASTER, PULSE_OFF, "button")])
        pulseCnt[PULSE_OFF] += 1
        # print(f"{Ansi.blue}{i+1})\nbutton -low-> broadcaster{Ansi.norm} {pulseCnt}")

        while len(stack) > 0:
            # print(stack)
            moduleName, inPulse, src = stack.popleft()

            if moduleName not in modules:
                # print("SKIP", moduleName, inPulse, src)
                continue

            module = modules[moduleName]
            modType = module[MOD_TYPE]
            modDests = module[MOD_DESTS]
            # print(moduleName, inPulse, module, pulseCnt)

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

                # part 2: cycle monitoring of inversors
                if moduleName in data.inversorNames:
                    if outPulse == 1:
                        print("cycle", moduleName, buttonPressCnt+1)
                        data.inversorCycles.append(buttonPressCnt+1)

            for dest in modDests:
                stack.append((dest, outPulse, moduleName))
                pulseCnt[outPulse] += 1
                # print(f"{Ansi.cyan}{modType} {
                # moduleName} -{PULSE_MAP[outPulse]}-> {dest}{Ansi.norm} {pulseCnt}")

            if len(data.inversorCycles) == 4:
                break

    print("pulseCnt", pulseCnt)
    print("inversorCycles", data.inversorCycles)
    return (math.prod(pulseCnt), math.lcm(*data.inversorCycles))


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

edgeList()

res = None

### PART 1 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 1 ###", Ansi.norm)
res = resolve(1000)
print()
print(
    f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res[0]}{Ansi.norm}")

# exit()

initData()
res = None

### PART 2 ###
startTime = time.time()
print()
print(Ansi.red, "### PART 2 ###", Ansi.norm)
print("rxAncestor", data.rxAncestor)
print("inversorNames", data.inversorNames)
res = resolve(10000)
print()
print(
    f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res[1]}{Ansi.norm}")
