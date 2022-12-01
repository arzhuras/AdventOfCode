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
    # print("initData:", g_data)
    for id, elt in enumerate(g_data["scanner"]):
        print("Scanner:", id, "nbBeacon:", len(elt[KEY_BEACON]))

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


def calcOffset2(beaconLst):
    # scanner = g_data["scanner"][scannerId]

    nbBeacon = len(beaconLst)
    scannerOffsetLst = [[0] * nbBeacon for _ in range(nbBeacon)]

    # print("- calcOffset:")
    for i in range(nbBeacon - 1):
        for j in range(i + 1, nbBeacon):
            # print(i, j, scanner[KEY_BEACON][i], scanner[KEY_BEACON][j])
            x1, y1, z1 = beaconLst[i]
            x2, y2, z2 = beaconLst[j]
            # distances sqrt[(Xa-Xb)²+(Ya-Yb)²+(Za-Zb)²]
            # scanner[KEY_OFFSET][i][j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            scannerOffsetLst[i][j] = (x2 - x1, y2 - y1, z2 - z1)
            scannerOffsetLst[j][i] = (x1 - x2, y1 - y2, z1 - z2)

    # for i in range(nbBeacon):
    # print(i, scannerOffsetLst[i])
    # print()

    return scannerOffsetLst


def rotateBeacon(rotateId, beaconLst):
    rotatedBeaconLst = []

    # print("- rotateBeacon:", rotateId)

    for beaconCoord in beaconLst:
        if rotateId < 4:
            beaconCoord = (beaconCoord[0], beaconCoord[1], beaconCoord[2])  # rot z = z
        elif rotateId < 8:
            beaconCoord = (-beaconCoord[0], beaconCoord[1], -beaconCoord[2])  # reverse z
        elif rotateId < 12:
            beaconCoord = (-beaconCoord[0], beaconCoord[2], beaconCoord[1])  # rot y = z
            # print(beaconCoord)
        elif rotateId < 16:
            beaconCoord = (beaconCoord[0], beaconCoord[2], -beaconCoord[1])  # reverse z
        elif rotateId < 20:
            beaconCoord = (beaconCoord[2], beaconCoord[1], -beaconCoord[0])  # rot x = z
        elif rotateId < 24:
            beaconCoord = (-beaconCoord[2], beaconCoord[1], beaconCoord[0])  # reverse z

        step = rotateId % 4

        # rotateZ
        if step == 0:  # north
            rotatedBeaconLst.append((beaconCoord[0], beaconCoord[1], beaconCoord[2]))
        elif step == 1:  #  east
            rotatedBeaconLst.append((-beaconCoord[1], beaconCoord[0], beaconCoord[2]))
        elif step == 2:  #  south
            rotatedBeaconLst.append((-beaconCoord[0], -beaconCoord[1], beaconCoord[2]))
        elif step == 3:  # west
            rotatedBeaconLst.append((beaconCoord[1], -beaconCoord[0], beaconCoord[2]))

    return rotatedBeaconLst


def checkMatch2(offsetA, offsetB, neededCommonBeacon):

    # print("- checkMatch: scanner:", nbBeacon)
    nbBeaconA = len(offsetA)
    nbBeaconB = len(offsetB)
    matchCount = [0] * nbBeaconB
    matchMap = [-1] * nbBeaconA
    for i in range(nbBeaconA):
        for j in range(i + 1, nbBeaconA):

            for k in range(nbBeaconB):
                for l in range(k + 1, nbBeaconB):
                    if k == l:
                        print("gotcha")
                        break
                    if offsetA[i][j] == offsetB[k][l]:
                        matchCount[k] += 1
                        matchCount[l] += 1
                        matchMap[i] = k
                        matchMap[j] = l

                        # print("GOTCHA 1")
                        # print(
                        # i,
                        # j,
                        # offsetA[i][j],
                        # k,
                        # l,
                        # offsetB[k][l],
                        # offsetB[l][k],
                        # )

                    elif offsetA[i][j] == offsetB[l][k]:
                        matchCount[k] += 1
                        matchCount[l] += 1
                        matchMap[i] = l
                        matchMap[j] = k
                        # print("GOTCHA 2")
                        # print(
                        # i,
                        # j,
                        # offsetA[i][j],
                        # k,
                        # l,
                        # offsetB[k][l],
                        # offsetB[l][k],
                        # )

    if max(matchCount) >= (neededCommonBeacon - 1):
        print("matchCount:", matchCount, max(matchCount), neededCommonBeacon)
        print("matchMap:", matchMap)
        return (max(matchCount), matchMap)

    return (0, [])

    # for i in range(nbBeacon):
    # print(offsetA[i], offsetB[matchMap[i]])


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    # calcOffset()
    # checkMatch()

    for scannerIdA in range(len(g_data["scanner"]) - 1):
        scannerA = g_data["scanner"][scannerIdA]

        # print(f"SCANNER A {scannerIdA}")
        beaconOffsetALst = calcOffset2(scannerA[KEY_BEACON])
        # print("ZZZ", scannerIdA, len(beaconOffsetALst), len(beaconOffsetALst[0]))

        for scannerIdB in range(scannerIdA + 1, len(g_data["scanner"])):
            scannerB = g_data["scanner"][scannerIdB]
            print(
                f"{ANSI_BLUE}MATCH SCANNER {scannerIdA} ({len(scannerA[KEY_BEACON])}) <-> {scannerIdB}({len(scannerB[KEY_BEACON])}){ANSI_NORM}"
            )
            for rotateId in range(24):
                rotatedBeaconLst = rotateBeacon(rotateId, scannerB[KEY_BEACON])
                # print(rotateId, rotatedBeaconLst)
                beaconOffsetBLst = calcOffset2(rotatedBeaconLst)
                # print()
                # print(beaconOffsetLst)
                if scannerIdA == 2 and scannerIdB == 3 and False:
                    for elt in beaconOffsetALst:
                        print("A", elt, len(beaconOffsetBLst), len(elt))
                    print()
                    for elt in beaconOffsetBLst:
                        print("B", elt, len(beaconOffsetBLst), len(elt))
                res = checkMatch2(beaconOffsetALst, beaconOffsetBLst, 12)
                if res[0] > 0:
                    # print("    GOTCHA", res[0], res[1])
                    print(f"{ANSI_GREEN}  Rotate {rotateId} -> {res[0]+1} beacon found{ANSI_NORM}")
                    for i in range(len(scannerA[KEY_BEACON])):
                        if res[1][i] > -1:
                            print(
                                f"    {i:2}:{str(scannerA[KEY_BEACON][i]):18} -> {res[1][i]:2} -> {scannerB[KEY_BEACON][res[1][i]]}"
                            )
                    # break
                # print()
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
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile("sample3.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

"""

# https://github.com/cnovel/AdventOfCode2021/blob/master/19/19.py
def cos(i):
    if i == 0:
        return 1
    if i == 180:
        return -1
    return 0


def sin(i):
    if i == 90:
        return 1
    if i == 270:
        return -1
    return 0


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
