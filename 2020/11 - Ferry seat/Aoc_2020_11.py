import sys, os
import time
import copy

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

inputLines = []

def readInputFile(file = INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines

g_data_l = []
g_adj_l = []

def initDataStructure():
    global g_data_l
    global g_adj_l
    g_data_l = []
    g_adj_l = []
    width = 0
    for line in inputLines:
        if (width == 0):
            width = len(line)
        g_data_l.append(list(line))
        g_adj_l.append([0] * width)
    #print(g_data_l)

def show():
    print()
    for row in range(len(g_data_l)):
        tmpStr = ""
        for col in range(len(g_data_l[0])):
            tmpStr += g_data_l[row][col]
        tmpStr += " "
        for col in range(len(g_data_l[0])):
            tmpStr += str(g_adj_l[row][col])
        print(tmpStr)

def updateAdjacentCount2(arg_row, arg_col, arg_occupied):
    val = -1
    if (arg_occupied):
        val = 1

    maxRow = len(g_data_l)
    maxCol = len(g_data_l[0])

    for offset_row, offset_col in [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]:
        row = arg_row + offset_row
        col = arg_col + offset_col
        while row >= 0 and row < maxRow and col >= 0 and col < maxCol and g_data_l[row][col] == ".":
            row += offset_row
            col += offset_col
        if (row >= 0 and row < maxRow and col >= 0 and col < maxCol):
            g_adj_l[row][col] += val

def updateSeat2():
    #print(f"updateSeat({arg_moveCount}):", len(g_data_l), g_data_l)
    changed_l = []
    # met à jour les occupants
    for row in range(len(g_data_l)):
        for col in range(len(g_data_l[0])):
            #print(f"[{row},{col}] = {g_data_l[row][col]} {g_adj_l[row][col]}")
            if (g_data_l[row][col] == "L" and g_adj_l[row][col] == 0):
                g_data_l[row][col] = "#"
                changed_l.append([row, col, True])
            elif (g_data_l[row][col] == "#" and g_adj_l[row][col] >= 5):
                g_data_l[row][col] = "L"
                changed_l.append([row, col, False])
    
    # met à jour les nombres d'adjacents occupés
    #print(f"{len(changed_l)} CHANGE")

    for row, col, occupied in changed_l:
        #print("->", row, col, occupied)
        updateAdjacentCount2(row, col, occupied)
    
    #show()
    return len(changed_l)

def updateAdjacentCount1(arg_row, arg_col, arg_occupied):
    val = -1
    if (arg_occupied):
        val = 1

    maxRow = len(g_data_l)
    maxCol = len(g_data_l[0])
    for offset_row, offset_col in [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]:
        row = arg_row + offset_row
        col = arg_col + offset_col
        if (row >= 0 and row < maxRow and col >= 0 and col < maxCol and g_data_l[row][col] != "."):
            g_adj_l[row][col] += val
            #print("update", row, col, g_adj_l[row][col])

def updateSeat1():
    #print(f"updateSeat({arg_moveCount}):", len(g_data_l), g_data_l)
    changed_l = []
    
    # met à jour les occupants
    for row in range(len(g_data_l)):
        for col in range(len(g_data_l[0])):
            #print(f"[{row},{col}] = {g_data_l[row][col]} {g_adj_l[row][col]}")
            if (g_data_l[row][col] == "L" and g_adj_l[row][col] == 0):
                g_data_l[row][col] = "#"
                changed_l.append((row, col, True))
            elif (g_data_l[row][col] == "#" and g_adj_l[row][col] >= 4):
                g_data_l[row][col] = "L"
                changed_l.append((row, col, False))
    
    # met à jour les nombres d'adjacents occupés
    #print(f"{len(changed_l)} CHANGE")

    for row, col, occupied in changed_l:
        #print("->", row, col, occupied)
        updateAdjacentCount1(row, col, occupied)
    
    #show()
    return len(changed_l)

def countOccupied():
    occupiedCount = 0
    for row in g_data_l:
        occupiedCount += row.count("#")
    return occupiedCount

def resolve_part2():
    #print("resolve_part2():", len(g_data_l), g_data_l)
    #show()
    while updateSeat2() > 0:
        pass
    #show()

    return countOccupied()

def resolve_part1():
    #print("resolve_part1():", len(g_data_l), g_data_l, g_adj_l)
    #show()
    while updateSeat1() > 0:
        pass
    #show()

    return countOccupied()

#inputLines = readInputFile("AoC_2020_11_sample.txt")
inputLines = readInputFile()

res = -1

###
### PART 1
###

print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res}")
print(f"{toc - tic:0.4f} seconds")

###
### PART 2
###

print()
print(f"### PART 2 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
