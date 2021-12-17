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
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

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


def initData():
    g_data["line"] = []

    for line in g_inputLines:
        g_data["line"].append(line)

    print("initData:", g_data)


##################
### PROCEDURES ###
##################


def decodeType4(packet):
    print("decodeType4:", packet)
    idx = 0

    tmpStr = ""
    while True:
        tmpStr += packet[idx + 1 : idx + 5]
        if packet[idx] == "0":
            break
        idx += 5
    val = int(tmpStr, 2)
    print(f"  {val}")

    return val


def decodeType6(packet):
    pass


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    for transmission in g_data["line"]:

        # conversion hexa
        packet = ""
        for hexdigit in transmission:
            packet += f"{int(hexdigit, 16):04b}"  # gère les leading zéro

        # header
        packetVersion = int(packet[0:3], 2)
        packetType = int(packet[3:6], 2)
        print(f"transmission: {transmission}")
        print(f"  binaire: {packet[0:3]} {packet[3:6]} {packet[6:]}")
        print(f"  version: {packetVersion}, type: {packetType}")

        # decode
        if packetType == 4:
            decodeType4(packet[6:])
        elif packetType == 6:
            decodeType6(packet[6:])
        else:
            print(ANSI_RED, "DECODE ERROR", ANSI_NORM)

    return 0


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return 0


############
### MAIN ###
############

g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
