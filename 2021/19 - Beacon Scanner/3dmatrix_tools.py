import sys
import os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

INPUT_FILE_NAME = "3dmatrix_tools.txt"

#########################
### COMMON PROCEDURES ###
#########################

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"


def show3dmatrix(matrix):
    size = len(matrix)
    for z in range(size):
        for y in range(size):
            for x in range(size):
                print(matrix[z][y][x], end="")
            print(" ", end="")
        print()
    print()


print(f"-> read {INPUT_FILE_NAME}")
matrix = []
with open(INPUT_FILE_NAME, "r") as inputFile:
    tab = []
    for line in inputFile:
        line = line.rstrip("\n")
        # print(line)
        if len(line) == 0:
            matrix.append(tab)
            tab = []
        else:
            tab.append([car for car in line])
    matrix.append(tab)

print()
show3dmatrix(matrix)
