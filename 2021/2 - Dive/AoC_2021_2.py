import sys
import os

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
# INPUT_URL = "https://adventofcode.com/2021/day/" + str(1) + "/input"


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


g_inputLines = []


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    # tableau des déplacements relatifs: position & depth
    moveParam = {"forward": (1, 0), "up": (0, -1), "down": (0, 1)}

    curPos = 0
    curDepth = 0
    for line in g_inputLines:
        move, offset = line.split()
        # print(move, offset)
        curPos += int(offset) * moveParam[move][0]
        curDepth += int(offset) * moveParam[move][1]

    print(f"curPos: {curPos}, curDepth: {curDepth}")

    return curPos * curDepth


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    curAim = 0
    curPos = 0
    curDepth = 0
    for line in g_inputLines:
        move, offset = line.split()
        # print(move, offset)
        if move == "down":
            curAim += int(offset)
        elif move == "up":
            curAim -= int(offset)
        else:
            curPos += int(offset)
            curDepth += int(offset) * curAim

    print(f"curPos: {curPos}, curDepth: {curDepth}, curAim: {curAim}")

    return curPos * curDepth


# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

res = resolve_part1()
print()
print(f"-> part 1 : {ANSI_BLUE}{res}{ANSI_NORM} final position")

res = resolve_part2()
print()
print(f"-> part 2 : {ANSI_BLUE}{res}{ANSI_NORM} ")
