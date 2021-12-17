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
    line = g_inputLines[0]

    line = line.replace("target area: x=", "")
    line = line.replace("..", " ")
    line = line.replace(",", "")
    line = line.replace("y=", "")

    x1, x2, y2, y1 = line.split()
    g_data["target"] = [int(x1), int(x2), int(y1), int(y2)]

    print("initData:", g_data)


##################
### PROCEDURES ###
##################


def simulate():
    x1, x2, y1, y2 = g_data["target"]
    print(f"target: ({x1},{y1}) -> ({x2},{y2})")

    velY = y2 - 1

    velLst = []
    higher = 0
    while velY < 1000:
        velX = -1
        velY += 1
        # print(ANSI_BLUE, "New velY:", velY, ANSI_NORM)
        while velX <= x2:
            velX += 1
            curPosX = 0
            curPosY = 0
            curVelX = velX
            curVelY = velY
            curHigher = 0
            # print(f"init: {curVelX}, {curVelY}")
            step = 0
            while curPosX <= x2 and curPosY >= y2:
                curPosX += curVelX
                curPosY += curVelY
                if curPosY > curHigher:
                    curHigher = curPosY
                    # print(
                    # f"  {ANSI_GREEN}[{step:2}]: ({curPosX:3},{curPosY:3}) vel: {curVelX:3}, {curVelY:3} NEW HIGHER: {curHigher}{ANSI_NORM}"
                    # )
                else:
                    # print(f"  [{step:2}]: ({curPosX:3},{curPosY:3}) vel: {curVelX:3}, {curVelY:3} curHigher: {curHigher}")
                    pass
                if curPosX >= x1 and curPosX <= x2 and curPosY <= y1 and curPosY >= y2:
                    print(ANSI_RED, f"   GOTCHA {velX}, {velY} -> ({curPosX:3},{curPosY:3}) step: {step+1}", ANSI_NORM)
                    velLst.append((velX, velY))
                    if curHigher > higher:
                        higher = curHigher
                        print(ANSI_GREEN, f"   NEW HIGHER {higher}", ANSI_NORM)
                    break
                if curVelX > 0:
                    curVelX -= 1
                curVelY -= 1
                step += 1

    return higher, velLst


def resolve_part1(res):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return res


def resolve_part2(res):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return res


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
# g_inputLines = readInputFile("sample2.txt")
g_inputLines = readInputFile()

initData()
higher, velLst = simulate()

### PART 1 ###
startTime = time.time()
res = resolve_part1(higher)
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2(len(velLst))
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
