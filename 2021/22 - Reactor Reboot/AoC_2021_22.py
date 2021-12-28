import sys
import os
import time
import keyboard

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


def initData():
    g_data["line"] = []
    g_data["cube"] = []
    g_data["width"] = 100 + 1
    g_data["offset"] = 50
    g_data["minmax"] = [0, 0, 0, 0, 0, 0]

    width = g_data["width"]
    offset = g_data["offset"]
    # minmax = g_data["minmax"]

    for line in g_inputLines:
        line = line.replace(",", " ")
        line = line.replace("x=", "")
        line = line.replace("y=", "")
        line = line.replace("z=", "")
        line = line.replace("..", " ")
        light, x1, x2, y1, y2, z1, z2 = line.split()

        # print(light, x1, x2, y1, y2, z1, z2)

        """
        if min(int(x1), int(x2)) < minmax[0]:
            minmax[0] = min(int(x1), int(x2))
        if max(int(x1), int(x2)) > minmax[1]:
            minmax[1] = max(int(x1), int(x2))

        if min(int(y1), int(y2)) < minmax[2]:
            minmax[2] = min(int(x1), int(x2))
        if max(int(y1), int(y2)) > minmax[3]:
            minmax[3] = max(int(x1), int(x2))

        if min(int(z1), int(z2)) < minmax[4]:
            minmax[4] = min(int(z1), int(z2))
        if max(int(z1), int(z2)) > minmax[5]:
            minmax[5] = max(int(z1), int(z2))
        """

        g_data["line"].append(
            [
                True if light == "on" else False,
                int(x1) + offset,
                int(x2) + offset,
                int(y1) + offset,
                int(y2) + offset,
                int(z1) + offset,
                int(z2) + offset,
            ]
        )

    """
    minmax[0] = abs(minmax[0])
    minmax[1] = abs(minmax[1])
    minmax[2] = abs(minmax[2])
    offset = max(minmax)
    width = offset * 2 + 1
    print(minmax, offset, width)
    """

    # force for sample 1
    offset = 50
    width = offset * 2 + 1

    for z in range(width):
        cubeY = []
        for y in range(width):
            cubeY.append([0] * width)
        g_data["cube"].append(cubeY)

    print("initData:", g_data["line"])


def initData2():
    g_data["line"] = []
    g_data["cube"] = []

    for line in g_inputLines:
        line = line.replace(",", " ")
        line = line.replace("x=", "")
        line = line.replace("y=", "")
        line = line.replace("z=", "")
        line = line.replace("..", " ")
        light, x1, x2, y1, y2, z1, z2 = line.split()

        # print(light, x1, x2, y1, y2, z1, z2)

        # region = LIGTH, XLEFT, XRIGHT, YUP, YDOWN, ZFRONT, ZREAR
        g_data["line"].append([True if light == "on" else False, int(x1), int(x2), int(y1), int(y2), int(z1), int(z2)])

    print("initData2:", g_data["line"])


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    line = g_data["line"]
    cube = g_data["cube"]
    width = g_data["width"]
    offset = g_data["offset"]

    for light, x1, x2, y1, y2, z1, z2 in line:
        print(light, x1, x2, y1, y2, z1, z2)

        # set light
        for z in range(z1, z2 + 1):
            if z < 0 or z >= width:
                continue
            for y in range(y1, y2 + 1):
                if y < 0 or y >= width:
                    continue
                for x in range(x1, x2 + 1):
                    if x < 0 or x >= width:
                        continue
                    cube[z][y][x] = light

    # count light
    lightCount = 0
    for z in range(width):
        for y in range(width):
            for x in range(width):
                if cube[z][y][x] == True:
                    lightCount += 1

    return lightCount


def intersect(region1, region2):  # region = LIGTH, XLEFT, XRIGHT, YUP, YDOWN, ZFRONT, ZREAR
    # print(f"INTERSECT region1: {region1}, region2: {region2}")
    regionIntersect = []

    if region2[2] < region1[1] or region2[1] > region1[2]:
        # print(f"  -> NO MATCH X region1: ({region1[1]}, {region1[2]}) region2: ({region2[1]}, {region2[2]})")
        return []

    if region2[4] < region1[3] or region2[3] > region1[4]:
        # print(f"  -> NO MATCH Y region1: ({region1[3]}, {region1[4]}) region2: ({region2[3]}, {region2[4]})")
        return []

    if region2[6] < region1[5] or region2[5] > region1[6]:
        # print(f"  -> NO MATCH Z region1: ({region1[5]}, {region1[6]}) region2: ({region2[5]}, {region2[6]})")
        return []

    regionIntersect.append(region2[0])
    for i in range(1, 7, 2):
        if region1[i] > region2[i]:
            regionIntersect.append(region1[i])
        else:
            regionIntersect.append(region2[i])

        if region1[i + 1] < region2[i + 1]:
            regionIntersect.append(region1[i + 1])
        else:
            regionIntersect.append(region2[i + 1])

    # print(ANSI_GREEN, "  -> inter ", regionIntersect, ANSI_NORM, region1, region2)
    return regionIntersect


