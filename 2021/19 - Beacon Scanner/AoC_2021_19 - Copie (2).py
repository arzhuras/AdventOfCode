import sys
import os
import time
from math import *

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


KEY_BEACON = 0  # liste des tuples de coordonnées des beacon
KEY_OFFSET = 1  #
KEY_ROTATED = 2
KEY_MATCH = 3


def initData():
    g_data["scanner"] = []

    scanner = g_data["scanner"]
    beacon = []
    for line in g_inputLines:
        line = line.rstrip("\n")
        if len(line) == 0:
            scanner.append([beacon, [], []])
            scanner[-1][KEY_OFFSET] = [[0] * len(scanner[-1][KEY_BEACON]) for _ in range(len(scanner[-1][KEY_BEACON]))]
            beacon = []
            continue

        if line[1] == "-":
            continue

        x, y, z = line.split(",")
        beacon.append((int(x), int(y), int(z)))

    scanner.append([beacon, [], []])
    scanner[-1][KEY_OFFSET] = [[0] * len(scanner[-1][KEY_BEACON]) for _ in range(len(scanner[-1][KEY_BEACON]))]

    # scanner[0].append([[1, 2], [2, 3]])
    print("initData:", g_data)

    # print(scanner[0][KEY_BEACON], scanner[0][KEY_DISTANCES], scanner[0][KEY_ROTATED])


##################
### PROCEDURES ###
##################


def calcOffset():
    for scannerId, scanner in enumerate(g_data["scanner"]):
        nbBeacon = len(scanner[KEY_BEACON])
        print("- calcOffset: scanner:", scannerId)
        for i in range(nbBeacon - 1):
            for j in range(i + 1, nbBeacon):
                # print(i, j, scanner[KEY_BEACON][i], scanner[KEY_BEACON][j])
                x1, y1, z1 = scanner[KEY_BEACON][i]
                x2, y2, z2 = scanner[KEY_BEACON][j]
                # distances sqrt[(Xa-Xb)²+(Ya-Yb)²+(Za-Zb)²]
                # scanner[KEY_OFFSET][i][j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
                scanner[KEY_OFFSET][i][j] = (x2 - x1, y2 - y1, z2 - z1)
                scanner[KEY_OFFSET][j][i] = (x1 - x2, y1 - y2, z1 - z2)

        for i in range(nbBeacon):
            print(i, scanner[KEY_OFFSET][i])
        print()


def calcOffset2(beaconLst):
    # scanner = g_data["scanner"][scannerId]

    nbBeacon = len(beaconLst)
    scannerOffsetLst = [[0] * nbBeacon for _ in range(nbBeacon)]

    print("- calcOffset:")
    for i in range(nbBeacon - 1):
        for j in range(i + 1, nbBeacon):
            # print(i, j, scanner[KEY_BEACON][i], scanner[KEY_BEACON][j])
            x1, y1, z1 = beaconLst[i]
            x2, y2, z2 = beaconLst[j]
            # distances sqrt[(Xa-Xb)²+(Ya-Yb)²+(Za-Zb)²]
            # scanner[KEY_OFFSET][i][j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            scannerOffsetLst[i][j] = (x2 - x1, y2 - y1, z2 - z1)
            scannerOffsetLst[j][i] = (x1 - x2, y1 - y2, z1 - z2)

    for i in range(nbBeacon):
        print(i, scannerOffsetLst[i])
    print()

    return scannerOffsetLst


def checkMatch():
    nbBeacon = len(g_data["scanner"][0][KEY_BEACON])
    for scannerIdA in range(len(g_data["scanner"]) - 1):
        scannerA = g_data["scanner"][scannerIdA]
        for scannerIdB in range(scannerIdA, len(g_data["scanner"])):
            scannerB = g_data["scanner"][scannerIdB]

        print("- checkMatch: scanner:", scannerIdA, scannerIdB, nbBeacon)
        matchCount = [0] * nbBeacon
        matchMap = [-1] * nbBeacon
        for i in range(nbBeacon):
            for j in range(i + 1, nbBeacon):

                for k in range(nbBeacon):
                    for l in range(k + 1, nbBeacon):
                        if k == l:
                            break
                        print(
                            i,
                            j,
                            scannerA[KEY_OFFSET][i][j],
                            k,
                            l,
                            scannerB[KEY_OFFSET][k][l],
                            scannerB[KEY_OFFSET][l][k],
                        )

                        if scannerA[KEY_OFFSET][i][j] == scannerB[KEY_OFFSET][k][l]:
                            matchCount[k] += 1
                            matchCount[l] += 1
                            matchMap[i] = k
                            matchMap[j] = l

                            print("GOTCHA 1")
                        elif scannerA[KEY_OFFSET][i][j] == scannerB[KEY_OFFSET][l][k]:
                            matchCount[k] += 1
                            matchCount[l] += 1
                            matchMap[i] = l
                            matchMap[j] = k
                            print("GOTCHA 2")
        print("matchCount:", matchCount)
        print("matchMap:", matchMap)
        for i in range(nbBeacon):
            print(scannerA[KEY_BEACON][i], scannerB[KEY_BEACON][matchMap[i]])


