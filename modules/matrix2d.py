from collections import namedtuple

from tools import *

offsetTuple = namedtuple("offset", ["y", "x", "label", "move"])


class OFFSET:
    # offset neihgbors (y,x)
    NW = offsetTuple(-1, -1, "NW", "↖")
    N = offsetTuple(-1, 0, "N", "^")
    NE = offsetTuple(-1, 1, "NE", "↗")
    W = offsetTuple(0, -1, "W", "<")
    E = offsetTuple(0, +1, "E", ">")
    SW = offsetTuple(+1, -1, "SW", "↙")
    S = offsetTuple(+1, 0, "S", "v")
    SE = offsetTuple(+1, +1, "SE", "↘")
    AROUND = (NW, N, NE, W, E, SW, S, SE)
    MAP_OFFSET = {
        (-1, -1): NW,
        (-1, 0): N,
        (-1, 1): NE,
        (0, -1): W,
        (0, 1): E,
        (1, -1): SW,
        (1, 0): S,
        (1, 1): SE,
    }

    CROSS = (N, E, S, W)
    CROSSWEST = (SW, NW)
    CROSSNORTH = (NW, NE)
    CROSSEAST = (NE, SE)
    CROSSSOUTH = (SE, SW)

    NORTH = (NW, N, NE)
    EAST = (NE, E, SE)
    WEST = (NW, W, SW)
    SOUTH = (SW, S, SE)

    OPPOSITE = {NW: SE, N: S, NE: SW, W: E, E: W, SW: NE, S: N, SE: NW}
    NOTURNINGBACK = {S: [W, N, E], N: [W, S, E], W: [N, E, S], E: [N, W, S]}
    ROTATE_RIGHT = {N: E, E: S, S: W, W: N}
    ROTATE_LEFT = {N: W, W: S, S: E, E: N}

    MOVE = {"^": N, ">": E, "v": S, "<": W}


# Exemple colorset pour showGrid
# MATRIX2D_COLORSET = {"#": Ansi.cyan, "X": Ansi.red}

# Affiche une matrice


def showGrid(grid, colorset={"#": Ansi.cyan, "X": Ansi.red}, span=3, coord=True):
    if coord == True:
        print(f"{' ':>{span}}", end="")
        for x in range(len(grid[0])):
            print(f"{Ansi.blue}{x:>{span}}{Ansi.norm}", end="")
        print()
    for y in range(len(grid)):
        if coord == True:
            print(f"{Ansi.blue}{y:>{span}}{Ansi.norm}", end="")
        for x in range(len(grid[y])):
            car = str(grid[y][x])
            if car in colorset:
                print(f"{colorset[car]}{car:>{span}}{Ansi.norm}", end="")
            else:
                print(f"{car:>{span}}", end="")
        print()


def showGridLst(gridLst, colorset={"#": Ansi.cyan, "X": Ansi.red}, span=3, coord=True):
    for i in range(len(gridLst)):
        showGrid(gridLst[i], colorset, span, coord)
        print()


# Etend une grille si les côtés contiennent au moins un élement. Voir extendGridForce pour forcer quoi qu'il arrive
def extendGrid(grid, eltEmpty="."):

    # première ligne
    y = 0
    boundX = len(grid[y])
    for x in range(boundX):
        if grid[y][x] != eltEmpty:
            grid.insert(0, [eltEmpty for _ in range(boundX)])
            break

    # dernière ligne
    y = len(grid) - 1
    boundX = len(grid[y])
    for x in range(boundX):
        if grid[y][x] != eltEmpty:
            grid.append([eltEmpty for _ in range(boundX)])
            break

    # première colonne
    x = 0
    boundY = len(grid)
    for y in range(boundY):
        if grid[y][x] != eltEmpty:
            for y2 in range(boundY):
                grid[y2].insert(0, eltEmpty)
            break

    # dernière colonne
    x = len(grid[0]) - 1
    boundY = len(grid)
    for y in range(boundY):
        if grid[y][x] != eltEmpty:
            for y2 in range(boundY):
                grid[y2].append(eltEmpty)
            break


