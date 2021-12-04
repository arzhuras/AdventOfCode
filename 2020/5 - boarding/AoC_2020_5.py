import sys, os
import timeit
import re 

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

#INPUT_FILE_NAME = "Aoc_2020_5_ben.txt"

def boarding():
    #seatList = [[0] * 8]  * 114 # ne marche pas, utilise toujours la même référence!!
    seatList = [[0] * 8 for i in range(114)] # initialisation correct d'une liste a 2 dimensions

    mySeatId = 0
    maxSeatId = 0
    seatCount = 0
    with open(INPUT_FILE_NAME, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            seatCount = seatCount + 1
            #print(line)

            #line = "FBFBBFFRLR" # 44 5 357
            #line = "BFFFBBFRRR" # 70 7 567
            #line = "FFFBBBFRRR" # 14 7 119
            #line = "BBFFBBFRLL" # 102 4 820

            # ROW
            minRow = 0
            maxRow = 127
            for row in range(7):
                if (line[row] == "F"):
                    maxRow = int(maxRow - ((maxRow - minRow + 1) /2))
                else:
                    minRow = int(minRow + ((maxRow - minRow + 1) /2))
                #print(f"{row}, {line[row]}, {minRow:3}, {maxRow:3}")

            # COL
            minCol = 0
            maxCol = 7
            for col in range(7,7+3):
                if (line[col] == "L"):
                    maxCol = int(maxCol - ((maxCol - minCol + 1) /2))
                else:
                    minCol = int(minCol + ((maxCol - minCol + 1) /2))
                #print(f"{col}, {line[col]}, {minCol:3}, {maxCol:3}")
            
            seatId = (minRow * 8) + minCol
            if (seatId > maxSeatId):
                maxSeatId = seatId
            
            seatList[minRow][minCol] = 1
            if (seatId in [357, 567, 119, 820]):
                print(line, seatId, minRow, minCol, seatList[minRow])

    print(maxSeatId, seatCount, 114 * 8)


    for row in range(114):
        sumrow=sum(seatList[row])
        if (sumrow > 0 and sumrow < 8):
            print(f"[{row}] - {row * 8}: {seatList[row]}")
            for col in range(8):
                if (seatList[row][col] == 0):
                    print(f"seatId= {row *8 + col} ({row},{col})")
                    #return ((row + 8) + col)
    return -1
# 0 pas bon
# 6 pas bon
# 619 trop petit
# 620 pas bon
# 909 trop grand
# 911 pas bon

def boarding2():
    return -1

###
### PART 1
###

print()
print(f"### PART 1 ###")

seatId = boarding()

print()
print(f"result part 1 = {seatId}")

###
### PART 2
###

print()
print(f"### PART 2 ###")

seatId = boarding2()

print()
print(f"result part 2 = {seatId}")