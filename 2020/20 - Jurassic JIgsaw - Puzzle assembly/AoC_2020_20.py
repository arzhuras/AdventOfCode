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
BORDER_N = 'N'
BORDER_E = 'E'
BORDER_S = 'S'
BORDER_O = 'O'
#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])

nessie = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "]


def addBorder(arg_tileId, arg_borderId, arg_line):
    reversedLine = arg_line[::-1]  # reverse string

    normalSet = arg_line in g_data_d['border']
    reverseSet = reversedLine in g_data_d['border']
    if (not normalSet and not reverseSet):
        #print(f"NEW BORDER {arg_tileId}, {arg_borderId}, False, {arg_line}")
        # True = reverse, False = normal
        g_data_d['border'][arg_line] = [(arg_tileId, arg_borderId, False)]
    else:
        if (normalSet):
            line = arg_line
            reverseFlag = False
        else:  # (reverseSet)
            line = reversedLine
            reverseFlag = True

        g_data_d['border'][line].append(
            (arg_tileId, arg_borderId, reverseFlag))
        g_data_d['link'][arg_tileId].append(g_data_d['border'][line][0][0])
        g_data_d['link'][g_data_d['border'][line][0][0]].append(arg_tileId)

        g_data_d['trans'][arg_tileId].append(arg_borderId)
        g_data_d['trans'][g_data_d['border'][line][0]
                          [0]].append(g_data_d['border'][line][0][1])

        #print(f"EXIST BORDER {arg_tileId}, {arg_borderId}, {reverseFlag}, {arg_line} : {g_data_d['border'][line]}")


def initDataStructure():
    global g_data_d

    g_data_d = {}
    g_data_d['tiles'] = {}
    g_data_d['border'] = {}
    g_data_d['link'] = {}
    g_data_d['trans'] = {}

    # https://pythex.org/
    #patternRule = r"^(\d*): (\d*) (\d*) \| (\d*)-(\d*)"
    tileId = 0
    lineIdx = 0
    for line in g_inputLines:
        # print(line)
        if (line == ''):
            continue

        if (line[0] == 'T'):
            line = line.replace('Tile ', '')
            line = line.replace(':', '')
            tileId = int(line)
            g_data_d['tiles'][tileId] = []
            g_data_d['link'][tileId] = []
            g_data_d['trans'][tileId] = []
            lineIdx = 0
            borderE = ''
            borderO = ''
            # print("#", tileId)

            continue

        g_data_d['tiles'][tileId].append(line)
        borderE += line[9]
        borderO += line[0]

        if (lineIdx == 0):
            addBorder(tileId, BORDER_N, line)
        elif (lineIdx == 9):
            addBorder(tileId, BORDER_E, borderE)
            addBorder(tileId, BORDER_S, line)
            addBorder(tileId, BORDER_O, borderO)

        lineIdx += 1


def show(jigsaw_l, width):
    for row in range(width):
        tmpStr = ""
        for tile in jigsaw_l[row]:
            tmpStr += f" {tile:<10}"
        print(tmpStr)
        for line in range(len(g_data_d['tiles'][jigsaw_l[0][0]])):
            tmpStr = ""
            for col in range(width):
                tmpStr += " " + g_data_d['tiles'][jigsaw_l[row][col]][line]
            print(tmpStr)


