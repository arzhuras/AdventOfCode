from tools import *


# Affiche une matrice
def showGrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end="")
        print()


def showGridLst(gridLst):
    for i in range(len(gridLst)):
        showGrid(gridLst[i])
        print()


# Affiche une matrice de bas en haut
def showStack(stack):
    for y in range(len(stack) - 1, -1, -1):
        for x in range(len(stack[y])):
            print(stack[y][x], end="")
        print()


def loadMatrix2d(argFile):
    rawInput = readInputFile(argFile)
    matrice2d = []
    tmpLine = []
    for line in rawInput:
        if line == "":
            matrice2d.append(tmpLine)
            tmpLine = []
            continue
        tmpLine.append([car for car in line])

    matrice2d.append(tmpLine)
    tmpLine = []

    return matrice2d


def flipH(grid):
    return list(reversed(grid))


def flipHLst(gridLst):
    # lst = [[flipV(grid)] for grid in gridLst]
    # tmpLst = []
    # for grid in gridLst:
    # print(grid)
    # tmpLst.append(flipV(grid))
    # print(tmpLst)
    return [flipH(grid) for grid in gridLst]


def isOverlap(grid, gridY, gridX, pieceGrid, empty):
    # print(f"isOverlap() {len(pieceGrid)} {len(pieceGrid[0])}")
    # showGrid(pieceGrid)
    for pieceY in range(len(pieceGrid)):
        # print("  pieceY:", pieceY, pieceGrid[pieceY])
        for pieceX in range(len(pieceGrid[pieceY])):
            # print("  pieceX:", pieceX)
            # print(
            # f"isOverlap: = piece[{pieceY},{pieceX}]={pieceGrid[pieceY][pieceX]}, grid[{gridY + pieceY}, {gridX + pieceX}]={grid[gridY + pieceY][gridX + pieceX]}"
            # )
            if pieceGrid[pieceY][pieceX] != empty and grid[gridY + pieceY][gridX + pieceX] != empty:
                # print(f"  -> overlap! {gridY}, {gridX}")
                return True
    # print(f"  -> not overlap! {gridY}, {gridX}")
    return False


if __name__ == "__main__":
    init_script()

    # load2dMatrix
    print("@@ load2datrix() @@")
    gridLst = loadMatrix2d("tetris.txt")
    print()

    # showGridLst
    print("@@ showGrid() @@")
    showGridLst(gridLst)
    print()

    # showStack
    print("@@ showStack() @@")
    for i in range(len(gridLst)):
        showStack(gridLst[i])
        print()

    # flipHLst
    gridLstFlipH = flipHLst(gridLst)
    showGridLst(gridLstFlipH)