def rotateBeacon(rotateId, beaconLst):
    rotatedBeaconLst = []

    swap = 1 if rotateId < 12 else -1
    rotateId = rotateId % 12

    print("- rotateBeacon:", rotateId, swap)

    for beaconCoord in beaconLst:
        # rotateZ
        if rotateId == 0:  # north
            rotatedBeaconLst.append((beaconCoord[0], beaconCoord[1], swap * beaconCoord[2]))
        elif rotateId == 1:  #  east
            rotatedBeaconLst.append((-beaconCoord[1], beaconCoord[0], swap * beaconCoord[2]))
        elif rotateId == 2:  #  south
            rotatedBeaconLst.append((-beaconCoord[0], -beaconCoord[1], swap * beaconCoord[2]))
        elif rotateId == 3:  # west
            rotatedBeaconLst.append((beaconCoord[1], -beaconCoord[0], swap * beaconCoord[2]))
        # rotateY
        elif rotateId == 4:  # north
            rotatedBeaconLst.append((beaconCoord[0], swap * beaconCoord[1], beaconCoord[2]))
        elif rotateId == 5:  # east
            rotatedBeaconLst.append((-beaconCoord[2], swap * beaconCoord[1], beaconCoord[0]))
        elif rotateId == 6:  # south
            rotatedBeaconLst.append((-beaconCoord[0], swap * beaconCoord[1], -beaconCoord[2]))
        elif rotateId == 7:  # west
            rotatedBeaconLst.append((beaconCoord[2], swap * beaconCoord[1], -beaconCoord[0]))
        # rotateX
        elif rotateId == 8:  # north
            rotatedBeaconLst.append((swap * beaconCoord[0], beaconCoord[1], beaconCoord[2]))
        elif rotateId == 9:  # east
            rotatedBeaconLst.append((swap * beaconCoord[0], -beaconCoord[2], beaconCoord[1]))
        elif rotateId == 10:  # south
            rotatedBeaconLst.append((swap * beaconCoord[0], -beaconCoord[1], -beaconCoord[2]))
        elif rotateId == 11:  # west
            rotatedBeaconLst.append((swap * beaconCoord[0], beaconCoord[2], -beaconCoord[1]))

    return rotatedBeaconLst


def rotateBeacon2(rotateId, beaconLst):
    rotatedBeaconLst = []

    swapFlag = False if rotateId < 12 else True
    faceID = rotateId % 4
    axeSwapId = int(rotateId / 6)

    axeSwapLst = [
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (1, -1, -1),
        (-1, 1, 1),
        (-1, 1, -1),
        # (-1, -1, 1),  # idem 1, 1, 1
        # (-1, -1, -1), # idem 1, 1, -1
    ]

    print("- rotateBeacon:", rotateId, axeSwapId, faceID, axeSwapLst[axeSwapId])

    for beaconCoord in beaconLst:
        # rotateZ
        if faceID == 0:  # north
            rotatedBeaconLst.append(
                (
                    axeSwapLst[axeSwapId][0] * beaconCoord[0],
                    axeSwapLst[axeSwapId][1] * beaconCoord[1],
                    axeSwapLst[axeSwapId][2] * beaconCoord[2],
                )
            )
        elif faceID == 1:  #  east
            rotatedBeaconLst.append(
                (
                    axeSwapLst[axeSwapId][0] * -beaconCoord[1],
                    axeSwapLst[axeSwapId][1] * beaconCoord[0],
                    axeSwapLst[axeSwapId][2] * beaconCoord[2],
                )
            )
        elif faceID == 2:  #  south
            rotatedBeaconLst.append(
                (
                    axeSwapLst[axeSwapId][0] * -beaconCoord[0],
                    axeSwapLst[axeSwapId][1] * -beaconCoord[1],
                    axeSwapLst[axeSwapId][2] * beaconCoord[2],
                )
            )
        elif faceID == 3:  # west
            rotatedBeaconLst.append(
                (
                    axeSwapLst[axeSwapId][0] * beaconCoord[1],
                    axeSwapLst[axeSwapId][1] * -beaconCoord[0],
                    axeSwapLst[axeSwapId][2] * beaconCoord[2],
                )
            )

    return rotatedBeaconLst


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    # calcOffset()
    # checkMatch()

    for scannerId, scanner in enumerate(g_data["scanner"]):
        nbBeacon = len(scanner[KEY_BEACON])
        for rotateId in range(24):
            rotatedBeaconLst = rotateBeacon(rotateId, scanner[KEY_BEACON])
            print(rotateId, rotatedBeaconLst)
            # beaconOffsetLst = calcOffset2(rotatedBeaconLst)
            # print(beaconOffsetLst)
        print()

    return 0


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return 0


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile("sample3.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

"""
transfos = set()
for c in [0, 90, 180, 270]:  # X
    for b in [0, 90, 180, 270]:  # Y
        for a in [0, 90, 180, 270]:  # Z
            rot = (
                cos(a) * cos(b),
                cos(a) * sin(b) * sin(c) - sin(a) * cos(c),
                cos(a) * sin(b) * cos(c) + sin(a) * sin(c),
                sin(a) * cos(b),
                sin(a) * sin(b) * sin(c) + cos(a) * cos(c),
                sin(a) * sin(b) * cos(c) - cos(a) * sin(c),
                -sin(b),
                cos(b) * sin(c),
                cos(b) * cos(c),
            )
            transfos.add(rot)
print(transfos, len(transfos))
"""

exit()
initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
