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
    origin = (None,None)
    sandUnits = None

data = Data()


def initData():
    data.line = []

    data.minX, data.maxX = None, None
    data.minY, data.maxY = 0, None

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
    data.origin = (500 - data.minX, 0)
    #print(tmpLines)

    data.grid = []
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
                    data.grid[y][x] = f"{Ansi.blue}#{Ansi.norm}"
            elif (coordA[1] == coordB[1]): # fill x
                y = coordA[1]
                if coordA[0] < coordB[0]:
                    start, end = coordA[0] - data.minX, coordB[0] - data.minX + 1
                else:
                    start, end = coordB[0] - data.minX, coordA[0] - data.minX + 1
                for x in range(start, end):
                    data.grid[y][x] = f"{Ansi.blue}#{Ansi.norm}"
            else:
                print("error")
                exit()
            coordA = coordB

    data.maxX -= data.minX
    data.minX = 0
    data.grid[data.origin[1]][data.origin[0]] = "+"
    print("min/max", data.minX, data.maxX, data.minY, data.maxY)
    print("origin", data.origin[0], data.origin[1])
    data.sandUnits = 0
    # print("initData:", data.line)
    #showGrid(data.grid)

def addSand():
    grid = data.grid
    x = data.origin[0]
    y = data.origin[1]

    if grid[y][x] != "." and grid[y][x] != "+":
        print(f"Reservoir full: {x}, {y}")
        return False

    while True:
        while y <= data.maxY and (grid[y][x] == "." or grid[y][x] == "+"):
            y += 1
        #print("Bottom", x, y)
        if y > data.maxY:
            print(f"Sands in endless void (y): {x}, {y}")
            return False
        if grid[y][x-1] == ".":
            x -= 1
            if x < 0:
                print(f"Sands in endless void (minX): {x}, {y}")
                return False
        elif grid[y][x+1] == ".":
            x += 1
            if x > data.maxX:
                print(f"Sands in endless void (maxX): {x}, {y}")
                return False
        else:
            grid[y-1][x] = f"{Ansi.green}o{Ansi.norm}"
            data.sandUnits += 1
            # print(f"Sand {data.sandUnits} at rest: {x}, {y-1}")
            if (x <= 5):
                gridExtendX(10,0)
            elif (x >= data.maxX - 5):
                gridExtendX(0,10)
            return True

def gridExtendX(left, right):
    for i in range(0, len(data.grid)-1):
        data.grid[i] = ["."] * left + data.grid[i] + ["."] * right
    data.grid[i+1] = ["#"] * left + data.grid[i+1] + ["#"] * right
    data.maxX = data.maxX + left + right 
    data.origin = (data.origin[0] + left, data.origin[1])
    print("extend min/max", data.minX, data.maxX, data.minY, data.maxY)
    print("extend origin ", data.origin[0], data.origin[1])
        
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
    
    # showGrid(data.grid)

    ret = addSand()
    while ret == True:
        #showGrid(data.grid)
        #print()
        ret = addSand()
    showGrid(data.grid)
    print()

    return data.sandUnits


def resolve_part2():
    print()
    print(Ansi.red, "### PART 2 ###", Ansi.norm)

    # showGrid(data.grid)

    # infinite floor
    data.grid.append(["."] * (data.maxX + 1))
    data.grid.append(["#"] * (data.maxX + 1))
    data.maxY += 2

    #gridExtendX(1000,1000)
    #showGrid(data.grid)
    #exit()

    ret = addSand()
    while ret == True:
        #if data.sandUnits > 120 : 
            #showGrid(data.grid)
            #exit()
        #showGrid(data.grid)
        #print()
        ret = addSand()
    showGrid(data.grid)
    print()
    print("extend min/max", data.minX, data.maxX, data.minY, data.maxY)
    print("extend origin ", data.origin[0], data.origin[1])

    return data.sandUnits


############
### MAIN ###
############

#readInputFile("sample.txt")
# readInputFile("sample2.txt")
readInputFile()

initData()

### PART 1 ###
startTime = time.time()
res = resolve_part1()
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")

#exit()

initData()

### PART 2 ###
startTime = time.time()
res = resolve_part2()
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {Ansi.blue}{res}{Ansi.norm}")
