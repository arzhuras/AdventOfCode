from tools import *


def loadMatrix3d(argFile):
    rawInput = readInputFile(argFile)

    matrix3d = []
    gridXY = []
    for line in rawInput:
        line = line.rstrip("\n")
        # print(line)
        if len(line) == 0:
            # print(gridXY)
            matrix3d.append(gridXY)
            gridXY = []
            continue

        gridXY.append([car for car in line])
    matrix3d.append(gridXY)

    return matrix3d


"""
def showMatrix3dH(matrix3d):
    size = len(matrix3d)
    for y in range(size):
        for z in range(size):
            for x in range(size):
                print(matrix3d[z][y][x], end="")
            print(" ", end="")
        print()
    print()
"""

# visualise les tranches (y,x) selon z
#
#  y
#  ^
#  | /z
#  |/
#  +---> x
#


def showMatrix3dV(matrix3d, span=1):
    for z in range(len(matrix3d)):
        print(f"[{z}]")
        for y in range(len(matrix3d[z])):
            for x in range(len(matrix3d[z][y])):
                print(f"{matrix3d[z][y][x]:^{span}}", end="")
            print()
        print()


def rotZ3dmatrix(matrix):
    pass


if __name__ == "__main__":
    init_script()

    # loadMatrix3d
    print("@@ loadMatrix3d() @@")
    matrix3d = loadMatrix3d("matrix3d.txt")
    print()

    # showMatrix3dV
    print("@@ showMatrix3dV() @@")
    showMatrix3dV(matrix3d)
    print()

    # showMatrix3dH
    print("@@ showMatrix3dH() @@")
    # showMatrix3dH(matrix3d)
    print()
