import sys
import os

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

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
    print("### PART 1 ###")
    prevDepth = int(g_inputLines[0])
    curDepth = -1
    measureCount = 0

    for i in range(1, len(g_inputLines)):
        curDepth = int(g_inputLines[i])
        if curDepth > prevDepth:
            measureCount += 1
        # print(f"[{i:04}] {prevDepth:4} {curDepth:4} {measureCount}")
        prevDepth = curDepth

    return measureCount


def resolve_part2():
    print()
    print("### PART 2 ###")
    prevDepth = sum(int(i) for i in g_inputLines[0:3])
    curDepth = -1
    measureCount = 0

    for i in range(1, len(g_inputLines) - 2):
        curDepth = sum(int(i) for i in g_inputLines[i : i + 3])
        if curDepth > prevDepth:
            measureCount += 1
        # print(f"[{i:04}] {prevDepth:4} {curDepth:4} {measureCount}")
        prevDepth = curDepth

    return measureCount


g_inputLines = readInputFile()

res = resolve_part1()
print(f"part1 : {res} measures larger than previous")

res = resolve_part2()
print(f"part1 : {res} window measures larger than previous")
