import sys
import os
import time
import re
import copy
import math

from collections import namedtuple

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
print(f"=== {SCRIPT_NAME} ===")


def readInputFile(file=INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines


g_inputLines = []
g_data_d = {}

#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])


def initDataStructure():
    global g_data_d

    g_data_d = {}

    # https://pythex.org/
    # patternRule = r"^(\d*): (\d*) (\d*) \| (\d*)-(\d*)
    player = "P1"
    g_data_d[player] = []
    for line in g_inputLines:
        if (len(line) == 0):
            player = "P2"
            g_data_d[player] = []
            continue

        if (line[0] == 'P'):
            continue

        g_data_d[player].append(int(line))


g_game = 0


def combat2(deck_p1_l, deck_p2_l):
    global g_game
    MAX_ROUND = 100000

    g_game += 1
    game = g_game

    round = 1
    win = 1
    #print(f"=== Game {game} ===\n")

    save_deck_p1_l = []
    save_deck_p2_l = []
    save_deck_p1_l.append(copy.deepcopy(deck_p1_l))
    save_deck_p2_l.append(copy.deepcopy(deck_p2_l))

    #save_deck_p2_s = set('_'.join(map(str, deck_p2_l)))
    #'_'.join(map(str,deck_p1_l)) in save_deck_p1_s

    infiniteFlag = False
    loserCardCount = len(deck_p1_l)
    while (loserCardCount > 0 and round < MAX_ROUND + 1 and infiniteFlag == False):
        #print(f"-- Round {round} (game {game}) --")
        #print("Player 1's deck", deck_p1_l, save_deck_p1_l)
        #print("Player 2's deck", deck_p2_l, save_deck_p2_l)

        # check recursive condition
        card1 = deck_p1_l[0]
        card2 = deck_p2_l[0]
        if (round > 1 and deck_p1_l in save_deck_p1_l and deck_p2_l in save_deck_p2_l):
            #print("INFINITE LOOP DETECTED")
            infiniteFlag = True
            win = 1
        elif (len(deck_p1_l) - 1 >= card1 and len(deck_p2_l) - 1 >= card2):
            #print("Playing a sub-game to determine the winner...")
            win = combat2(copy.deepcopy(
                deck_p1_l[1:card1+1]), copy.deepcopy(deck_p2_l[1:card2+1]))
            #print(f"... back to game {game}")
        elif (card1 > card2):
            win = 1
        else:
            win = 2

        save_deck_p1_l.append(copy.deepcopy(deck_p1_l))
        save_deck_p2_l.append(copy.deepcopy(deck_p2_l))

        if (win == 1):
            #print(f"Player 1 wins round {round} of game {game}!\n")
            if (infiniteFlag == False):
                deck_p1_l.append(deck_p1_l.pop(0))
                deck_p1_l.append(deck_p2_l.pop(0))
                loserCardCount = len(deck_p2_l)
        else:
            #print(f"Player 2 wins round {round} of game {game}!\n")
            if (infiniteFlag == False):
                deck_p2_l.append(deck_p2_l.pop(0))
                deck_p2_l.append(deck_p1_l.pop(0))
                loserCardCount = len(deck_p1_l)

        round += 1

    round -= 1
    if (round >= MAX_ROUND):
        print("!!! MAX_ROUND reached !!!")

    #print(f"\n== Post-game {game} round {round} results  ==")
    #print(f"Player's 1 deck: {deck_p1_l}")
    #print(f"Player's 2 deck: {deck_p2_l}")

    return win


def resolve_part2():
    # print("resolve_part2():", g_data_d}

    win = combat2(g_data_d["P1"], g_data_d["P2"])

    print("P1:", g_data_d["P1"])
    print("P2:", g_data_d["P2"])
    res = 0
    if (win == 1):
        tmp_l = g_data_d["P1"]
    else:
        tmp_l = g_data_d["P2"]

    weigh = len(tmp_l)
    for card in tmp_l:
        res += card * weigh
        weigh -= 1

    return res


def combat():
    round = 0
    win = ""
    lose = ""

    loserCardCount = len(g_data_d["P1"])
    while (loserCardCount > 0):
        if (g_data_d["P1"][0] > g_data_d["P2"][0]):
            win = "P1"
            lose = "P2"
        else:
            win = "P2"
            lose = "P1"
        round += 1
        #print(f"[{round}] {win} {g_data_d['P1']}         {g_data_d['P2']}" )

        g_data_d[win].append(g_data_d[win].pop(0))
        g_data_d[win].append(g_data_d[lose].pop(0))
        loserCardCount = len(g_data_d[lose])

    #print(f"[{round}] FINAL {win} {g_data_d['P1']}         {g_data_d['P2']}" )

    return win


def resolve_part1():
    #print("resolve_part1():", g_data_d)

    win = combat()
    print(f"{win} wins\n{g_data_d[win]}")

    res = 0
    weigh = len(g_data_d[win])
    for card in g_data_d[win]:
        res += card * weigh
        weigh -= 1

    return res


#g_inputLines = readInputFile("AoC_2020_22_sample2.txt")
#g_inputLines = readInputFile("AoC_2020_22_sample.txt")
g_inputLines = readInputFile()

res = -1

###
# PART 1
###

#'''
print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")
#'''

###
# PART 2
###

# '''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''
