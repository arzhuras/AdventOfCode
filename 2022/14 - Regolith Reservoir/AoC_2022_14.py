from tools import *
import time
from collections import deque

INPUT_FILE_NAME = "input.txt"

#########################
### COMMON PROCEDURES ###
#########################


def readInputFile(argFile=INPUT_FILE_NAME):
    data.rawInput = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            data.rawInput.append(line)
    print(f"  {len(data.rawInput)} lignes")
    # print(inputLines)
    return data.rawInput


#############################
### INITIALISATION & DATA ###
#############################

init_script()


class Data:
    rawInput = []
    grid = []
    minX, maxX = None, None
    minY, maxY = 0, None

data = Data()


def initData():
    data.line = []

    tmpLines = []
    for line in data.rawInput:
        line = line.replace("->", "")
        line = line.replace(",", " ")
        fields = line.split()
        tmpFields = []
        for i in range(0, len(fields), 2):
            x = int(fields[i])
            y = int(fields[i+1])
            if (data.minX == None or x < data.minX):
                data.minX = x
            if (data.maxX == None or x > data.maxX):
                data.maxX = x
            if (data.maxY == None or y > data.maxY):
                data.maxY = y
            tmpFields.append((x,y))
        tmpLines.append(tmpFields)
    print("min/max", data.minX, data.maxX, data.minY, data.maxY)
    #print(tmpLines)

    data.grid = [["."] * (data.maxX - data.minX + 1) for _ in range(data.maxY + 1)]

    for elt in tmpLines:
        #print(elt)
        coordA = elt[0]
        for coordB in elt[1:]:
            if (coordA[0] == coordB[0]): # fill y
                x = coordA[0] - data.minX
                if coordA[1] < coordB[1]:
                    start, end = coordA[1], coordB[1] + 1
                else:
                    start, end = coordB[1], coordA[1] + 1
                for y in range(start, end):
                    data.grid[y][x] = "#"
            elif (coordA[1] == coordB[1]): # fill x
                y = coordA[1]
                if coordA[0] < coordB[0]:
                    start, end = coordA[0] - data.minX, coordB[0] - data.minX + 1
                else:
                    start, end = coordB[0] - data.minX, coordA[0] - data.minX + 1
                for x in range(start, end):
                    data.grid[y][x] = "#"
            else:
                print("error")
                exit()
            coordA = coordB
    data.grid[0][500-data.minX] = "+"
    
    # print("initData:", data.line)
    #showGrid(data.grid)


##################
### PROCEDURES ###
##################

def showGrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end="")
        print()

def resolve_part1():
    print()
    print(Ansi.red, "### PART 1 ###", Ansi.norm)
    res = 0

    showGrid(data.grid)

    return res


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)
    res = 0

    return res


############
### MAIN ###
############

readInputFile("sample.txt")
# readInputFile("sample2.txt")
# readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
