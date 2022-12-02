from tools import *
import time

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################

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


PLAY = {"X": 1, "Y": 2, "Z": 3}

GAME_LOST = 0
GAME_DRAW = 3
GAME_WIN = 6


# A: Rock, B: Paper, C: Scissors
# X: Rock, Y: Paper, Z: Scissors
result = {
    "A X": PLAY["X"] + GAME_DRAW,
    "A Y": PLAY["Y"] + GAME_WIN,
    "A Z": PLAY["Z"] + GAME_LOST,
    "B X": PLAY["X"] + GAME_LOST,
    "B Y": PLAY["Y"] + GAME_DRAW,
    "B Z": PLAY["Z"] + GAME_WIN,
    "C X": PLAY["X"] + GAME_WIN,
    "C Y": PLAY["Y"] + GAME_LOST,
    "C Z": PLAY["Z"] + GAME_DRAW,
}

# A: Rock, B: Paper, C: Scissors
# in  X: loose, Y: draw, Z: win
# out X: Rock, Y: Paper, Z: Scissors
strat = {
    "A X": "Z",
    "A Y": "X",
    "A Z": "Y",
    "B X": "X",
    "B Y": "Y",
    "B Z": "Z",
    "C X": "Y",
    "C Y": "Z",
    "C Z": "X",
}

#############################
### INITIALISATION & DATA ###
#############################

init_script()

g_data = {}


def initData():
    g_data["line"] = []

    for line in g_inputLines:
        g_data["line"].append(line)

    # print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)

    score = 0
    for line in g_inputLines:
        score += result[line]

    return score


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    score = 0
    for line in g_inputLines:
        score += result[line[0] + " " + strat[line]]

    return score


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
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