def explode(region, intersect, label):  # region = LIGTH, XLEFT, XRIGHT, YUP, YDOWN, ZFRONT, ZREAR
    # print(f"EXPLODE region: {region}, intersect: {intersect}")
    exploded = []
    if region[1] != intersect[1]:  # encadrement gauche de l'intersecton sur les Z
        exploded.append(
            [
                region[0],
                region[1],
                intersect[1] - 1,
                intersect[3],
                intersect[4],
                intersect[5],
                intersect[6],
                str(label) + "_LEFT",
            ]
        )
        # print("  LEFT", exploded[-1])

    if region[2] != intersect[2]:  # encadrement droit de l'intersecton sur les Z
        exploded.append(
            [
                region[0],
                intersect[2] + 1,
                region[2],
                intersect[3],
                intersect[4],
                intersect[5],
                intersect[6],
                str(label) + "_RIGHT",
            ]
        )
        # print("  RIGHT", exploded[-1])

    if region[3] != intersect[3]:  # encadrement bas de l'intersecton sur les Z
        exploded.append(
            [
                region[0],
                region[1],
                region[2],
                region[3],
                intersect[3] - 1,
                intersect[5],
                intersect[6],
                str(label) + "_DOWN",
            ],
        )
        # print("  DOWN", exploded[-1])

    if region[4] != intersect[4]:  # encadrement haut de l'intersecton sur les Z
        exploded.append(
            [
                region[0],
                region[1],
                region[2],
                intersect[4] + 1,
                region[4],
                intersect[5],
                intersect[6],
                str(label) + "_UP",
            ],
        )
        # print("  UP", exploded[-1])

    if region[5] != intersect[5]:  # encadrement avant sur les Z
        exploded.append(
            [region[0], region[1], region[2], region[3], region[4], region[5], intersect[5] - 1, str(label) + "_FRONT"]
        )
        # print("  FRONT", exploded[-1])

    if region[6] != intersect[6]:  # encadrement arriere sur les Z
        exploded.append(
            [region[0], region[1], region[2], region[3], region[4], intersect[6] + 1, region[6], str(label) + "_REAR"]
        )
        # print("  REAR", exploded[-1])

    print(ANSI_BLUE, "  -> explode ", len(exploded), exploded, ANSI_NORM, region, intersect)

    return exploded

    # check explosion validity just to be sure
    if len(exploded) > 0:
        tmpSize = 0
        for tmpRegion in exploded:
            tmpSize += regionSize(tmpRegion)
        tmpSize += regionSize(intersect)
        if regionSize(region) != tmpSize:
            print(ANSI_RED, "diff", regionSize(region), tmpSize, ANSI_NORM)
            exit()

    return exploded


def regionSize(region):
    width = region[2] - region[1] + 1
    height = region[4] - region[3] + 1
    depth = region[6] - region[5] + 1

    # print("SIZE", width * height * depth, region)
    return width * height * depth


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    line = g_data["line"]
    regionLst = []

    regionLst.append(line[0])  # first region has no intersect with previous region
    print(ANSI_YELLOW, "line:", 0, line[0], regionSize(line[0]), ANSI_NORM)

    for lineIdx in range(1, len(line)):
        print(ANSI_YELLOW, "line:", lineIdx, line[lineIdx], regionSize(line[lineIdx]), ANSI_NORM)
        # if i == 20:
        # exit()
        explodedLst = []
        explodedLst.append(line[lineIdx])
        while len(explodedLst) > 0:
            # print("  regionLst:", len(regionLst), regionLst)
            # print("  explodedLst:", len(explodedLst), explodedLst)
            for regionIdx in range(len(regionLst) - 1, -1, -1):
                region = regionLst[regionIdx]
                # print(idx, region, len(regionLst))
                resIntersect = intersect(region, explodedLst[0])

                if len(resIntersect) == 0:
                    # print("no intersec")
                    continue  # no intersec so check against next exisiting region

                resIntersect.append(str(lineIdx) + "_" + str(regionIdx) + "_INTERSEC")
                print(
                    ANSI_GREEN,
                    "  -> inter ",
                    resIntersect,
                    regionSize(resIntersect),
                    ANSI_NORM,
                    lineIdx,
                    regionIdx,
                    region,
                    explodedLst[0],
                )

                resExplode = explode(explodedLst[0], resIntersect, str(lineIdx) + "_" + str(regionIdx))
                # if len(resExplode) == 0 and region[0] == resIntersect[0]:
                # continue

                # add newly exploded regions to the scan list
                if region[0] != resIntersect[0]:  # if light is different
                    # if region[0] != resIntersect[0]:  # if light is different
                    print(ANSI_RED, "    keep intersect", ANSI_NORM)
                    regionLst.append(resIntersect)
                    # explodedLst.append(resIntersect)
                else:
                    print(ANSI_PURPLE, "    keep extrasect", ANSI_NORM)
                    for tmpRegion in resExplode:
                        explodedLst.append(tmpRegion)
                explodedLst.pop(0)  # remove exploded region
                # print("  explodedLst:", explodedLst)
                break  # check newly created region against all existing region
            else:  # sortie normale du for (sans break)
                # print(idx)
                # if len(resIntersect) == 0:
                # if idx == -1:
                regionLst.append(explodedLst.pop(0))
                print(ANSI_GREY, "regionLst updated", regionLst[-1], regionSize(regionLst[-1]), ANSI_NORM)

                # print("-> regionLst:", regionLst)
                # print("-> explodedLst:", explodedLst)
                # print()
                # keyboard.wait("space")

    sum = 0
    for regionIdx, region in enumerate(regionLst):
        if region[0] == True:
            sum += regionSize(region)
            print("ADD", regionIdx, region, regionSize(region), sum)
        else:
            sum -= regionSize(region)
            print("SUB", regionIdx, region, regionSize(region), sum)

    return sum


############
### MAIN ###
############

"""
for i in range(5):
    print(i)
    # break
else:
    print("break", i)
print("->", i)
exit()
"""

g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
# g_inputLines = readInputFile("sample3.txt")
# g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

initData2()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
# too high 1457340527889594
