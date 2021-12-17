import sys
import os
import time
import math

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


def decodeLiteral(packet, tab="  "):
    print(f"{tab}decodeLiteral: {packet}")
    cursor = 0
    tmpStr = ""
    while packet[cursor] == "1":
        cursor += 1
        tmpStr += packet[cursor : cursor + 4]
        cursor += 4
    cursor += 1
    tmpStr += packet[cursor : cursor + 4]
    cursor += 4

    val = int(tmpStr, 2)

    print(f"{tab} -> cursor: {cursor}, valLst: {[val]}")
    return cursor, [val]


def decodeOperator(packet, tab="  "):

    cursor = 0
    valLst = []
    if packet[cursor] == "0":  # total lengths in bits
        cursor += 1
        bitLen = int(packet[cursor : cursor + 15], 2)
        cursor += 15
        print(f"{tab}decodeOperator: bitLen: {bitLen} {packet[0]} {packet[1:16]} {packet[cursor:]}")
        endCursor = cursor + bitLen
        while cursor < endCursor:
            res, resValLst = decodePacket(packet[cursor:endCursor], tab + "  ")
            cursor += res
            valLst += resValLst
    else:
        cursor += 1
        subpacketCnt = int(packet[cursor : cursor + 11], 2)
        cursor += 11
        print(f"{tab}decodeOperator: subpacketCnt: {subpacketCnt} {packet[0]} {packet[1:11]} {packet[cursor:]}")

        for _ in range(subpacketCnt):
            res, resValLst = decodePacket(packet[cursor:], tab + "  ")
            cursor += res
            valLst += resValLst

    print(f"{tab} -> cursor: {cursor}, valLst: {valLst}")
    return cursor, valLst


def decodePacket(packet, tab="  "):
    global g_packetVersionSum
    packetVersion = int(packet[0:3], 2)
    g_packetVersionSum += packetVersion
    packetType = int(packet[3:6], 2)
    cursor = 6
    print(f"{tab}decodePacket - ver: {packetVersion}, type: {packetType}, {packet[0:3]} {packet[3:6]} {packet[6:]}")

    # decode
    if packetType == 4:
        res, valLst = decodeLiteral(packet[cursor:], tab + "  ")
    else:
        res, valLst = decodeOperator(packet[cursor:], tab + "  ")
        if packetType == 0:  # sum
            valLst = [sum(valLst)]
        elif packetType == 1:  # product
            valLst = [math.prod(valLst)]
        elif packetType == 2:  # minimum
            valLst = [min(valLst)]
        elif packetType == 3:  # maximum
            valLst = [max(valLst)]
        elif packetType == 5:  # greater than
            valLst = [1 if valLst[0] > valLst[1] else 0]
        elif packetType == 6:  # less than
            valLst = [1 if valLst[0] < valLst[1] else 0]
        elif packetType == 7:  # equals
            valLst = [1 if valLst[0] == valLst[1] else 0]
    cursor += res

    print(f"{tab} -> cursor: {cursor}, valLst: {valLst}")
    return cursor, valLst


g_packetVersionSum = 0


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    global g_packetVersionSum
    for transmission in g_data["line"]:
        g_packetVersionSum = 0

        # conversion hexa
        packet = ""
        for hexdigit in transmission:
            packet += f"{int(hexdigit, 16):04b}"  # gère les leading zéro

        # header
        print(f"transmission: {transmission}")
        print(f"  binaire: {packet}")

        res, valLst = decodePacket(packet)

        print(f"  SKIP {packet[res:]}")
        print(f"{ANSI_BLUE}-> {g_packetVersionSum}{ANSI_NORM}")
        print()

    return g_packetVersionSum


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    global g_packetVersionSum
    for transmission in g_data["line"]:
        g_packetVersionSum = 0

        # conversion hexa
        packet = ""
        for hexdigit in transmission:
            packet += f"{int(hexdigit, 16):04b}"  # gère les leading zéro

        # header
        print(f"transmission: {transmission}")
        print(f"  binaire: {packet}")

        res, valLst = decodePacket(packet)

        print(f"  SKIP {packet[res:]}")
        print(f"{ANSI_BLUE}-> {valLst[0]}{ANSI_NORM}")
        print()

    return valLst[0]


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

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
