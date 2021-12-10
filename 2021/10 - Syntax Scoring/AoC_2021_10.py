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


def checkChuncks():
    OPENING_DELIM = ["(", "[", "{", "<"]
    MATCHING_CLOSING_DELIM = {")": "(", "]": "[", "}": "{", ">": "<"}
    MATCHING_OPENING_DELIM = {"(": ")", "[": "]", "{": "}", "<": ">"}
    CORRUPTED_SCORE = {")": 3, "]": 57, "}": 1197, ">": 25137}
    COMPLETED_SCORE = {")": 1, "]": 2, "}": 3, ">": 4}

    scoreCorrupted = 0
    scoreCompletedLst = []
    for line in g_data["line"]:
        print("###", line)
        chunks = []
        corrupted = False
        for delim in line:
            if delim in OPENING_DELIM:  # opening bracket
                chunks.append(delim)
                # print("IN  ", delim, chunks)
            else:  # closing bracket
                if chunks[-1] == MATCHING_CLOSING_DELIM[delim]:
                    chunks.pop()
                    # print("OUT ", delim, chunks)
                else:
                    # print("CORRUPTED", delim, chunks)
                    corrupted = True
                    break
        if corrupted:
            print(
                f"  CORRUPTED expected {MATCHING_OPENING_DELIM[chunks[-1]]} found {delim}, score: {CORRUPTED_SCORE[delim]}"
            )
            scoreCorrupted += CORRUPTED_SCORE[delim]
        elif len(chunks) > 0:
            # print(chunks)
            score = 0
            for i in range(len(chunks) - 1, -1, -1):
                score = score * 5 + COMPLETED_SCORE[MATCHING_OPENING_DELIM[chunks[i]]]
            scoreCompletedLst.append(score)
            print("  INCOMPLETE", chunks, scoreCompletedLst[-1])
        else:
            print("  VALID")
        print()

        scoreCompletedLst = sorted(scoreCompletedLst)
        scoreCompleted = scoreCompletedLst[int(len(scoreCompletedLst) / 2)]

    return scoreCorrupted, scoreCompleted


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    return checkChuncks()[0]


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    return checkChuncks()[1]


############
### MAIN ###
############

# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