# Etend une grille sur tous les cotes systematiquement


def extendGridForce(grid, eltEmpty="."):

    # première ligne
    y = 0
    boundX = len(grid[y])
    grid.insert(0, [eltEmpty for _ in range(boundX)])

    # dernière ligne
    y = len(grid) - 1
    boundX = len(grid[y])
    grid.append([eltEmpty for _ in range(boundX)])

    # première colonne
    x = 0
    boundY = len(grid)
    for y in range(boundY):
        grid[y].insert(0, eltEmpty)

    # dernière colonne
    x = len(grid[0]) - 1
    boundY = len(grid)
    for y in range(boundY):
        grid[y].append(eltEmpty)


# compact une grille en éliminant les côtés vides


def shrinkGrid(grid, eltEmpty="."):

    # première ligne
    isEmpty = True
    while isEmpty == True:
        y = 0
        boundX = len(grid[y])
        for x in range(boundX):
            if grid[y][x] != eltEmpty:
                isEmpty = False
                break
        if isEmpty == True:
            grid.pop(0)

    # dernière ligne
    isEmpty = True
    while isEmpty == True:
        y = len(grid) - 1
        boundX = len(grid[y])
        for x in range(boundX):
            if grid[y][x] != eltEmpty:
                isEmpty = False
                break
        if isEmpty == True:
            grid.pop(y)

    # première colonne
    isEmpty = True
    while isEmpty == True:
        x = 0
        boundY = len(grid)
        for y in range(boundY):
            if grid[y][x] != eltEmpty:
                isEmpty = False
                break
        if isEmpty == True:
            for y2 in range(boundY):
                grid[y2].pop(0)

    # dernière colonne
    isEmpty = True
    while isEmpty == True:
        x = len(grid[0]) - 1
        boundY = len(grid)
        for y in range(boundY):
            if grid[y][x] != eltEmpty:
                isEmpty = False
                break
        if isEmpty == True:
            for y2 in range(boundY):
                grid[y2].pop(x)


# Affiche une matrice de bas en haut


def showStack(stack):
    for y in range(len(stack) - 1, -1, -1):
        for x in range(len(stack[y])):
            print(stack[y][x], end="")
        print()


# Charge une ou plusieurs matrices 2D depuis un fichier
def loadMatrix2d(argFile):
    rawInput = readInputFile(argFile)
    gridLst = []
    grid = []
    for line in rawInput:
        if line == "":
            gridLst.append(grid)
            grid = []
            continue
        grid.append([car for car in line])

    gridLst.append(grid)
    grid = []

    return gridLst


def loadGrid(rawInput):
    grid = []
    for line in rawInput:
        if line == "":
            break
        grid.append([car for car in line])

    return grid


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
            if (
                pieceGrid[pieceY][pieceX] != empty
                and grid[gridY + pieceY][gridX + pieceX] != empty
            ):
                # print(f"  -> overlap! {gridY}, {gridX}")
                return True
    # print(f"  -> not overlap! {gridY}, {gridX}")
    return False


if __name__ == "__main__":
    init_script()

    # load2dMatrix
    print("@@ load2datrix() @@")
    gridLst = loadMatrix2d("tetris.txt")
    print(gridLst)

    # showGridLst
    print("@@ showGridLst() @@")
    showGridLst(gridLst)
    print()

    # showStack
    print("@@ showStack() @@")
    for i in range(len(gridLst)):
        showStack(gridLst[i])
        print()

    # extendGrid
    print("@@ extendGrid() @@")
    for i in range(len(gridLst)):
        extendGrid(gridLst[i])
        showGrid(gridLst[i])
        print()

    # test pas d'extension
    extendGrid(gridLst[0])
    showGrid(gridLst[0])
    print()

    # flipHLst
    print("@@ flipHLst() @@")
    gridLstFlipH = flipHLst(gridLst)
    showGridLst(gridLstFlipH)
