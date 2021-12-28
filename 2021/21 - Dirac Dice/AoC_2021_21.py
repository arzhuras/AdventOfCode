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
    g_data["start"] = []

    g_data["start"].append(int(g_inputLines[0].replace("Player 1 starting position: ", "")))
    g_data["start"].append(int(g_inputLines[1].replace("Player 2 starting position: ", "")))

    print("initData:", g_data)


##################
### PROCEDURES ###
##################


def resolve_part1():
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    curPos = [g_data["start"][0] - 1, g_data["start"][1] - 1]  # 0 -> 9
    curScore = [0, 0]
    dice = 1
    roll = 0

    while curScore[0] < 1000 and curScore[1] < 1000:
        for player in 0, 1:
            roll += 3
            draw = dice % 100 + (dice + 1) % 100 + (dice + 2) % 100
            # print("->", curPos[player], draw, (curPos[player] + draw) % 10 + 1)
            curPos[player] = (curPos[player] + draw) % 10
            curScore[player] += curPos[player] + 1
            dice = (dice + 3) % 100
            # print(player + 1, dice, curPos[player] + 1, curScore[player])
            if curScore[player] >= 1000:
                break
    print(roll, curScore)

    return roll * min(curScore)


def rollQuanticDice(player, dice, pos, score, win, tab=""):
    # print(f"{tab}player: {player+1}, dice: {dice}, pos: {pos[player]+1}, score: {score[player]}, win: {win[player]}")

    if len(dice) == 3:
        draw = dice[0] % 100 + dice[1] % 100 + dice[2] % 100
        pos[player] = (pos[player] + draw) % 10
        score[player] += pos[player] + 1
        print(
            f"{tab}-> player: {player+1}, dice: {dice}, pos: {pos[player]+1}, score: {score[player]}, win: {win[player]}"
        )
        if score[player] >= 21:
            win[player] += 1
            print(
                f"{tab}-> WIN player: {player+1}, dice: {dice}, pos: {pos[player]+1}, score: {score[player]}, win: {win[player]}"
            )
            return
        player = (player + 1) % 2
        dice = []
        rollQuanticDice(player, dice, pos, score, win, tab + " ")
    else:
        for i in range(1, 4):
            dice.append(i)
            rollQuanticDice(player, dice, pos, score, win, tab + " ")
            dice.pop()

    # rollQuanticDice(curPos, curScore, curWin, tab + "  ")
    pass


def resolve_part2():
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    pos = [g_data["start"][0] - 1, g_data["start"][1] - 1]  # 0 -> 9
    score = [0, 0]
    win = [0, 0]
    dice = []

    rollQuanticDice(0, dice, pos, score, win)
    print(f"-> {pos}, {score}, {win}")

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

# initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")