def flipV(cur, tile_l):
    #print("FLIPV", cur, tile_l)
    lineSize = len(tile_l)
    for row in range(lineSize // 2):
        tmpLine = tile_l[row]
        tile_l[row] = tile_l[lineSize - row - 1]
        tile_l[lineSize - row - 1] = tmpLine
    #print("FLIPV", cur, g_data_d['tiles'][cur])


def flipH(cur, tile_l):
    #print("FLIPH", cur, tile_l)
    lineSize = len(tile_l)
    for row in range(lineSize):
        # reverse string
        tile_l[row] = tile_l[row][::-1]
    #print("FLIPH", cur, g_data_d['tiles'][cur])


def rotR(cur, tile_l):
    #print("ROTR", cur, tile_l)
    lineSize = len(tile_l)

    # rotate right
    tmp_l = [[''] * lineSize for _ in range(lineSize)]
    for row in range(lineSize):
        for col in range(lineSize):
            tmp_l[col][lineSize - row - 1] = tile_l[row][col]
    for row in range(lineSize):
        #print(row, ''.join(tmp_l[row]))
        tile_l[row] = ''.join(tmp_l[row])

    #print("ROTR", cur, g_data_d['tiles'][cur])

    if (cur == 0):
        return

    for i in range(len(g_data_d['trans'][cur])):
        if (g_data_d['trans'][cur][i] == 'N'):
            g_data_d['trans'][cur][i] = 'E'
        elif (g_data_d['trans'][cur][i] == 'E'):
            g_data_d['trans'][cur][i] = 'S'
        elif (g_data_d['trans'][cur][i] == 'S'):
            g_data_d['trans'][cur][i] = 'O'
        elif (g_data_d['trans'][cur][i] == 'O'):
            g_data_d['trans'][cur][i] = 'N'


def rotL(cur, tile_l):
    #print("ROTL", cur, tile_l)
    lineSize = len(tile_l)

    # rotate left
    tmp_l = [[''] * lineSize for _ in range(lineSize)]
    for row in range(lineSize):
        for col in range(lineSize):
            #print(row, col, lineSize)
            tmp_l[lineSize - col - 1][row] = tile_l[row][col]
    for row in range(lineSize):
        #print(row, ''.join(tmp_l[row]))
        tile_l[row] = ''.join(tmp_l[row])

    #print("ROTL", cur, g_data_d['tiles'][cur])

    if (cur == 0):
        return

    for i in range(len(g_data_d['trans'][cur])):
        if (g_data_d['trans'][cur][i] == 'N'):
            g_data_d['trans'][cur][i] = 'O'
        elif (g_data_d['trans'][cur][i] == 'E'):
            g_data_d['trans'][cur][i] = 'N'
        elif (g_data_d['trans'][cur][i] == 'S'):
            g_data_d['trans'][cur][i] = 'E'
        elif (g_data_d['trans'][cur][i] == 'O'):
            g_data_d['trans'][cur][i] = 'S'


def searchNessie(picture_l, pattern_l, nessieHeigth, nessieWidth, nessieWeight):
    nessieLocation = []
    for row in range(len(picture_l) - nessieHeigth + 1):
        for col in range(len(picture_l[0]) - nessieWidth + 1):
            #if (row == 2 and col == 2):
                #print(f"  ({row},{col}) {picture_l[row][col:col+20]}")
                #print(f"  ({row+1},{col}) {picture_l[row+1][col:col+20]}")
                #print(f"  ({row+2},{col}) {picture_l[row+2][col:col+20]}")
                #print(pattern_l)

            matchCount = 0
            for patIdx in range(nessieHeigth):
                for ofsCol in pattern_l[patIdx]:
                    if (picture_l[row + patIdx][col + ofsCol] == '#'):
                        matchCount += 1
            if (matchCount == nessieWeight):
                print("!!! BINGO !!!", row, col)
                nessieLocation.append((row, col))

    return nessieLocation


def resolve_part2():
    # print("resolve_part2():", g_data_d}
    # for tile in g_data_d['link'].keys():
    #print(f"link [{tile}] {g_data_d['link'][tile]}")
    #print(f"            {g_data_d['trans'][tile]}")

    width = int(math.sqrt(len(g_data_d['tiles'])))
    #print(f"# tiles: {len(g_data_d['tiles'])}, width: {width}")

    # Nettoyage des border sans lien pour ne garder que les borders unique
    tmp_l = []
    for border in g_data_d['border'].keys():
        if (len(g_data_d['border'][border]) > 1):
            #print(f"border: {border} -> {g_data_d['border'][border]}")
            pass
        else:
            tmp_l.append(border)
    for border in tmp_l:  # suppresion des border sans lien
        g_data_d['border'].pop(border)

    # on sélectionne un coin au hasard -> le premier
    for key, value in g_data_d['link'].items():
        if (len(value) == 2):
            #print("first corner", key)
            break

    # On construit la grille du puzzle
    jigsaw_l = [[0] * width for _ in range(width)]
    jigsaw_l[0][1] = g_data_d['link'][key][0]
    jigsaw_l[1][0] = g_data_d['link'][key][1]

    #print("jigsaw_l:", jigsaw_l)

    #for tile in g_data_d['link'].keys():
        #print(f"link[{tile}] {g_data_d['link'][tile]}")
        #print(f"            {g_data_d['trans'][tile]}")
    tmp_l = copy.deepcopy(g_data_d['link'])
    #print("tmp_l", tmp_l)

    # construction de la première ligne en partant sur un coté au hasard
    row = 0
    jigsaw_l[0][0] = key
    for col in range(width):
        cur = jigsaw_l[row][col]
        down = tmp_l[cur][0]
        right = 0
        if (col < width - 1):
            if (len(tmp_l[down]) == 4):
                right = tmp_l[cur][1]
            else:
                right = tmp_l[cur][0]
                down = tmp_l[cur][1]
        #print(f"  ({row},{col}) {cur} right:{right}, down:{down}")

        del tmp_l[cur]  # pas nécessaire
        jigsaw_l[row+1][col] = down
        tmp_l[down].remove(cur)
        if (col > 0):
            tmp_l[jigsaw_l[row+1][col-1]].remove(down)
            tmp_l[down].remove(jigsaw_l[row+1][col-1])

        if (col < width - 1):
            jigsaw_l[row][col+1] = right
            tmp_l[right].remove(cur)
        #print("tmp_l", tmp_l)
    #print("jigsaw_l:", jigsaw_l)

    # remplissage des lignes suivantes
    for row in range(1, width-1):
        for col in range(width):
            cur = jigsaw_l[row][col]

            down = tmp_l[cur][0]
            #print(f"  ({row},{col}) {cur} down:{down}")
            if (len(tmp_l[cur]) != 1):
                print("!!!! ERROR", cur, tmp_l[cur])

            del tmp_l[cur]  # pas nécessaire
            jigsaw_l[row+1][col] = down
            tmp_l[down].remove(cur)

            if (col > 0):  # on supprime le lien down avec le tile sud ouest
                #right = jigsaw_l[row][col+1]
                tmp_l[jigsaw_l[row+1][col-1]].remove(down)
                #print(f"  sud ouest:{jigsaw_l[row+1][col-1]} cut link {tmp_l[jigsaw_l[row+1][col-1]]} -> {down}")
                tmp_l[down].remove(jigsaw_l[row+1][col-1])
                #print(f"  down:{down} cut link {down} -> {tmp_l[jigsaw_l[row+1][col-1]]}")

            #print(down, tmp_l[down])
    # for lst in jigsaw_l:
        #print("jigsaw_l:", lst)

    # print("tmp_l", tmp_l)

    # transformation des tiles de la première ligne
    # transformation du premier tile 0,0 -> orientation sur angle haut à gauche: S & E
    for row in range(width):
        for col in range(width):
            cur = jigsaw_l[row][col]
            #print(f"-> ({row}, {col}) = {cur}")

            # on vérifie le positionnement horizontal
            if (col == 0):  # on aligne sur la droite
                idx = g_data_d['link'][cur].index(jigsaw_l[row][col+1])
                align = g_data_d['trans'][cur][idx]

                if (align == 'O'):
                    flipH(cur, g_data_d['tiles'][cur])
                elif (align == 'N'):
                    rotR(cur, g_data_d['tiles'][cur])
                elif (align == 'S'):
                    rotL(cur, g_data_d['tiles'][cur])
            else:  # on aligne sur la gauche
                idx = g_data_d['link'][cur].index(jigsaw_l[row][col-1])
                align = g_data_d['trans'][cur][idx]

                if (align == 'E'):
                    flipH(cur, g_data_d['tiles'][cur])
                elif (align == 'N'):
                    rotL(cur, g_data_d['tiles'][cur])
                elif (align == 'S'):
                    rotR(cur, g_data_d['tiles'][cur])

            # on vérifie le positionnement vertical
            if (row == 0):  # on aligne sur le dessous
                idx = g_data_d['link'][cur].index(jigsaw_l[row+1][col])
                align = g_data_d['trans'][cur][idx]

                if (align == 'N'):
                    flipV(cur, g_data_d['tiles'][cur])
                elif (align == 'E'):
                    rotR(cur, g_data_d['tiles'][cur])
                elif (align == 'O'):
                    rotL(cur, g_data_d['tiles'][cur])
            else:  # on aligne sur le dessus
                idx = g_data_d['link'][cur].index(jigsaw_l[row-1][col])
                align = g_data_d['trans'][cur][idx]

                if (align == 'S'):
                    flipV(cur, g_data_d['tiles'][cur])
                elif (align == 'E'):
                    rotL(cur, g_data_d['tiles'][cur])
                elif (align == 'O'):
                    rotR(cur, g_data_d['tiles'][cur])

    #print("\n--- FINAL TILE SET ---")
    #show(jigsaw_l, width)

    # image finale
    #print("\n--- FINAL PICTURE ---")
    picture_l = []
    lineSize = len(g_data_d['tiles'][jigsaw_l[0][0]])
    for row in range(width):
        for line in range(lineSize):
            if (line == 0):
                continue
            if (line == lineSize - 1):
                continue

            tmpStr = ""
            for col in range(width):
                tmpStr += g_data_d['tiles'][jigsaw_l[row]
                                            [col]][line][1:lineSize-1]
            # print(tmpStr)
            picture_l.append(tmpStr)

    #for line in picture_l:
        #print(line)

    #print("\n--- Nessie ---")
    #for line in nessie:
        #print(line)
    nessieHeigth = len(nessie)
    nessieWidth = len(nessie[0])
    nessieWeight = 0
    pattern_l = []
    for row in range(nessieHeigth):
        pattern_l.append([])
        for col in range(nessieWidth):
            if (nessie[row][col] == '#'):
                pattern_l[row].append(col)
                nessieWeight += 1
    #print("pattern_l:", pattern_l, nessieHeigth, nessieWidth, nessieWeight)

    # search nessie
    nessieLocation = searchNessie(
        picture_l, pattern_l, nessieHeigth, nessieWidth, nessieWeight)

    rotL(0, picture_l)
    flipV(0, picture_l)
    
    print("")
    for line in picture_l:
        print(line)

    nessieLocation = searchNessie(
        picture_l, pattern_l, nessieHeigth, nessieWidth, nessieWeight)

    # calculate roughness
    rough = 0
    for line in picture_l:
        rough += line.count('#')

    rough -= nessieWeight * len(nessieLocation)
    return rough


def resolve_part1():
    #print("resolve_part1():", g_data_d)

    res = 1
    for key, value in g_data_d['link'].items():
        if (len(value) == 2):
            res *= key
            print(key, value, res)

    return res


#g_inputLines = readInputFile("AoC_2020_20_sample.txt")
g_inputLines = readInputFile()

res = -1

###
# PART 1
###

# '''
print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''

###
# PART 2
###

# '''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

# initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
# '''
